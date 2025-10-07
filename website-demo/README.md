# Website Demo (Flask)

This is a minimal Flask wrapper for your static pages so you can run a small local site with three pages.

How to run

1. Create a virtual environment and activate it:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

2. Install requirements:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

4. Open http://127.0.0.1:5000/ in your browser.

Notes

- The templates are in `templates/` (index, home, data_entry).
- Replace template content with your full static HTML if you want the complete layout.
