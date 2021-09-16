# pylint: disable=import-error
from flask import session
from werkzeug.security import generate_password_hash
from db import db


def create_user(firstname, lastname, email, username, password):
    hashed_pw = generate_password_hash(password)
    sql = ('INSERT INTO users '
           '(first_name, last_name, email, username, '
           'password, isAdmin, isRestaurant) '
           'VALUES '
           '(:firstname, :lastname, :email, :username, '
           ':password, FALSE, FALSE)')
    db.session.execute(sql, {
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'username': username,
        'password': hashed_pw
    })
    db.session.commit()


def is_admin():
    user_id = session['user_id']
    sql = 'SELECT isAdmin FROM users WHERE id=:user'
    result = db.session.execute(sql, {'user': user_id})
    return result.fetchone()[0]


def is_restaurant():
    user_id = session['user_id']
    sql = 'SELECT isRestaurant FROM users WHERE id=:user'
    result = db.session.execute(sql, {'user': user_id})
    return result.fetchone()[0]


def set_as_restaurant(user):
    sql = 'UPDATE users SET isRestaurant=TRUE WHERE id=:user_id'
    db.session.execute(sql, {'user_id': user.id})


def current_user():
    user_id = session['user_id']
    sql = ('SELECT first_name, last_name, email, username, '
           'isAdmin, isRestaurant FROM users WHERE id=:user_id')
    result = db.session.execute(sql, {'user_id': user_id})
    return result.fetchone()


def get_user_restaurants():
    user = current_user()
    sql = 'SELECT * FROM restaurants WHERE owner=:user_id'
    result = db.session.execute(sql, {'user_id': user.id})
    return result.fetchall()
