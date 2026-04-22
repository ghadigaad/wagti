# Wagti — Track. Focus. Improve.

> **Live demo:** _coming soon_

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

## Project Structure

```
wagti/
├── app.py              # Flask app, routes, auth
├── models.py           # SQLAlchemy models (User, Activity)
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
