# pylint: disable=import-error
from services.user import current_user
from db import db


def create_review(restaurant_id, stars, review):
    sql = ('INSERT INTO reviews '
           '(restaurant, guest, stars, review, createdAt) '
           'VALUES '
           '(:restaurant, :guest, :stars, :review, NOW())')
    db.session.execute(sql, {
        'restaurant': restaurant_id,
        'guest': current_user().id,
        'stars': stars,
        'review': review
    })
    db.session.commit()


def get_all_reviews():
    sql = 'SELECT * FROM reviews'
    result = db.session.execute(sql)
    return result.fetchall()


def get_restaurant_reviews(restaurant_id):
    sql = 'SELECT * FROM reviews WHERE restaurant=:restaurant_id'
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchall()


def get_user_reviews(user_id):
    sql = 'SELECT R.*, RE.id AS rest_id, RE.name AS rest_name FROM reviews R, restaurants RE WHERE guest=:user_id AND R.restaurant=RE.id'
    result = db.session.execute(sql, {'user_id': user_id})
    return result.fetchall()
