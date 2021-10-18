# pylint: disable=import-error
import secrets
from flask import session, abort
from werkzeug.security import check_password_hash
from db import db


def password_check(username, password):
    sql = 'SELECT id, password FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session['user_id'] = user.id
        session['username'] = username
        session['csrf_token'] = secrets.token_hex(16)
        return True
    return False


def remove_tokens():
    del session['user_id']
    del session['username']
    del session['csrf_token']


def check_csrf(token):
    if session['csrf_token'] != token:
        abort(403)
