from flask import session


def remove_tokens():
    del session['user_id']
    del session['username']
