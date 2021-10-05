# pylint: disable=import-error
from flask import session
from db import db


def create_reservation(restaurant_id, date, start_time,
                       pax, allergies='-', wishes='-'):
    if session['user_id']:
        user_id = session['user_id']
        sql = ('INSERT INTO reservations '
               '(restaurant, guest, date, startTime, '
               'pax, allergies, wishes, createdAt) '
               'VALUES (:restaurant_id, :user_id, :date, '
               ':startTime, :pax, :allergies, :wishes, NOW())')
        db.session.execute(sql, {
            'restaurant_id': restaurant_id,
            'user_id': user_id,
            'date': date,
            'startTime': start_time,
            'pax': pax,
            'allergies': allergies,
            'wishes': wishes})
        db.session.commit()


def get_reservations(restaurant_id):
    sql = ('SELECT U.id, U.last_name, R.date, R.startTime, '
           'R.pax, R.allergies, R.wishes, R.createdAt '
           'FROM reservations R, users U '
           'WHERE R.restaurant=:restaurant_id '
           'AND U.id=R.guest')
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchall()


def get_user_reservations(user_id):
    sql = ('SELECT id, date, startTime, pax, allergies, wishes, createdAt '
           'FROM reservations WHERE guest=:user_id')
    result = db.session.execute(sql, {'user_id': user_id})
    return result.fetchall()
