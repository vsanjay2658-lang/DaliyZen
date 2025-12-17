# DailyZen

DailyZen — Smart Habit & Daily Essentials Tracker

This scaffold implements the frontend-only UI refresh and a simple Flask backend skeleton to host templates and static assets. It intentionally keeps backend logic minimal and preserves all core feature placeholders so you can plug your existing application logic into it.

Features added:
- Live day/date/time widget in dashboard header (updates every second)
- Glassmorphism / soft-neumorphism theme (`static/css/dailyzen-theme.css`)
- Base templates and sample pages (Dashboard, Habits, Items, Schedule, Notifications, Chatbot, Profile)

Run locally (Python 3.10+):

1. Create venv and install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start the Flask dev server

```powershell
$env:FLASK_APP = 'app.py'; flask run
```

This scaffold uses SQLite for local testing; replace with MySQL in `config.py` for production.