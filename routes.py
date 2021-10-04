from flask import render_template, request, redirect, Response
from app import app
from services.reservation import create_reservation
from services.user import (create_user, set_as_restaurant,
                           get_all_non_restaurant_users)
from services.restaurant import (get_restaurant_info,
                                 get_restaurant_menu,
                                 get_all_restaurants,
                                 get_available_capacity)
from services.search import search
from services.review import create_review
from services.auth import remove_tokens, password_check

all_restaurants = get_all_restaurants()


@app.route('/')
def index():
    return render_template('index.html', restaurants=get_all_restaurants())


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


@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        return render_template('review.html', restaurants=get_all_restaurants())
    if request.method == 'POST':
        restaurant = request.form['restaurant']
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
    menu = get_restaurant_menu(restaurant)
    return render_template('restaurant.html', restaurant=restaurant, menu=menu)


@app.route('/result')
def result():
    query = request.args['query']
    search_result = search(query)
    return render_template('result.html', results=search_result)


@app.route('/restaurants/reservation/<int:id>', methods=['GET'])
def reservation(id):
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
    restaurant_id = request.form['restaurant_id']
    date = request.form['date']
    time = request.form['time']
    pax = request.form['pax']
    allergies = request.form['allergies']
    wishes = request.form['wishes']
    create_reservation(restaurant_id, date, time, pax, allergies, wishes)
    return redirect('/user/reservations')


@app.route('/user/reservations')
def user_reservations():
    # TODO: implement this
    return redirect('/')


@app.route('/admin', methods=['GET'])
def admin():
    users = get_all_non_restaurant_users()
    return render_template('admin.html', users=users)


@app.route('/setasrestaurant', methods=['POST'])
def setasrestaurant():
    user_id = request.form['user']
    set_as_restaurant(user_id)
    return redirect('/admin')


@app.route('/teapot', methods=['GET'])
def teapot():
    return Response(status=418, response="<h1 style='text-align:center'>418. I'm a teapot!</h1>")
