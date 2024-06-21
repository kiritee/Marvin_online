from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Session, Message
from chat_algorithm import chat_algorithm
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'chatbot_db',
    'host': 'localhost',
    'port': 27017
}
app.secret_key = os.getenv('SECRET_KEY', 'mysecret')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.objects(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        user.save()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.objects(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    sessions = Session.objects(user=current_user)
    return render_template('index.html', sessions=sessions)

@app.route('/session/<session_id>')
@login_required
def load_session(session_id):
    session = Session.objects.get(id=session_id)
    messages = Message.objects(session=session)
    return render_template('index.html', sessions=Session.objects(user=current_user), messages=messages)

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    user_message = data.get('message')
    session_id = data.get('session_id')
    session = Session.objects.get(id=session_id)
    
    try:
        response_text = chat_algorithm(user_message)
        
        # Save user and bot messages in MongoDB
        message = Message(
            session=session,
            user_message=user_message, 
            bot_response=response_text, 
            timestamp=datetime.utcnow()
        )
        message.save()
        session.update(push__messages=message)
        
        return jsonify({'response': response_text})
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'response': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
