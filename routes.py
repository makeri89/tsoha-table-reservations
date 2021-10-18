from flask import render_template, request, redirect, Response, url_for

from app import app
from utils.format import format_to_psql_array
from services.reservation import create_reservation, get_user_reservations
from services.search import search
from services.review import (create_review, get_best_review,
                             get_restaurant_reviews, get_review_average,
                             get_user_reviews, remove_review)
from services.auth import remove_tokens, password_check, check_csrf
from services.user import (create_user,
                           set_as_restaurant,
                           get_all_users,
                           get_all_non_restaurant_users,
                           is_admin,
                           remove_user,
                           current_user,
                           is_restaurant,
                           get_user_restaurants)
from services.restaurant import (add_restaurant, get_restaurant_info,
                                 get_all_restaurants, add_dish, add_table,
                                 get_available_capacity, get_restaurant_menus,
                                 remove_restaurant, get_menu_info, add_menu,
                                 find_owner)

all_restaurants = get_all_restaurants()


@app.route('/')
def index():
    admin_info = is_admin()
    return render_template('index.html', restaurants=get_all_restaurants(), admin=admin_info)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        create_user(firstname, lastname, email, username, password)
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password_check(username, password):
            return redirect('/')
        return redirect('/login')


@app.route('/logout')
def logout():
    remove_tokens()
    return redirect('/')


@app.route('/review/<int:id>', methods=['GET', 'POST'])
def review(id):
    restaurant_info = get_restaurant_info(id)
    if request.method == 'GET':
        return render_template('review.html', restaurant=restaurant_info)
    if request.method == 'POST':
        check_csrf(request.form['csrf_token'])
        restaurant = restaurant_info.id
        stars = request.form['stars']
        review_text = request.form['review-text']
        create_review(restaurant, stars, review_text)
        return redirect('/')


@app.route('/restaurants', defaults={'id': None})
@app.route('/restaurants/<int:id>')
def restaurants(id):
    if id is None:
        return redirect('/')
    restaurant = get_restaurant_info(id)
    menus = get_restaurant_menus(restaurant.id)
    average_reviews = get_review_average(restaurant.id)
    best_review = get_best_review(restaurant.id)
    return render_template('restaurant.html', restaurant=restaurant,
                           menus=menus, average_reviews=average_reviews,
                           best_review=best_review)


@app.route('/result')
def result():
    query = request.args['query']
    search_result = search(query)
    return render_template('result.html', results=search_result)


@app.route('/restaurants/reservation/<int:id>', methods=['GET'])
def reservation(id):
    if not current_user():
        return redirect(url_for('login', error='Please log in first!'))
    restaurant = get_restaurant_info(id)
    return render_template('reservation.html', restaurant=restaurant, error=0)


@app.route('/restaurants/reservation/<int:id>/fail', methods=['GET'])
def failed_reservation(id):
    restaurant = get_restaurant_info(id)
    return render_template('reservation.html', restaurant=restaurant, error=1)


@app.route('/restaurants/reservation/<int:id>/confirm', methods=['GET', 'POST'])
def confirm(id):
    restaurant_id = id
    pax = request.args['pax']
    date = request.args['date']
    time = request.args['starttime']
    if len(get_available_capacity(restaurant_id, date, time, pax)) > 0:
        restaurant = get_restaurant_info(id)
        return render_template('confirmation.html',
                               restaurant=restaurant,
                               date=date, time=time, pax=pax)
    return redirect('/restaurants/reservation/'+str(id)+'/fail')


@app.route('/reserve', methods=['POST'])
def reserve():
    check_csrf(request.form['csrf_token'])
    restaurant_id = request.form['restaurant_id']
    date = request.form['date']
    time = request.form['time']
    pax = request.form['pax']
    allergies = request.form['allergies']
    wishes = request.form['wishes']
    create_reservation(restaurant_id, date, time, pax, allergies, wishes)
    return redirect('/user')


@app.route('/user', methods=['GET'])
def user_page():
    user = current_user()
    if not user:
        return redirect('/login')
    all_reviews = get_user_reviews(user.id)
    reservations = get_user_reservations(user.id)
    restaurant_status = is_restaurant()
    user_restaurants = get_user_restaurants(user.id)
    return render_template('user.html', user=user,
                           reviews=all_reviews, reservations=reservations,
                           restaurant_status=restaurant_status,
                           restaurants=user_restaurants)


@app.route('/admin', methods=['GET'])
def admin():
    if is_admin():
        users = get_all_users()
        non_restaurant_users = get_all_non_restaurant_users()
        return render_template('admin.html', users=users,
                               non_restaurant_users=non_restaurant_users,
                               restaurants=all_restaurants)
    return render_template('unauthorized.html')


@app.route('/setasrestaurant', methods=['POST'])
def setasrestaurant():
    user_id = request.form['user']
    set_as_restaurant(user_id)
    return redirect('/admin')


@app.route('/deleteuser', methods=['POST'])
def delete_user():
    if is_admin():
        user_id = request.form['user']
        remove_user(user_id)
        return redirect('/admin')
    return render_template('unauthorized.html')


@app.route('/deleterestaurant', methods=['POST'])
def delete_restaurant():
    user = current_user()
    restaurant_id = request.form['restaurant']
    admin_status = is_admin()
    rest_owner = find_owner(restaurant_id)
    if admin_status or rest_owner == user.id:
        remove_restaurant(restaurant_id)
        if admin_status:
            return redirect('/admin')
        return redirect('/user')
    return render_template('unauthorized.html')


@app.route('/restaurants/<int:id>/admin', methods=['GET'])
def restaurantadmin(id):
    if is_restaurant():
        restaurant_info = get_restaurant_info(id)
        menus = get_restaurant_menus(id)
        return render_template('restaurantadmin.html',
                               restaurant=restaurant_info, menus=menus)
    return render_template('unauthorized.html')


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>',
           methods=['GET'])
def show_menu(restaurant_id, menu_id):
    restaurant_info = get_restaurant_info(restaurant_id)
    menu_info = get_menu_info(menu_id)
    return render_template('menu.html',
                           restaurant=restaurant_info, menu=menu_info)


@app.route('/newrestaurant', methods=['GET', 'POST'])
def newrestaurant():
    if is_restaurant():
        if request.method == 'GET':
            return render_template('newrestaurant.html')
        if request.method == 'POST':
            name = request.form['name']
            address = request.form['address']
            weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            openinghours = [[i, request.form[i],  request.form[i+'close']]
                            for i in weekdays]
            openinghours = format_to_psql_array(openinghours)
            servicetimes = [[i] for i in weekdays]
            for _ in range(10):
                for j in servicetimes:
                    j.append('-')
            for i, value in enumerate(weekdays):
                data = request.form[value+'-servicetimes'].split(';')
                for j, val in enumerate(data):
                    servicetimes[i][j+1] = val
            servicetimes = format_to_psql_array(servicetimes)
            owner = current_user().id
            add_restaurant(name, owner, address, openinghours, servicetimes)
            return redirect('/user')
    return render_template('unauthorized.html')


@app.route('/adddish', methods=['POST'])
def adddish():
    menu_id = request.form['menu']
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    course = request.form['course']
    if is_restaurant():
        add_dish(title, description, price, menu_id, course)
        return redirect('/user')
    return render_template('unauthorized.html')


@app.route('/addtable', methods=['POST'])
def addtable():
    if is_restaurant():
        restaurant_id = request.form['restaurant']
        size = request.form['size']
        amount = request.form['amount']
        for _ in range(int(amount)):
            add_table(restaurant_id, size)
        return redirect('/user')
    return render_template('unauthorized.html')


@app.route('/addmenu', methods=['POST'])
def addmenu():
    if is_restaurant():
        restaurant_id = request.form['restaurant'].replace('/', '')
        name = request.form['name']
        add_menu(restaurant_id, name)
        return redirect(f'/restaurants/{restaurant_id}/admin')
    return render_template('unauthorized.html')


@app.route('/reviews/<int:id>', methods=['GET'])
def reviews(id):
    all_reviews = get_restaurant_reviews(id)
    admin_status = is_admin()
    return render_template('reviews.html', reviews=all_reviews, admin=admin_status)


@app.route('/deletereview/<int:id>', methods=['POST'])
def delete_review(id):
    if is_admin():
        remove_review(id)
        return redirect('/')
    return render_template('unauthorized.html')


@app.route('/teapot', methods=['GET'])
def teapot():
    return Response(status=418, response="<h1 style='text-align:center'>418. I'm a teapot!</h1>")
