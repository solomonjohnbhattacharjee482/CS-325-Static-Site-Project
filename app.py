from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date  # <--- Crucial Import
import random # Add this line!
from flask import Flask, render_template

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey' 

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- DATABASE MODELS ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTES ---

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # 1. Fetch User's Tasks
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # 2. Define Holidays
    all_holidays = [
        {'date': date(2025, 12, 25), 'name': 'Christmas Day'},
        {'date': date(2026, 1, 1),   'name': "New Year's Day"},
        {'date': date(2026, 1, 19),  'name': 'Martin Luther King Jr. Day'},
        {'date': date(2026, 2, 16),  'name': "Washington's Birthday"},
        {'date': date(2026, 5, 25),  'name': 'Memorial Day'},
        {'date': date(2026, 6, 19),  'name': 'Juneteenth National Independence Day'},
        {'date': date(2026, 7, 3),   'name': 'Independence Day (Observed)'},
        {'date': date(2026, 9, 7),   'name': 'Labor Day'},
        {'date': date(2026, 10, 12), 'name': 'Columbus Day'},
        {'date': date(2026, 11, 11), 'name': 'Veterans Day'},
        {'date': date(2026, 11, 26), 'name': 'Thanksgiving Day'},
        {'date': date(2026, 12, 25), 'name': 'Christmas Day'},
    ]
    
    today = date.today()
    future_holidays = [h for h in all_holidays if h['date'] >= today]
    
    # 3. NEW: Quotes Logic
    quotes = [
        "The only way to do great work is to love what you do.",
        "Success is not final, failure is not fatal.",
        "Believe you can and you're halfway there.",
        "Don't watch the clock; do what it does. Keep going.",
        "Act as if what you do makes a difference. It does."
    ]
    daily_quote = random.choice(quotes)
    
    # 4. Pass 'quote' to the template
    return render_template('dashboard.html', 
                         pageTitle='Dashboard', 
                         tasks=tasks, 
                         name=current_user.username,
                         holidays=future_holidays,
                         quote=daily_quote) # <--- Pass the quote here

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    task_text = request.form.get('task_text')
    if task_text:
        new_task = Task(text=task_text, done=False, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task_to_delete = Task.query.get_or_404(id)
    if task_to_delete.user_id == current_user.id:
        db.session.delete(task_to_delete)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', pageTitle='Calendar')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)