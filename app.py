import os
from flask import Flask, render_template, url_for, session, redirect, request,\
    flash
from flask_pymongo import PyMongo

from flask_paginate import Pagination, get_page_parameter
from bson.objectid import ObjectId
from bson.code import Code
import bcrypt
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def homepage():

    return render_template("homepage.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'user': request.form['user']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user[
            'password']) == login_user[
                'password']:
            session['user'] = request.form['user']

            return redirect(url_for('account', user=session['user']))

    flash('Invalid username/password combination', "failed")
    return redirect(url_for('homepage'))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'user': request.form['user']})
        existing_email = users.find_one({'email': request.form['email']})

        if existing_user:
            flash('That username already exists! Try Again!', 'register')
            return redirect(url_for('homepage'))
        if existing_email:
            flash('That email already exists! Try Again!', 'register')
            return redirect(url_for('homepage'))

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({
                'user': request.form['user'],
                'password': hashpass,
                'email': request.form['email']})
            session['user'] = request.form['user']
            flash('Successfully Signed Up!')
            return redirect(url_for('account', user=session['user']))

    return render_template('account.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('homepage'))


@app.route('/account/<user>', methods=['GET'])
def account(user):
    user = mongo.db.users.find_one({'user': session['user']})
    reviews = mongo.db.reviews.find({'username': session['user']})
    return render_template('account.html', user=user, reviews=reviews)


@app.route('/account/<user>/upload', methods=['POST'])
def profile_upload(user):
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
        mongo.db.users.find_one_and_update({
            'user': session['user']}, {
            "$set": {"profile_image": profile_image.filename}})

        return redirect(url_for('account', user=session['user']))


@app.route('/account/<user>/delete', methods=['POST', 'GET'])
def delete_account(user):
    mongo.db.users.delete_one({'user': session['user']})
    session.pop('user', None)
    return redirect(url_for('homepage'))


@app.route('/user_uploads/<filename>')
def user_upload(filename):
    return mongo.send_file(filename)


@app.route('/account/<user>/edit_profile')
def edit_profile(user):
    user = mongo.db.users.find_one({'user': session['user']})

    return render_template('edit_profile.html', user=user)


@app.route('/account/<user>/user_details', methods=['POST'])
def user_details(user):
    mongo.db.users.find_one_and_update({'user': session['user']}, {
        "$set": {
            "first_name": request.form['firstName'].capitalize(),
            "last_name": request.form['lastName'].capitalize(),
            "age": request.form['age'],
            "gender": request.form['gender'],
            "email": request.form['email'],
            "favourite_book": request.form['fav-book'].capitalize()}})

    return redirect(url_for('account', user=session['user']))


@app.route('/all_books')
def get_books():
    user = mongo.db.users.find()
    reviews = mongo.db.reviews.find()
    search = False
    q = request.args.get('q')
    if q:
        search = True
        per_page = 100
        page = request.args.get(get_page_parameter(), type=int, default=1)

        books = mongo.db.books.find().sort(
            "original_title", 1).skip((page - 1) * per_page).limit(per_page)
        pagination = get_pagination(
            per_page=per_page,
            page=page,
            total=books.count(),
            search=search, record_name='books', format_total=True,
            format_number=True)

    return render_template(
        "books.html",
        user=user,
        reviews=reviews,
        books=books,
        pagination=pagination)


@app.route('/all_books/year')
def get_books_year():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    per_page = 100
    page = request.args.get(get_page_parameter(), type=int, default=1)

    books = mongo.db.books.find().sort(
        "original_publication_year", -1).skip((
            page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page,
        page=page,
        total=books.count(),
        search=search, record_name='books', format_total=True,
        format_number=True)

    return render_template(
        "books.html",
        books=books,
        pagination=pagination)


@app.route('/all_books/isbn')
def get_books_isbn():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    per_page = 100
    page = request.args.get(get_page_parameter(), type=int, default=1)

    books = mongo.db.books.find().sort(
        "isbn", -1).skip((
            page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page,
        page=page,
        total=books.count(),
        search=search, record_name='books', format_total=True,
        format_number=True)

    return render_template(
        "books.html",
        books=books,
        pagination=pagination)


@app.route('/all_books/id')
def get_books_id():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    per_page = 100
    page = request.args.get(get_page_parameter(), type=int, default=1)

    books = mongo.db.books.find().sort(
        "book_id", 1).skip((
            page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page,
        page=page,
        total=books.count(),
        search=search, record_name='books', format_total=True,
        format_number=True)

    return render_template(
        "books.html",
        books=books,
        pagination=pagination)


@app.route('/all_books/delete', methods=['POST', 'GET'])
def delete_book():
    mongo.db.books.delete_one({'authors': request.form['delete']})
    return redirect(url_for('get_books'))


@app.route('/all_books/edit_book/<book_name>', methods=['POST', 'GET'])
def edit_book(book_name):
    the_book = mongo.db.books.find_one({'original_title': book_name})
    book_name.replace(" ", "_")

    return render_template('edit_book.html', book=the_book)


@app.route(
    '/all_books/add_review/<user_id>+<book_id>', methods=["POST"])
def add_review(user_id, book_id):
    book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    reviews = mongo.db.reviews
    print(book)
    reviews.insert_one({
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id),
        'book_image_url': book['image_url'],
        'book_title': book['original_title'],
        'book_author': book['authors'],
        'user_image': user['profile_image'],
        'username': session['user'],
        'review': request.form.get('review'),
        'stars': request.form.get('stars')
        })

    return redirect(url_for('get_books'))


def get_css_framework():
    return app.config.get('CSS_FRAMEWORK', 'bootstrap4')


def get_link_size():
    return app.config.get('LINK_SIZE', 'md')


def show_single_page_or_not():
    return app.config.get('SHOW_SINGLE_PAGE', False)


def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'books')
    return Pagination(
        css_framework=get_css_framework(),
        link_size=get_link_size(),
        show_single_page=show_single_page_or_not(), **kwargs)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
