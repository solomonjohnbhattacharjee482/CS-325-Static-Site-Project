from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__, template_folder='templates')

# In-memory placeholder data
TASKS = [
    {'id': 1, 'name': 'Complete Assignment 1', 'due': '2025-11-15'},
    {'id': 2, 'name': 'Study for Final', 'due': '2025-12-10'},
    {'id': 3, 'name': 'Group Project Meeting', 'due': '2025-11-22'}
]

CAL_EVENTS = {
    '2025-11-15': ['Complete Assignment 1'],
    '2025-12-10': ['Study for Final'],
    '2025-11-22': ['Group Project Meeting']
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # placeholder: accept credentials and redirect
    username = request.form.get('username')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    now = datetime.now()
    return render_template('HomePage.html', tasks=TASKS, current_month_name=now.strftime('%B'), current_year=now.year)

@app.route('/calendar')
def calendar_view():
    return render_template('Calender.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        due = request.form.get('due')
        if name and due:
            new_id = len(TASKS) + 1
            TASKS.append({'id': new_id, 'name': name, 'due': due})
            CAL_EVENTS.setdefault(due, []).append(name)
            return redirect(url_for('dashboard'))
    return render_template('add.html')

@app.route('/api/events', methods=['GET', 'POST'])
def api_events():
    if request.method == 'GET':
        return jsonify(CAL_EVENTS)
    data = request.get_json() or {}
    date = data.get('date')
    item = data.get('item')
    if date and item:
        CAL_EVENTS.setdefault(date, []).append(item)
        return jsonify({'status': 'ok'}), 201
    return jsonify({'error': 'invalid payload'}), 400

if __name__ == '__main__':
    app.run(debug=True)
