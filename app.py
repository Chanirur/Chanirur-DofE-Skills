from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField 
from wtforms.validators import InputRequired, Length, ValidationError, Email, Regexp

from flask_migrate import Migrate

from flask_bcrypt import Bcrypt

from dotenv import load_dotenv
import ssl
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure SSL context with only the ca.pem file
ssl_context = ssl.create_default_context(cafile='ca.pem')

# Ensure you set the DATABASE_URI correctly
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

#Ensures the use of only the CA for ssl
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'ssl': ssl_context
    }
}

# Initialize SQLAlchemy
db = SQLAlchemy(app)

#db migration setup
migrate = Migrate(app, db)

#bcrypt
bcrypt = Bcrypt(app)

#login setup
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Info(db.Model):
    __tablename__ = 'info'

    user_id = db.Column(db.Integer)

# Custom validator to disallow SQL harmful characters
def no_sql_harmful_chars(form, field):
    # List of characters typically associated with SQL injection or issues
    harmful_chars = ["'", '"', ";", "--", "#", "/*", "*/"]
    
    for char in harmful_chars:
        if char in field.data:
            raise ValidationError(f"Field contains forbidden character: {char}")

class RegisterForm(FlaskForm):
    # Email Field with regex to ensure proper format
    email = StringField(validators=[
        InputRequired(message="Please enter an Email address"),
        Length(max=120, message="Email cannot be more than 120 characters"),
        Email(message="Please enter a valid Email address."),
        Regexp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', message="Please enter a valid Email address."),
        no_sql_harmful_chars  # Custom validation for harmful SQL characters
    ], render_kw={"placeholder": "Email"})

    # Username Field with regex to ensure proper format
    username = StringField(validators=[
        InputRequired(message="Please enter a username"),
        Length(min=4, max=20, message="Username must be between 4-20 characters"),
        Regexp(r'^[A-Za-z0-9_-]{4,20}$', message="Username should not contain spaces and only contain letters, numbers, hyphens, or underscores."),
        no_sql_harmful_chars  # Custom validation for harmful SQL characters
    ], render_kw={"placeholder": "Username"})

    # Password Field with regex to ensure no spaces and length constraints
    password = PasswordField(validators=[
        InputRequired(message="Please enter a password"),
        Length(min=4, max=20, message="Password must be between 4-20 characters"),
        Regexp(r'^\S{4,20}$', message="Password should not contain spaces."),
        no_sql_harmful_chars  # Custom validation for harmful SQL characters
    ], render_kw={"placeholder": "Password"})
    
    # Submit Button
    submit = SubmitField("Register")

    # Custom username validation to ensure it is unique in the database
    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError("Username not available. Please choose a different one.")

    # Custom email validation to ensure it is unique in the database
    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("Email is already registered")

#form for logging in
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message = ''

    if request.method == 'POST':
        # Validate the form submission
        if form.validate_on_submit():
            # Query the database for the user by username
            user = User.query.filter_by(username=form.username.data).first()
            
            if user:
                # Check if the provided password matches the hashed password in the database
                if bcrypt.check_password_hash(user.password, form.password.data):
                    # Log the user in if the password is correct
                    login_user(user)
                    return redirect(url_for('dashboard'))
                else:
                    # Invalid password
                    error_message = 'Incorrect password. Please try again.'
                    
            else:
                # Invalid username
                error_message = 'Username not found. Please try again.'

    return render_template('login.html', form=form, error_message=error_message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if request.method == 'POST':
        if form.validate_on_submit:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(email=form.email.data, username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if request.method == 'POST':
        data = request.get_json()
        if data.get('name') == 'details':
            print(data.get('firstname'), data.get('surname'))
            response = {
                'state': 'success',
            }
            return jsonify(response)
        return('non name')
    return render_template('onboarding.html')