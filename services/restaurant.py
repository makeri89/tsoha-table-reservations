# pylint: disable=import-error
from flask import session
from services.user import is_restaurant
from db import db


def get_restaurant_info(restaurant_id):
    sql = 'SELECT * FROM restaurants WHERE id=:restaurant_id'
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchone()


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


def add_table(restaurant_id, size):
    if is_restaurant():
        sql = ('INSERT INTO tables (size, restaurant) '
               'VALUES (:size, :restaurant_id)')
        db.session.execute(sql, {'size': size, 'restaurant_id': restaurant_id})
        db.session.commit()


def create_reservation(restaurant_id, date, start_time, pax, allergies, wishes):
    if session['user_id']:
        user_id = session['user_id']
        sql = ('INSERT INTO reservations '
               '(restaurant, guest, date, startTime, '
               'pax, allergies, wishes, createdAt) '
               'VALUES (:restaurant_id, :user_id, :date, '
               ':startTime, :pax, :allergies, :wishes, NOW()')
        db.session.execute(sql, {
            'restaurant_id': restaurant_id,
            'user_id': user_id,
            'date': date,
            'startTime': start_time,
            'pax': pax,
            'allergies': allergies,
            'wishes': wishes})
        db.session.commit()
