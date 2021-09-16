# pylint: disable=import-error
from flask import session
from db import db


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

