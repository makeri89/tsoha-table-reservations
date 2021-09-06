from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_handler', methods=['POST'])
def signup_handler():
    username = request.form['username']
    password = request.form['password']
    create_user(username, password)
    return redirect('/login')


def create_user(username, password):
    hashed_pw = generate_password_hash(password)
    sql = 'INSERT INTO users (username, password) VALUES (:username, :password)'
    db.session.execute(sql, {'username': username, 'password': hashed_pw})
    db.session.commit()


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_handler', methods=['POST'])
def login_handler():
    username = request.form['username']
    password = request.form['password']
    if password_check(username, password):
        return redirect('/')
    return redirect('/login')


def password_check(username, password):
    sql = 'SELECT id, password FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session['username'] = username
        return True
    return False
