# Wagti — Track. Focus. Improve.

> **Live demo:** [https://wagti.onrender.com](https://wagti.onrender.com)

A personal productivity web app that helps you manage tasks, track focus time with a Pomodoro timer, and analyze your work habits with AI-powered insights.

---

## Features

- **Task Manager** — Add tasks with categories (Study / Work / Personal) and time goals
- **Deep Focus** — Pomodoro timer (25 min focus + breaks) with tab-switch alerts
- **Insights Dashboard** — Charts for daily focus, category breakdown, and hourly productivity
- **Focus Score** — 0–100 score based on focus time, tasks completed, and consistency
- **Focus Alerts** — Smart warnings when your focus is below average
- **AI Prediction** — Predicts your best focus time for tomorrow based on history
- **Multi-user** — Each user has their own private account and data
- **Dark / Light mode** — Toggle with persistence

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-Login |
| Database | PostgreSQL (Supabase) / SQLite (local) |
| ORM | SQLAlchemy |
| Data Analysis | pandas |
| Frontend | HTML, CSS, JavaScript, Chart.js |

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/ghadigaad/wagti.git
cd wagti
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

> Local mode uses SQLite automatically — no database setup needed.

---

## Deploy (Render + Supabase)

Wagti runs in production on [Render](https://render.com) with [Supabase](https://supabase.com) PostgreSQL.

**Environment variables (Render web service)**

| Variable | Required | Notes |
| --- | --- | --- |
| `DATABASE_URL` | Yes (production) | Full `postgresql://` URI. |
| `SECRET_KEY` | Yes (production) | Long random string for session signing. |
| `WAGTI_SHOW_DB_ERR` | No | Set to `1` only to print raw DB errors in responses while debugging; remove afterward. |
| `WAGTI_DB_NO_HOSTADDR` | No | Set to `1` to skip automatic IPv4 `hostaddr` hints for Postgres (rare; only if you hit TLS/DNS issues). |

**Supabase connection string (important on Render)**  
Render’s network is **IPv4-only** for outbound traffic. Supabase’s **Direct** host (`db.*.supabase.co`) is often **IPv6-only** in DNS, so connections can fail with “Network is unreachable.”

- Use the **Session** pooler URI, **port 5432** (host like `aws-0-…` or `aws-1-….pooler.supabase.com`, user like `postgres.<project-ref>`). Copy it from the Supabase dashboard: **Connect** (or **Project Settings → Database → Connection string**).
- Do **not** use the **Transaction** pooler on **port 6543** for this app: first-time table setup uses DDL that does not work reliably on that mode.
- Replace the password placeholder with your real database password; URL-encode special characters in the password.

**Health check**  
Set the Render service **health check path** to `/healthz` (returns JSON `{"status":"ok"}`). Using `/` can run database setup on `HEAD` requests and complicate deploys.

**Start command** (see `Procfile` / `render.yaml`) is typically Gunicorn binding to `$PORT`, e.g. `gunicorn app:app --bind 0.0.0.0:$PORT`.

---

## Project Structure

```
wagti/
├── app.py              # Flask app, routes, auth
├── models.py           # SQLAlchemy models (User, Activity)
├── db_url.py           # Postgres URL helpers (SSL, optional IPv4 hostaddr)
├── analysis.py         # pandas data analysis & AI insights
├── requirements.txt    # Python dependencies
├── Procfile            # Render start command
├── templates/
│   ├── base.html       # Shared layout & navbar
│   ├── index.html      # Task Manager page
│   ├── focus.html      # Pomodoro timer page
│   ├── dashboard.html  # Insights dashboard
│   ├── login.html      # Login page
│   └── register.html   # Register page
└── static/
    ├── css/style.css   # All styles + themes
    └── js/
        ├── main.js     # Task management logic
        ├── focus.js    # Pomodoro timer logic
        └── dashboard.js # Charts & insights
```

---

## License

MIT License — Copyright (c) 2026 Ghaday Gaad
