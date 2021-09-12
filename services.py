# pylint: disable=no-member
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
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


def password_check(username, password):
    sql = 'SELECT id, password FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    if not user:
        # TODO: better error handling
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session['user_id'] = user.id
        session['username'] = username
        return True
    return False


def create_review(restaurant_name, stars, review):
    restaurant = get_restaurant_info(restaurant_name)
    sql = ('INSERT INTO reviews '
           '(restaurant, guest, stars, review, createdAt) '
           'VALUES '
           '(:restaurant, :guest, :stars, :review, NOW())')
    db.session.execute(sql, {
        'restaurant': restaurant.id,
        'guest': current_user().id,
        'stars': stars,
        'review': review
    })
    db.session.commit()


def is_admin():
    user = session['user']
    sql = 'SELECT isAdmin FROM users WHERE id=:user'
    result = db.session.execute(sql, {'user': user})
    return result.fetchone()[0]


def set_as_restaurant(user):
    sql = 'UPDATE users SET isRestaurant=TRUE WHERE id=:user_id'
    db.session.execute(sql, {'user_id': user.id})


def remove_tokens():
    del session['user_id']
    del session['username']


def current_user():
    sql = ('SELECT first_name, last_name, email, username, '
           'isAdmin, isRestaurant FROM users WHERE id=:user_id')
    result = db.session.execute(sql, {'user_id': session['user_id']})
    return result.fetchone()


def get_restaurant_info(restaurant_id):
    sql = 'SELECT * FROM restaurants WHERE id=:restaurant_id'
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchone()


def get_user_restaurant():
    user = current_user()
    sql = 'SELECT * FROM restaurants WHERE owner=:user_id'
    result = db.session.execute(sql, {'user_id': user.id})
    return result.fetchall()


def get_all_restaurants():
    sql = 'SELECT * FROM restaurants'
    result = db.session.execute(sql)
    return result.fetchall()


def get_restaurant_tables(restaurant):
    sql = 'SELECT * FROM tables WHERE restaurant=:restaurant_id'
    result = db.session.execute(sql, {'restaurant_id': restaurant.id})
    return result.fetchall()


def get_restaurant_menu(restaurant):
    sql = ('SELECT M.title, M.description, M.price, C.course '
           'FROM menuItems M, menuCourses C WHERE '
           'M.menu=(SELECT id FROM menus WHERE restaurant=:restaurant_id) '
           'and C.id=M.course')
    result = db.session.execute(sql, {'restaurant_id': restaurant.id})
    return result.fetchall()
