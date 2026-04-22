from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Activity
from analysis import get_dashboard_stats, get_recommendations, get_productivity_score, get_warnings
from i18n import get_locale, template_globals, tr
from db_url import normalize_database_url, ipv4_preferred_connect_args_for_url
from sqlalchemy.exc import OperationalError
from datetime import datetime
from urllib.parse import urlparse
import os
import re
import threading
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production-please")

# ─── Database ─────────────────────────────────────────────────────────────────

_db_url = os.environ.get(
    "DATABASE_URL",
    "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "smartfocus.db"),
)
if not _db_url.startswith("sqlite"):
    try:
        u = normalize_database_url(_db_url)
        cargs = ipv4_preferred_connect_args_for_url(u)
        if cargs:
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": cargs}
        _db_url = u
    except Exception:
        pass

app.config["SQLALCHEMY_DATABASE_URI"] = _db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Do not run db.create_all() at import time: Gunicorn would exit with status 1
# if the DB is unreachable, before the process can listen. Create tables on
# the first request instead (Render can still "deploy" and you get usable logs).
# This hook MUST be registered before Flask-Login, which runs load_user and can
# hit User.query before this runs if the order is wrong (→ 500 on first load).
_db_init_lock = threading.Lock()
_db_tables_ready = False

_SUPABASE_IPV4_MSG = (
    "Wagti could not open a network connection to PostgreSQL (often: Render is IPv4-only, "
    "and Supabase 'Direct' db.….supabase.co is reachable only over IPv6).\n\n"
    "Fix: In the Supabase dashboard, open your project -> Connect (or Project Settings -> Database) "
    "-> Connection string. Use the **Session** pooler, port **5432** (not Transaction on 6543). "
    "The host looks like aws-0-REGION.pooler.supabase.com and the username is often "
    "postgres.YourProjectRef. Paste the full postgresql:// URI (with your real password) as "
    "DATABASE_URL in Render, save, and redeploy.\n\n"
    "In Render, set the service health check path to /healthz (not /) so probes do not hit the DB on HEAD /.\n"
    "To see the raw exception, set WAGTI_SHOW_DB_ERR=1 in Render (then remove it)."
)


def _db_error_looks_like_unreachable(e: BaseException) -> bool:
    parts: list[str] = [str(e)]
    o = getattr(e, "orig", None)
    if o is not None:
        parts.append(str(o))
    c = getattr(e, "__cause__", None)
    if c is not None:
        parts.append(str(c))
    text = " ".join(parts).lower()
    return any(
        x in text
        for x in (
            "network is unreachable",
            "no route to host",
            "address family not supported",
        )
    )


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.before_request
def _ensure_db_tables():
    global _db_tables_ready
    if request.path == "/healthz" or request.path.startswith("/static"):
        return
    if _db_tables_ready:
        return
    durl = os.environ.get("DATABASE_URL") or ""
    p = urlparse(durl)
    if p.port == 6543 or ":6543" in durl:
        return Response(
            "Wagti cannot use the Supabase Transaction pooler (port 6543) for first-time setup. "
            "In Supabase: Project Settings → Database → Connection string, set Type to URI, "
            "and choose Session pooler or Direct connection (db project host, port 5432). "
            "Paste that full URL as DATABASE_URL in Render, then redeploy.\n"
            "Optional: set WAGTI_SHOW_DB_ERR=1 in Render to see raw DB errors on the page for debugging.",
            status=503,
            mimetype="text/plain; charset=utf-8",
        )
    with _db_init_lock:
        if _db_tables_ready:
            return
        with app.app_context():
            try:
                db.create_all()
            except Exception as e:
                app.logger.exception("db.create_all failed: %s", e)
                durl2 = (os.environ.get("DATABASE_URL") or "").lower()
                if os.environ.get("WAGTI_SHOW_DB_ERR") == "1":
                    return Response(
                        f"Database error (set WAGTI_SHOW_DB_ERR=0 after debugging):\n\n{repr(e)}",
                        status=500,
                        mimetype="text/plain; charset=utf-8",
                    )
                if isinstance(
                    e, OperationalError
                ) and _db_error_looks_like_unreachable(
                    e
                ) and "supabase.co" in durl2:
                    return Response(
                        _SUPABASE_IPV4_MSG,
                        status=503,
                        mimetype="text/plain; charset=utf-8",
                    )
                raise
        _db_tables_ready = True


# ─── Flask-Login (after _ensure_db_tables) ──────────────────────────────────

login_manager = LoginManager(app)
login_manager.login_view = "home"
login_manager.login_message = ""


@app.context_processor
def _inject_i18n():
    return template_globals()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─── Auth Routes ──────────────────────────────────────────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated and not current_user.is_guest:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")

        loc = get_locale()

        def pw_errors(p):
            errs = []
            if len(p) < 8:
                errs.append(tr("pw.err.len", loc))
            if not re.search(r"[A-Z]", p):
                errs.append(tr("pw.err.upper", loc))
            if not re.search(r"[0-9]", p):
                errs.append(tr("pw.err.digit", loc))
            if not re.search(r"[^A-Za-z0-9]", p):
                errs.append(tr("pw.err.special", loc))
            return errs

        errors = []

        if not username or not email or not password:
            errors.append(tr("flash.all_required", loc))
        else:
            pe = pw_errors(password)
            if pe:
                errors.append(tr("flash.pw_rules", loc, rules=", ".join(pe)))
            if password != confirm:
                errors.append(tr("flash.pw_mismatch", loc))
            if User.query.filter_by(username=username).first():
                errors.append(tr("flash.user_taken", loc))
            if User.query.filter_by(email=email).first():
                errors.append(tr("flash.email_taken", loc))

        if errors:
            flash(" — ".join(errors), "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated and not current_user.is_guest:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user     = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))
        else:
            flash(tr("flash.login_bad", get_locale()), "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing"))


@app.route("/guest")
def guest():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    # Create a unique temporary guest account
    guest_id  = uuid.uuid4().hex[:8]
    username  = f"guest_{guest_id}"
    email     = f"{username}@wagti.guest"
    password  = uuid.uuid4().hex  # random, unhashable by anyone
    user = User(username=username, email=email, is_guest=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=False)
    return redirect(url_for("home"))


# ─── Page Routes ──────────────────────────────────────────────────────────────

@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("index.html")
    return render_template("landing.html")


@app.route("/landing")
def landing():
    return render_template("landing.html")


@app.route("/tasks")
@login_required
def index():
    return redirect(url_for("home"))


@app.route("/focus")
@login_required
def focus():
    return render_template("focus.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# ─── Task API ─────────────────────────────────────────────────────────────────

@app.route("/api/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks = Activity.query.filter_by(user_id=current_user.id).order_by(Activity.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


@app.route("/api/tasks", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    loc = get_locale()
    if not data or not data.get("task_name"):
        return jsonify({"error": tr("api.task_name_required", loc)}), 400

    task = Activity(
        user_id=current_user.id,
        task_name=data["task_name"].strip(),
        category=data.get("category", "Study"),
        expected_duration=int(data.get("expected_duration", 25)),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Activity.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": tr("api.task_deleted", get_locale())})


@app.route("/api/tasks/<int:task_id>/start", methods=["POST"])
@login_required
def start_task(task_id):
    active = Activity.query.filter_by(user_id=current_user.id, status="active").all()
    for a in active:
        a.end_time = datetime.utcnow()
        elapsed = int((a.end_time - a.start_time).total_seconds())
        a.duration = (a.duration or 0) + elapsed
        a.status = "pending"

    task = Activity.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    if task.status == "completed":
        return jsonify({"error": "Task already completed"}), 400

    task.start_time = datetime.utcnow()
    task.status = "active"
    db.session.commit()
    return jsonify(task.to_dict())


@app.route("/api/tasks/<int:task_id>/stop", methods=["POST"])
@login_required
def stop_task(task_id):
    task = Activity.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    if task.status != "active":
        return jsonify({"error": tr("api.task_not_active", get_locale())}), 400

    task.end_time = datetime.utcnow()
    elapsed = int((task.end_time - task.start_time).total_seconds())
    task.duration = (task.duration or 0) + elapsed
    task.status = "completed"
    db.session.commit()
    return jsonify(task.to_dict())


# ─── Dashboard & Recommendations API ─────────────────────────────────────────

@app.route("/api/dashboard")
@login_required
def api_dashboard():
    loc = get_locale()
    return jsonify(get_dashboard_stats(current_user.id, loc))


@app.route("/api/recommendations")
@login_required
def api_recommendations():
    loc = get_locale()
    return jsonify(get_recommendations(current_user.id, loc))


@app.route("/api/score")
@login_required
def api_score():
    loc = get_locale()
    return jsonify(get_productivity_score(current_user.id, loc))


@app.route("/api/warnings")
@login_required
def api_warnings():
    loc = get_locale()
    return jsonify(get_warnings(current_user.id, loc))


if __name__ == "__main__":
    app.run(debug=True)
