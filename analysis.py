import pandas as pd
from datetime import datetime, timedelta
import os
from sqlalchemy import create_engine, text
from db_url import normalize_database_url, ipv4_preferred_connect_args_for_url
from i18n import (
    category_label,
    dow_name,
    format_daily_chart_label,
    tr,
)

# Saudi Arabia Standard Time = UTC+3
SAUDI_OFFSET = timedelta(hours=3)


def _now_saudi():
    """Current datetime in Saudi Arabia local time."""
    return datetime.utcnow() + SAUDI_OFFSET


def _get_engine():
    """Return a SQLAlchemy engine for the configured database."""
    db_url = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "smartfocus.db"),
    )
    if db_url.startswith("sqlite"):
        return create_engine(db_url)
    db_url = normalize_database_url(db_url)
    cargs = ipv4_preferred_connect_args_for_url(db_url)
    opts = {}
    if cargs:
        opts["connect_args"] = cargs
    return create_engine(db_url, **opts) if opts else create_engine(db_url)


def _load_completed(user_id):
    """Load completed activities for a specific user into a DataFrame."""
    engine = _get_engine()
    try:
        with engine.connect() as conn:
            df = pd.read_sql(
                text("SELECT * FROM activities WHERE status = 'completed' AND user_id = :uid"),
                conn,
                params={"uid": user_id},
                parse_dates=["start_time", "end_time", "created_at"],
            )
        return df
    except Exception:
        return pd.DataFrame()


def _prep_df(df):
    """Add Saudi-time hour/date columns to a completed-activities DataFrame."""
    saudi_times = pd.to_datetime(df["start_time"]) + SAUDI_OFFSET
    out = df.copy()
    out = out.assign(
        start_time=saudi_times.values,
        date=saudi_times.dt.date.values,
        hour=saudi_times.dt.hour.values,
        dow=saudi_times.dt.dayofweek.values,
    )
    return out


def _score_label(score: float, locale: str) -> str:
    if score >= 80:
        return tr("score.excellent", locale)
    if score >= 60:
        return tr("score.good", locale)
    if score >= 40:
        return tr("score.fair", locale)
    return tr("score.needs_work", locale)


# ─── Dashboard Stats ──────────────────────────────────────────────────────────

def get_dashboard_stats(user_id, locale: str = "en"):
    """Return aggregated stats for the dashboard charts."""
    df = _load_completed(user_id)

    if df.empty:
        return _empty_stats(locale)

    df = _prep_df(df)
    today = _now_saudi().date()
    last7 = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    # Last 7 days daily totals
    daily = df.groupby("date")["duration"].sum().reindex(last7, fill_value=0)
    daily_labels = [format_daily_chart_label(d, locale) for d in last7]
    daily_values = [round(float(v) / 60, 1) for v in daily.values]

    # Today's category breakdown
    today_df = df[df["date"] == today]
    if not today_df.empty:
        cat_totals = today_df.groupby("category")["duration"].sum()
        category_labels = [category_label(str(x), locale) for x in cat_totals.index]
        category_values = [round(float(v) / 60, 1) for v in cat_totals.values]
        # Keep raw keys for chart colors (JS maps Study/Work/Personal)
        category_raw = [str(x) for x in cat_totals.index]
    else:
        category_labels = []
        category_values = []
        category_raw = []

    # Hourly productivity (all time)
    hourly = df.groupby("hour")["duration"].sum()
    hourly_labels = [f"{h:02d}:00" for h in range(24)]
    hourly_values = [round(float(hourly.get(h, 0)) / 60, 1) for h in range(24)]

    # Summary cards
    total_today_min = round(float(today_df["duration"].sum()) / 60, 1) if not today_df.empty else 0
    total_tasks_today = int(len(today_df))
    total_all_time_hrs = round(int(df["duration"].sum()) / 3600, 1)

    return {
        "daily": {"labels": daily_labels, "values": daily_values},
        "category": {
            "labels": category_labels,
            "values": category_values,
            "keys": category_raw,
        },
        "hourly": {"labels": hourly_labels, "values": hourly_values},
        "summary": {
            "total_today_min": total_today_min,
            "total_tasks_today": total_tasks_today,
            "total_all_time_hrs": total_all_time_hrs,
        },
    }


# ─── Productivity Score ───────────────────────────────────────────────────────

def get_productivity_score(user_id, locale: str = "en"):
    """Return a 0–100 productivity score with component breakdown."""
    today = _now_saudi().date()
    last7 = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    df = _load_completed(user_id)

    if df.empty:
        return _zero_score(locale)

    df = _prep_df(df)

    today_df = df[df["date"] == today]
    today_min = float(today_df["duration"].sum()) / 60 if not today_df.empty else 0
    tasks_today = len(today_df)

    # Focus time today → up to 40 pts (2 hours = max)
    focus_pts = min(40, round(today_min / 120 * 40))

    # Tasks completed today → up to 30 pts (3 tasks = max)
    task_pts = min(30, tasks_today * 10)

    # Consistency: active days in last 7 → up to 30 pts
    active_days = int(df[df["date"].isin(last7)]["date"].nunique())
    cons_pts = round(active_days / 7 * 30)

    score = focus_pts + task_pts + cons_pts

    return {
        "score": score,
        "label": _score_label(score, locale),
        "breakdown": {
            "focus": focus_pts,
            "tasks": task_pts,
            "consistency": cons_pts,
        },
        "today_min": round(today_min, 1),
        "tasks_today": tasks_today,
        "active_days": active_days,
    }


def _zero_score(locale: str = "en"):
    return {
        "score": 0,
        "label": tr("score.needs_work", locale),
        "breakdown": {"focus": 0, "tasks": 0, "consistency": 0},
        "today_min": 0,
        "tasks_today": 0,
        "active_days": 0,
    }


# ─── Smart Warnings ───────────────────────────────────────────────────────────

def get_warnings(user_id, locale: str = "en"):
    """Return actionable warnings based on today's activity."""
    warnings = []
    today = _now_saudi().date()
    last7 = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    df = _load_completed(user_id)

    if df.empty:
        warnings.append(
            {
                "icon": "fa-circle-play",
                "text": tr("warn.no_sessions", locale),
                "type": "info",
            }
        )
        return warnings

    df = _prep_df(df)
    today_df = df[df["date"] == today]
    today_min = float(today_df["duration"].sum()) / 60 if not today_df.empty else 0

    # No sessions today
    if today_df.empty:
        warnings.append(
            {
                "icon": "fa-circle-exclamation",
                "text": tr("warn.none_today", locale),
                "type": "danger",
            }
        )
    elif today_min < 30:
        warnings.append(
            {
                "icon": "fa-hourglass-half",
                "text": tr("warn.low_today", locale, m=round(today_min, 1)),
                "type": "warning",
            }
        )

    # Compare to 7-day average (excluding today)
    past_df = df[df["date"].isin(last7[:-1])]  # last 6 days
    if not past_df.empty:
        daily_avg = float(past_df.groupby("date")["duration"].sum().mean()) / 60
        if daily_avg > 0 and today_min < daily_avg * 0.5:
            warnings.append(
                {
                    "icon": "fa-arrow-trend-down",
                    "text": tr(
                        "warn.below_avg",
                        locale,
                        t=round(today_min, 1),
                        a=round(daily_avg, 1),
                    ),
                    "type": "warning",
                }
            )

    # Category balance warning (all tasks same category this week)
    week_df = df[df["date"].isin(last7)]
    if not week_df.empty:
        cats = week_df["category"].nunique()
        if cats == 1:
            only_cat = category_label(str(week_df["category"].iloc[0]), locale)
            warnings.append(
                {
                    "icon": "fa-layer-group",
                    "text": tr("warn.one_cat", locale, c=only_cat),
                    "type": "info",
                }
            )

    return warnings


# ─── Prediction ───────────────────────────────────────────────────────────────

def get_prediction(user_id, locale: str = "en"):
    """Predict tomorrow's best focus hour based on same day-of-week history."""
    today = _now_saudi().date()
    tomorrow_dow = (today.weekday() + 1) % 7

    df = _load_completed(user_id)

    if df.empty or len(df) < 3:
        return None

    df = _prep_df(df)

    # Filter to same day-of-week as tomorrow
    same_dow = df[df["dow"] == tomorrow_dow]
    if same_dow.empty:
        # Fall back to overall peak hour
        same_dow = df

    hourly = same_dow.groupby("hour")["duration"].sum()
    peak_hour = int(hourly.idxmax())
    sessions = int(len(same_dow))

    # Find the peak range (consecutive high hours)
    top_hours = hourly.nlargest(2).index.tolist()
    top_hours.sort()
    if len(top_hours) == 2 and abs(top_hours[1] - top_hours[0]) <= 2:
        range_label = f"{top_hours[0]:02d}:00 – {top_hours[-1]+1:02d}:00"
    else:
        range_label = f"{peak_hour:02d}:00 – {peak_hour+1:02d}:00"

    conf = tr("conf.high", locale) if sessions >= 5 else tr("conf.medium", locale) if sessions >= 2 else tr("conf.low", locale)
    day_ar = dow_name(tomorrow_dow, locale)

    title_line = tr("pred.ui_title", locale, day=day_ar)
    subtitle_line = tr("pred.ui_sub", locale, day=day_ar)
    confidence_line = tr("pred.conf_line", locale, c=conf, n=sessions)

    return {
        "hour": peak_hour,
        "range_label": range_label,
        "day_name": day_ar,
        "sessions": sessions,
        "confidence": conf,
        "title_line": title_line,
        "subtitle_line": subtitle_line,
        "confidence_line": confidence_line,
    }


# ─── Smart Recommendations ───────────────────────────────────────────────────

def get_recommendations(user_id, locale: str = "en"):
    """Generate specific, actionable productivity tips from historical data."""
    tips = []

    df = _load_completed(user_id)

    if df.empty:
        tips.append(
            {
                "icon": "fa-lightbulb",
                "title": tr("rec.get_started_title", locale),
                "text": tr("rec.get_started_text", locale),
                "type": "info",
            }
        )
        return {"tips": tips, "prediction": None}

    if len(df) < 2:
        tips.append(
            {
                "icon": "fa-lightbulb",
                "title": tr("rec.need_data_title", locale),
                "text": tr("rec.need_data_text", locale),
                "type": "info",
            }
        )
        return {"tips": tips, "prediction": None}

    df = _prep_df(df)
    today = _now_saudi().date()
    last7 = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    # ── Peak productivity hour ────────────────────────────────────────────────
    hourly_duration = df.groupby("hour")["duration"].sum()
    if not hourly_duration.empty:
        peak_hour = int(hourly_duration.idxmax())
        peak_min = round(float(hourly_duration[peak_hour]) / 60, 1)
        cutoff_hour = min(peak_hour + 3, 23)
        tips.append(
            {
                "icon": "fa-bolt",
                "title": tr("rec.peak_title", locale),
                "text": tr(
                    "rec.peak_text",
                    locale,
                    h=f"{peak_hour:02d}",
                    p=peak_min,
                    c=f"{cutoff_hour:02d}",
                ),
                "type": "success",
            }
        )

    # ── Most distracted hour ──────────────────────────────────────────────────
    hourly_avg = df.groupby("hour")["duration"].mean()
    if len(hourly_avg) >= 2:
        worst_hour = int(hourly_avg.idxmin())
        worst_avg = round(float(hourly_avg[worst_hour]) / 60, 1)
        tips.append(
            {
                "icon": "fa-triangle-exclamation",
                "title": tr("rec.distraction_title", locale),
                "text": tr(
                    "rec.distraction_text",
                    locale,
                    h=f"{worst_hour:02d}",
                    a=worst_avg,
                ),
                "type": "warning",
            }
        )

    # ── Average session length ────────────────────────────────────────────────
    avg_session = df["duration"].mean()
    avg_min = round(float(avg_session) / 60, 1)
    if avg_min < 15:
        tips.append(
            {
                "icon": "fa-clock",
                "title": tr("rec.short_sess_title", locale),
                "text": tr("rec.short_sess_text", locale, m=avg_min),
                "type": "warning",
            }
        )
    elif avg_min >= 45:
        tips.append(
            {
                "icon": "fa-clock",
                "title": tr("rec.breaks_title", locale),
                "text": tr("rec.breaks_text", locale, m=avg_min),
                "type": "info",
            }
        )
    else:
        tips.append(
            {
                "icon": "fa-clock",
                "title": tr("rec.sess_len_title", locale),
                "text": tr("rec.sess_len_text", locale, m=avg_min),
                "type": "info",
            }
        )

    # ── Category balance ──────────────────────────────────────────────────────
    cat_totals = df.groupby("category")["duration"].sum()
    total_duration = cat_totals.sum()
    if total_duration > 0 and "Study" in cat_totals:
        study_pct = round(float(cat_totals["Study"]) / total_duration * 100)
        if study_pct < 40:
            tips.append(
                {
                    "icon": "fa-book",
                    "title": tr("rec.study_warn_title", locale),
                    "text": tr("rec.study_warn_text", locale, p=study_pct),
                    "type": "warning",
                }
            )
        else:
            tips.append(
                {
                    "icon": "fa-book",
                    "title": tr("rec.study_ok_title", locale),
                    "text": tr("rec.study_ok_text", locale, p=study_pct),
                    "type": "success",
                }
            )

    # ── Focus streak ──────────────────────────────────────────────────────────
    if len(df) >= 3:
        all_dates = sorted(df["date"].unique())
        streak = 1
        max_streak = 1
        for i in range(1, len(all_dates)):
            delta = (all_dates[i] - all_dates[i - 1]).days
            if delta == 1:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 1
        if max_streak >= 2:
            tips.append(
                {
                    "icon": "fa-fire",
                    "title": tr("rec.streak_title", locale),
                    "text": tr("rec.streak_text", locale, n=max_streak),
                    "type": "success",
                }
            )

    # ── Best day of week ──────────────────────────────────────────────────────
    dow_totals = df.groupby("dow")["duration"].sum()
    if len(dow_totals) >= 2:
        best_dow = int(dow_totals.idxmax())
        best_min = round(float(dow_totals[best_dow]) / 60, 1)
        dn = dow_name(best_dow, locale)
        tips.append(
            {
                "icon": "fa-calendar-star",
                "title": tr("rec.best_day_title", locale),
                "text": tr("rec.best_day_text", locale, day=dn, m=best_min),
                "type": "success",
            }
        )

    prediction = get_prediction(user_id, locale)

    return {"tips": tips, "prediction": prediction}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _empty_stats(locale: str = "en"):
    labels_7 = [
        format_daily_chart_label(_now_saudi().date() - timedelta(days=i), locale) for i in range(6, -1, -1)
    ]
    return {
        "daily": {"labels": labels_7, "values": [0] * 7},
        "category": {"labels": [], "values": [], "keys": []},
        "hourly": {"labels": [f"{h:02d}:00" for h in range(24)], "values": [0] * 24},
        "summary": {
            "total_today_min": 0,
            "total_tasks_today": 0,
            "total_all_time_hrs": 0,
        },
    }
