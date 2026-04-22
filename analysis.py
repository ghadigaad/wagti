import pandas as pd
from datetime import datetime, timedelta
import os
from sqlalchemy import create_engine, text
from db_url import normalize_database_url

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
    if not db_url.startswith("sqlite"):
        db_url = normalize_database_url(db_url)
    return create_engine(db_url)


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


# ─── Dashboard Stats ──────────────────────────────────────────────────────────

def get_dashboard_stats(user_id):
    """Return aggregated stats for the dashboard charts."""
    df = _load_completed(user_id)

    if df.empty:
        return _empty_stats()

    df = _prep_df(df)
    today  = _now_saudi().date()
    last7  = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    # Last 7 days daily totals
    daily       = df.groupby("date")["duration"].sum().reindex(last7, fill_value=0)
    daily_labels = [d.strftime("%a %d") for d in last7]
    daily_values = [round(float(v) / 60, 1) for v in daily.values]

    # Today's category breakdown
    today_df = df[df["date"] == today]
    if not today_df.empty:
        cat_totals      = today_df.groupby("category")["duration"].sum()
        category_labels = list(cat_totals.index)
        category_values = [round(float(v) / 60, 1) for v in cat_totals.values]
    else:
        category_labels = []
        category_values = []

    # Hourly productivity (all time)
    hourly        = df.groupby("hour")["duration"].sum()
    hourly_labels = [f"{h:02d}:00" for h in range(24)]
    hourly_values = [round(float(hourly.get(h, 0)) / 60, 1) for h in range(24)]

    # Summary cards
    total_today_min    = round(float(today_df["duration"].sum()) / 60, 1) if not today_df.empty else 0
    total_tasks_today  = int(len(today_df))
    total_all_time_hrs = round(int(df["duration"].sum()) / 3600, 1)

    return {
        "daily":    {"labels": daily_labels,    "values": daily_values},
        "category": {"labels": category_labels, "values": category_values},
        "hourly":   {"labels": hourly_labels,   "values": hourly_values},
        "summary": {
            "total_today_min":    total_today_min,
            "total_tasks_today":  total_tasks_today,
            "total_all_time_hrs": total_all_time_hrs,
        },
    }


# ─── Productivity Score ───────────────────────────────────────────────────────

def get_productivity_score(user_id):
    """Return a 0–100 productivity score with component breakdown."""
    today  = _now_saudi().date()
    last7  = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    df = _load_completed(user_id)

    if df.empty:
        return _zero_score()

    df = _prep_df(df)

    today_df    = df[df["date"] == today]
    today_min   = float(today_df["duration"].sum()) / 60 if not today_df.empty else 0
    tasks_today = len(today_df)

    # Focus time today → up to 40 pts (2 hours = max)
    focus_pts = min(40, round(today_min / 120 * 40))

    # Tasks completed today → up to 30 pts (3 tasks = max)
    task_pts = min(30, tasks_today * 10)

    # Consistency: active days in last 7 → up to 30 pts
    active_days = int(df[df["date"].isin(last7)]["date"].nunique())
    cons_pts    = round(active_days / 7 * 30)

    score = focus_pts + task_pts + cons_pts

    if score >= 80:
        label = "Excellent"
    elif score >= 60:
        label = "Good"
    elif score >= 40:
        label = "Fair"
    else:
        label = "Needs work"

    return {
        "score":       score,
        "label":       label,
        "breakdown": {
            "focus":       focus_pts,
            "tasks":       task_pts,
            "consistency": cons_pts,
        },
        "today_min":    round(today_min, 1),
        "tasks_today":  tasks_today,
        "active_days":  active_days,
    }


def _zero_score():
    return {
        "score": 0, "label": "Needs work",
        "breakdown": {"focus": 0, "tasks": 0, "consistency": 0},
        "today_min": 0, "tasks_today": 0, "active_days": 0,
    }


# ─── Smart Warnings ───────────────────────────────────────────────────────────

def get_warnings(user_id):
    """Return actionable warnings based on today's activity."""
    warnings = []
    today  = _now_saudi().date()
    last7  = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    df = _load_completed(user_id)

    if df.empty:
        warnings.append({
            "icon": "fa-circle-play",
            "text": "No focus sessions completed yet. Start your first task to begin tracking!",
            "type": "info",
        })
        return warnings

    df = _prep_df(df)
    today_df = df[df["date"] == today]
    today_min = float(today_df["duration"].sum()) / 60 if not today_df.empty else 0

    # No sessions today
    if today_df.empty:
        warnings.append({
            "icon": "fa-circle-exclamation",
            "text": "No focus sessions completed today. Open the Tasks page and start a task!",
            "type": "danger",
        })
    elif today_min < 30:
        warnings.append({
            "icon": "fa-hourglass-half",
            "text": f"Low focus today ({round(today_min, 1)} min). Start a 25-min session to improve.",
            "type": "warning",
        })

    # Compare to 7-day average (excluding today)
    past_df   = df[df["date"].isin(last7[:-1])]   # last 6 days
    if not past_df.empty:
        daily_avg = float(past_df.groupby("date")["duration"].sum().mean()) / 60
        if daily_avg > 0 and today_min < daily_avg * 0.5:
            warnings.append({
                "icon": "fa-arrow-trend-down",
                "text": f"Today's focus ({round(today_min, 1)} min) is well below your daily average ({round(daily_avg, 1)} min). You can do better!",
                "type": "warning",
            })

    # Category balance warning (all tasks same category this week)
    week_df = df[df["date"].isin(last7)]
    if not week_df.empty:
        cats = week_df["category"].nunique()
        if cats == 1:
            only_cat = week_df["category"].iloc[0]
            warnings.append({
                "icon": "fa-layer-group",
                "text": f"All your tasks this week are '{only_cat}'. Add variety with Work or Personal tasks.",
                "type": "info",
            })

    return warnings


# ─── Prediction ───────────────────────────────────────────────────────────────

def get_prediction(user_id):
    """Predict tomorrow's best focus hour based on same day-of-week history."""
    today        = _now_saudi().date()
    tomorrow_dow = (today.weekday() + 1) % 7
    dow_names    = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    df = _load_completed(user_id)

    if df.empty or len(df) < 3:
        return None

    df = _prep_df(df)

    # Filter to same day-of-week as tomorrow
    same_dow = df[df["dow"] == tomorrow_dow]
    if same_dow.empty:
        # Fall back to overall peak hour
        same_dow = df

    hourly    = same_dow.groupby("hour")["duration"].sum()
    peak_hour = int(hourly.idxmax())
    sessions  = int(len(same_dow))

    # Find the peak range (consecutive high hours)
    top_hours = hourly.nlargest(2).index.tolist()
    top_hours.sort()
    if len(top_hours) == 2 and abs(top_hours[1] - top_hours[0]) <= 2:
        range_label = f"{top_hours[0]:02d}:00 – {top_hours[-1]+1:02d}:00"
    else:
        range_label = f"{peak_hour:02d}:00 – {peak_hour+1:02d}:00"

    return {
        "hour":        peak_hour,
        "range_label": range_label,
        "day_name":    dow_names[tomorrow_dow],
        "sessions":    sessions,
        "confidence":  "High" if sessions >= 5 else "Medium" if sessions >= 2 else "Low",
    }


# ─── Smart Recommendations ───────────────────────────────────────────────────

def get_recommendations(user_id):
    """Generate specific, actionable productivity tips from historical data."""
    tips = []

    df = _load_completed(user_id)

    if df.empty:
        tips.append({
            "icon": "fa-lightbulb",
            "title": "Get Started",
            "text": "Complete a few tasks to receive personalized recommendations.",
            "type": "info",
        })
        return {"tips": tips, "prediction": None}

    if len(df) < 2:
        tips.append({
            "icon": "fa-lightbulb",
            "title": "Not Enough Data",
            "text": "Complete at least 2 tasks to unlock smart recommendations.",
            "type": "info",
        })
        return {"tips": tips, "prediction": None}

    df = _prep_df(df)
    today  = _now_saudi().date()
    last7  = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    # ── Peak productivity hour ────────────────────────────────────────────────
    hourly_duration = df.groupby("hour")["duration"].sum()
    if not hourly_duration.empty:
        peak_hour   = int(hourly_duration.idxmax())
        peak_min    = round(float(hourly_duration[peak_hour]) / 60, 1)
        cutoff_hour = min(peak_hour + 3, 23)
        tips.append({
            "icon": "fa-bolt",
            "title": "Peak Focus Hour",
            "text": (
                f"Your peak focus hour is {peak_hour:02d}:00 ({peak_min} min total focused). "
                f"Schedule your hardest tasks before {cutoff_hour:02d}:00 for best results."
            ),
            "type": "success",
        })

    # ── Most distracted hour ──────────────────────────────────────────────────
    hourly_avg = df.groupby("hour")["duration"].mean()
    if len(hourly_avg) >= 2:
        worst_hour   = int(hourly_avg.idxmin())
        worst_avg    = round(float(hourly_avg[worst_hour]) / 60, 1)
        tips.append({
            "icon": "fa-triangle-exclamation",
            "title": "Distraction Alert",
            "text": (
                f"{worst_hour:02d}:00 is your weakest hour (avg {worst_avg} min per session). "
                f"Avoid scheduling deep work at this time."
            ),
            "type": "warning",
        })

    # ── Average session length ────────────────────────────────────────────────
    avg_session = df["duration"].mean()
    avg_min     = round(float(avg_session) / 60, 1)
    if avg_min < 15:
        tips.append({
            "icon": "fa-clock",
            "title": "Sessions Too Short",
            "text": (
                f"Your average session is only {avg_min} min. "
                f"Your sessions are too short — try completing full 25-min focus blocks."
            ),
            "type": "warning",
        })
    elif avg_min >= 45:
        tips.append({
            "icon": "fa-clock",
            "title": "Take Breaks",
            "text": (
                f"Your average session is {avg_min} min — impressive! "
                f"Remember to take 5-min breaks to avoid burnout."
            ),
            "type": "info",
        })
    else:
        tips.append({
            "icon": "fa-clock",
            "title": "Session Length",
            "text": f"Your average focus session is {avg_min} min. Keep building consistency!",
            "type": "info",
        })

    # ── Category balance ──────────────────────────────────────────────────────
    cat_totals     = df.groupby("category")["duration"].sum()
    total_duration = cat_totals.sum()
    if total_duration > 0 and "Study" in cat_totals:
        study_pct = round(float(cat_totals["Study"]) / total_duration * 100)
        if study_pct < 40:
            tips.append({
                "icon": "fa-book",
                "title": "Study Balance",
                "text": (
                    f"Only {study_pct}% of your tracked time is Study. "
                    f"Try to dedicate at least 40% of focus time to learning."
                ),
                "type": "warning",
            })
        else:
            tips.append({
                "icon": "fa-book",
                "title": "Study Balance",
                "text": f"Great! {study_pct}% of your total time is Study. Keep it up!",
                "type": "success",
            })

    # ── Focus streak ──────────────────────────────────────────────────────────
    if len(df) >= 3:
        all_dates  = sorted(df["date"].unique())
        streak     = 1
        max_streak = 1
        for i in range(1, len(all_dates)):
            delta = (all_dates[i] - all_dates[i - 1]).days
            if delta == 1:
                streak    += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 1
        if max_streak >= 2:
            tips.append({
                "icon": "fa-fire",
                "title": "Focus Streak",
                "text": (
                    f"Your longest streak is {max_streak} consecutive days. "
                    f"Consistency compounds — keep showing up daily!"
                ),
                "type": "success",
            })

    # ── Best day of week ──────────────────────────────────────────────────────
    dow_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow_totals = df.groupby("dow")["duration"].sum()
    if len(dow_totals) >= 2:
        best_dow = int(dow_totals.idxmax())
        best_min = round(float(dow_totals[best_dow]) / 60, 1)
        tips.append({
            "icon": "fa-calendar-star",
            "title": "Best Day",
            "text": (
                f"{dow_names[best_dow]} is your most productive day ({best_min} min total). "
                f"Plan your most important work for {dow_names[best_dow]}s."
            ),
            "type": "success",
        })

    prediction = get_prediction(user_id)

    return {"tips": tips, "prediction": prediction}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _empty_stats():
    labels_7 = [(_now_saudi().date() - timedelta(days=i)).strftime("%a %d") for i in range(6, -1, -1)]
    return {
        "daily":    {"labels": labels_7, "values": [0] * 7},
        "category": {"labels": [],       "values": []},
        "hourly":   {"labels": [f"{h:02d}:00" for h in range(24)], "values": [0] * 24},
        "summary": {
            "total_today_min":    0,
            "total_tasks_today":  0,
            "total_all_time_hrs": 0,
        },
    }
