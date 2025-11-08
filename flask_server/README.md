Flask server for the static site (Option A)

Quick start (PowerShell on Windows):

1. Create and activate a venv
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2. Install requirements
   pip install -r requirements.txt

3. Run the app
   python app.py

Routes:
- GET /           -> login page (templates/index.html)
- POST /login     -> simple redirect to /dashboard
- GET /dashboard  -> dashboard (templates/HomePage.html)
- GET /calendar   -> calendar (templates/Calender.html)
- GET/POST /add   -> simple add task form
- GET/POST /api/events -> JSON API for calendar events (in-memory)

Notes:
- Persistence: events and tasks are stored in-memory in app.py (CAL_EVENTS, TASKS). This is a placeholder. If you want persistent storage, I can add SQLite or a JSON file.
- I kept the root static HTML files untouched; these templates in flask_server/templates are copies used by the Flask app.
- Next steps are outlined in the todo list (managed separately).
