from flask import render_template, request, redirect
from app import app
from services import create_review, create_user, get_restaurant_info, get_restaurant_menu, password_check, remove_tokens, get_all_restaurants, search


@app.route('/')
def index():
    all_restaurants = get_all_restaurants()
    return render_template('index.html', restaurants=all_restaurants)


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
        return render_template('review.html')
    if request.method == 'POST':
        test_restaurant = 'TestiRavintola'
        stars = request.form['stars']
        review_text = request.form['review-text']
        create_review(test_restaurant, stars, review_text)
        return redirect('/')


@app.route('/restaurants/<int:id>')
def restaurants(id):
    restaurant = get_restaurant_info(id)
    menu = get_restaurant_menu(restaurant)
    return render_template('restaurant.html', restaurant=restaurant, menu=menu)


@app.route('/result')
def result():
    query = request.args['query']
    search_result = search(query)
    return render_template('result.html', results=search_result)
