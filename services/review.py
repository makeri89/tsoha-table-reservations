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
    sql = ('SELECT RW.id, RE.name, RW.guest, '
           'RW.stars, RW.review, RW createdAt '
           'FROM reviews RW LEFT JOIN restaurants RE ON RW.restaurant=RE.id ')
    result = db.session.execute(sql)
    return result.fetchall()


def get_restaurant_reviews(restaurant_id):
    sql = ('SELECT RW.id, RE.name, RW.guest, '
           'RW.stars, RW.review, RW createdAt '
           'FROM reviews RW LEFT JOIN restaurants RE ON RW.restaurant=RE.id '
           'WHERE restaurant=:restaurant_id')
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchall()


def get_user_reviews(user_id):
    sql = ('SELECT RW.id, RE.name, RW.guest, '
           'RW.stars, RW.review, RW createdAt '
           'FROM reviews RW LEFT JOIN restaurants RE ON RW.restaurant=RE.id '
           'WHERE RW.guest=:user_id')
    result = db.session.execute(sql, {'user_id': user_id})
    return result.fetchall()


def get_review_average(restaurant_id):
    sql = ('SELECT AVG(stars), COUNT(stars) FROM reviews '
           'WHERE restaurant=:restaurant_id')
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchone()


def get_best_review(restaurant_id):
    sql = ('SELECT stars FROM reviews WHERE restaurant=:restaurant_id '
           'ORDER BY stars DESC LIMIT 1')
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchone()


def remove_review(review_id):
    sql = 'DELETE FROM reviews WHERE id=:review_id'
    db.session.execute(sql, {'review_id': review_id})
    db.session.commit()
