# pylint: disable=no-member
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def create_user(firstname, lastname, email, username, password):
    hashed_pw = generate_password_hash(password)
    sql = ('INSERT INTO users'
          ' (first_name, last_name, email, username,'
          ' password, isAdmin, isRestaurant)'
          ' VALUES'
          ' (:firstname, :lastname, :email, :username,'
          ' :password, FALSE, FALSE)')
    db.session.execute(sql, {
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'username': username,
        'password': hashed_pw
        })
    db.session.commit()


def password_check(username, password):
    sql = 'SELECT id, password FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session['user'] = user.id
        return True
    return False
