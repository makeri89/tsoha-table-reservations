# pylint: disable=import-error
from db import db


def add_restaurant(name, owner, address, openinghours, servicetimes):
    sql = ('INSERT INTO restaurants '
           '(name, owner, address, openingHours, serviceTimes) '
           'VALUES (:name, :owner, :address, :openingHours, :serviceTimes)')
    db.session.execute(sql, {
        'name': name,
        'owner': owner,
        'address': address,
        'openingHours': openinghours,
        'serviceTimes': servicetimes
    })
    db.session.commit()


def get_restaurant_info(restaurant_id):
    sql = 'SELECT * FROM restaurants WHERE id=:restaurant_id'
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchone()


def get_all_restaurants():
    sql = 'SELECT * FROM restaurants'
    result = db.session.execute(sql)
    return result.fetchall()


def get_restaurant_tables(restaurant_id):
    sql = 'SELECT * FROM tables WHERE restaurant=:restaurant_id'
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchall()


def get_restaurant_menus(restaurant_id):
    sql = 'SELECT * FROM menus WHERE restaurant=:restaurant_id'
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchall()


def get_restaurant_full_menus(restaurant_id):
    sql = ('SELECT M.menu, menus.name AS menuname, M.title, '
           'M.description, M.price, C.course '
           'FROM menuItems M, menuCourses C, menus WHERE '
           'M.menu IN (SELECT id FROM menus WHERE restaurant=:restaurant_id) '
           'and C.id=M.course AND menus.id=M.menu ORDER BY M.menu')
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchall()


def add_table(restaurant_id, size):
    sql = ('INSERT INTO tables (size, restaurant) '
           'VALUES (:size, :restaurant_id)')
    db.session.execute(sql, {'size': size, 'restaurant_id': restaurant_id})
    db.session.commit()


def get_capacity(restaurant_id):
    sql = ('SELECT size, COUNT(size) FROM tables '
           'WHERE restaurant=:restaurant_id '
           'GROUP BY size ORDER BY size')
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchall()


def get_available_capacity(restaurant_id, date, time, party_size):
    sql = ('SELECT id, size FROM tables WHERE restaurant=:restaurant_id '
           'AND NOT id IN (SELECT tableId FROM reservations '
           'WHERE date=:date AND startTime=:time) '
           'AND size >= :party_size ORDER BY size')
    result = db.session.execute(sql, {
        'restaurant_id': restaurant_id,
        'date': date, 'time': time,
        'party_size': party_size})
    return result.fetchall()


def remove_restaurant(restaurant_id):
    sql = 'DELETE FROM restaurants WHERE id=:restaurant_id'
    db.session.execute(sql, {'restaurant_id': restaurant_id})
    db.session.commit()


def get_menu_info(menu_id):
    sql = ('SELECT menus.name AS menuname, M.title, '
           'M.description, M.price, C.course '
           'FROM menuItems M, menuCourses C, menus WHERE '
           'C.id=M.course AND menus.id=:menu_id AND M.menu=:menu_id '
           'ORDER BY C.id')
    result = db.session.execute(sql, {'menu_id': menu_id})
    return result.fetchall()


def add_dish(title, description, price, menu, course):
    sql = ('INSERT INTO menuItems (title, description, price, menu, course) '
           'VALUES (:title, :description, :price, :menu, :course)')
    db.session.execute(sql, {
        'title': title,
        'description': description,
        'price': price,
        'menu': menu,
        'course': course})
    db.session.commit()


def add_menu(restaurant_id, name):
    sql = 'INSERT INTO menus (name, restaurant) VALUES (:name, :restaurant)'
    db.session.execute(sql, {'name': name, 'restaurant': restaurant_id})
    db.session.commit()


def find_owner(restaurant_id):
    sql = 'SELECT owner FROM restaurants WHERE id=:restaurant_id'
    result = db.session.execute(sql, {'restaurant_id': restaurant_id})
    return result.fetchone()[0]
