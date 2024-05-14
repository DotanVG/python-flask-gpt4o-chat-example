from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
import openai
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///chatbot.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress the warning
app.permanent_session_lifetime = timedelta(minutes=30)

# Initialize CSRF protection
csrf = CSRFProtect(app)
csrf.init_app(app)

# Initialize SQLAlchemy
db = SQLAlchemy(app)
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Flask-Limiter for rate limiting (using in-memory storage)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri='memory://'
)
limiter.init_app(app)

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Define Chat model
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)

# Load user by ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Define registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

# Define login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    return render_template('register.html', form=form)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    return render_template('login.html', form=form)

# Route for user logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Route for index page
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Route for chat functionality
@app.route('/chat', methods=['POST'])
@limiter.limit("5 per minute")
@login_required
@csrf.exempt  # Exempt the CSRF token check for this endpoint
def chat():
    user_message = request.json.get('message')
    logging.info(f"User message: {user_message}")
    try:
        response = openai.Completion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        logging.info(f"OpenAI response: {response}")
        reply = response.choices[0].message['content']
        
        chat_entry = Chat(user_id=current_user.id, message=user_message, response=reply)
        db.session.add(chat_entry)
        db.session.commit()
        
        return jsonify({"reply": reply})
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Error handler for 404
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

# Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logging.error(str(error))
    return jsonify({'error': 'An unexpected error occurred'}), 500

# Main entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('DEBUG', 'False') == 'True', port=int(os.getenv('PORT', 5000)))
