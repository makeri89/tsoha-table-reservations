# pylint: disable=import-error
from db import db


def search(query):
    sql = ('SELECT id, name, address FROM restaurants '
           'WHERE LOWER(name) LIKE LOWER(:query)')
    result = db.session.execute(sql, {'query': f'%{query}%'})
    return result.fetchall()
