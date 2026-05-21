# Wagti — Track. Focus. Improve.

> **Live demo:** [https://wagti.onrender.com](https://wagti.onrender.com)  
> **Repo:** [github.com/ghadigaad/wagti](https://github.com/ghadigaad/wagti)

A personal productivity web app to manage tasks, run a Pomodoro-style focus timer, and see how you actually work — with charts, a focus score, and smart tips from your history.

**Languages:** English and **Najdi Arabic** (RTL), switchable from the navbar.

---

## Features

- **Task Manager** — Add tasks with categories (Study / Work / Personal) and time goals
- **Deep Focus** — Pomodoro timer with **custom focus length (1–60 min)**, saved in the browser; 5 min / 15 min breaks; tab-switch alert; optional sound
- **Statistics dashboard** — Daily focus (7 days), today’s category split, hourly productivity (12-hour labels: 1–12 with AM/PM or ص/م)
- **Focus Score** — 0–100 from focus time, tasks completed, and consistency
- **Focus Alerts** — Warnings when today is quiet or below your usual pace
- **Smart timing** — Suggests a good focus window for tomorrow from past sessions
- **Recommendations** — Personalized tips (peak hours, streaks, study mix, session length)
- **Multi-user** — Private accounts; guest mode to try without signing up
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
| i18n | `i18n.py` — English / Arabic strings, 12-hour time helpers |

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

After you push to `main`, Render redeploys automatically if auto-deploy is enabled.

---

## Project Structure

```
wagti/
├── app.py              # Flask app, routes, auth
├── models.py           # SQLAlchemy models (User, Activity)
├── db_url.py           # Postgres URL helpers (SSL, optional IPv4 hostaddr)
├── i18n.py             # English / Najdi Arabic copy, locale cookie, 12h time labels
├── analysis.py         # pandas stats, warnings, predictions, recommendations
├── requirements.txt    # Python dependencies
├── Procfile            # Render start command
├── templates/
│   ├── base.html       # Shared layout, navbar, language toggle
│   ├── index.html      # Task Manager page
│   ├── focus.html      # Pomodoro timer (custom duration slider)
│   ├── dashboard.html  # Statistics & charts
│   ├── landing.html    # Marketing / signup
│   ├── login.html      # Login page
│   └── register.html   # Register page
└── static/
    ├── css/style.css   # All styles + themes + RTL
    └── js/
        ├── main.js     # Task management logic
        ├── focus.js    # Pomodoro timer (duration 1–60 min, localStorage)
        └── dashboard.js # Charts & recommendations
```

---

## License

MIT License — Copyright (c) 2026 Ghaday Gaad
