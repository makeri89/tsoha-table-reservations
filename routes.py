from flask import render_template, request, redirect, Response
from app import app
from services.user import create_user, set_as_restaurant, get_all_non_restaurant_users
from services.restaurant import get_restaurant_info, get_restaurant_menu, get_all_restaurants
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


@app.route('/restaurants/reservation/<int:id>', methods=['GET', 'POST'])
def reservation(id):
    restaurant = get_restaurant_info(id)
    if request.method == 'GET':
        return render_template('reservation.html', restaurant=restaurant)
    if request.method == 'POST':
        pass


@app.route('/admin', methods=['GET'])
def admin():
    users = get_all_non_restaurant_users()
    print(users)
    return render_template('admin.html', users=users)


@app.route('/setasrestaurant', methods=['POST'])
def setasrestaurant():
    user_id = request.form['user']
    set_as_restaurant(user_id)
    return redirect('/admin')


@app.route('/teapot', methods=['GET'])
def teapot():
    return Response(status=418, response="<h1>418. I'm a teapot!</h1>")
