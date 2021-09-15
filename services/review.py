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
