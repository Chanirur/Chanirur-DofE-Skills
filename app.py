from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "this works"

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return "login works"

@app.route('/   register')
def register():
    return "register works"