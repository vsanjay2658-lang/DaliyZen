from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple user store for scaffold
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    # Placeholder: replace with DB lookup
    return User(user_id, 'demo')

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        # placeholder auth
        user = User('1', username)
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # placeholder signup
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # sample data placeholders
    data = load_data()
    habits = data.get('habits', [])
    items = data.get('items', [])
    schedules = data.get('schedules', [])
    return render_template('dashboard.html', habits=habits, items=items, schedules=schedules)


# Simple JSON file store for scaffold data (keeps features without DB setup)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data_store.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        default = {
            'habits': [
                {'name': 'Exercise', 'completed': False, 'streak': 3},
                {'name': 'Meditation', 'completed': True, 'streak': 10},
                {'name': 'Reading', 'completed': False, 'streak': 1}
            ],
            'items': [
                {'name': 'Laptop', 'carried': True},
                {'name': 'ID Card', 'carried': False},
                {'name': 'Water Bottle', 'carried': True}
            ],
            'schedules': [
                {'title': 'Team Meeting', 'date': '', 'time': '14:00', 'status': 'upcoming'}
            ],
            'profile': {'username': 'demo'}
        }
        save_data(default)
        return default
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

# Placeholders for other pages (do not modify core features)
@app.route('/habits')
@login_required
def habits():
    data = load_data()
    return render_template('habits.html', habits=data.get('habits', []))

@app.route('/items')
@login_required
def items_page():
    data = load_data()
    return render_template('items.html', items=data.get('items', []))


@app.route('/items/add', methods=['POST'])
@login_required
def add_item():
    name = request.form.get('name') or request.json.get('name') if request.is_json else None
    if not name:
        return jsonify({'ok': False, 'error': 'Name required'}), 400
    data = load_data()
    items = data.get('items', [])
    new_item = {'name': name, 'carried': False}
    items.append(new_item)
    data['items'] = items
    save_data(data)
    return jsonify({'ok': True, 'item': new_item})

@app.route('/schedule')
@login_required
def schedule():
    data = load_data()
    return render_template('schedule.html', schedules=data.get('schedules', []))


@app.route('/schedule/add', methods=['POST'])
@login_required
def add_schedule():
    title = request.form.get('title') or (request.json.get('title') if request.is_json else None)
    date = request.form.get('date') or (request.json.get('date') if request.is_json else '')
    time = request.form.get('time') or (request.json.get('time') if request.is_json else '')
    if not title:
        return jsonify({'ok': False, 'error': 'Title required'}), 400
    data = load_data()
    schedules = data.get('schedules', [])
    new_event = {'title': title, 'date': date, 'time': time, 'status': 'upcoming'}
    schedules.append(new_event)
    data['schedules'] = schedules
    save_data(data)
    return jsonify({'ok': True, 'event': new_event})

@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')


@app.route('/chatbot/message', methods=['POST'])
@login_required
def chatbot_message():
    payload = request.get_json() or {}
    msg = (payload.get('message') or '').lower()
    data = load_data()
    # simple rule-based responses
    if not msg:
        return jsonify({'ok': False, 'reply': 'Please send a message.'}), 400
    if 'miss' in msg or 'missed' in msg:
        missed = []
        for h in data.get('habits', []):
            if not h.get('completed'):
                missed.append(h.get('name'))
        forgotten = [it.get('name') for it in data.get('items', []) if not it.get('carried')]
        parts = []
        if missed:
            parts.append('Missed habits: ' + ', '.join(missed))
        if forgotten:
            parts.append('Forgotten items: ' + ', '.join(forgotten))
        reply = ' . '.join(parts) if parts else 'You didn\'t miss anything yet — nice job!'
        return jsonify({'ok': True, 'reply': reply})
    if 'tip' in msg or 'suggest' in msg:
        reply = 'Try the Pomodoro technique: 25 minutes focused work, 5 minutes break.'
        return jsonify({'ok': True, 'reply': reply})
    # default echo + simple scheduling suggestion
    if 'schedule' in msg or 'meeting' in msg:
        reply = 'I can add a schedule for you — go to Schedule and use the Add form.'
        return jsonify({'ok': True, 'reply': reply})
    return jsonify({'ok': True, 'reply': 'I\'m here to help — ask me "What did I miss today?" or request a tip.'})

@app.route('/profile')
@login_required
def profile():
    data = load_data()
    profile = data.get('profile', {'username': current_user.username})
    return render_template('profile.html', profile=profile)


@app.route('/profile/update', methods=['POST'])
@login_required
def profile_update():
    username = request.form.get('username') or (request.json.get('username') if request.is_json else None)
    if not username:
        return jsonify({'ok': False, 'error': 'Username required'}), 400
    data = load_data()
    data['profile'] = {'username': username}
    save_data(data)
    return jsonify({'ok': True, 'profile': data['profile']})

if __name__ == '__main__':
    app.run(debug=True)
