# pylint: disable=import-error
from flask import session
from werkzeug.security import check_password_hash
from db import db


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


def remove_tokens():
    del session['user_id']
    del session['username']
