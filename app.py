from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
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

print(app.config['SQLALCHEMY_DATABASE_URI'])
print(app.config['SECRET_KEY'])

#Ensures the use of only the CA for ssl
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'ssl': ssl_context
    }
}

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return "login works"

@app.route('/register')
def register():
    return "register works"
