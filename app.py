import os
from datetime import datetime
from flask import Flask, render_template, url_for, session, redirect, request,\
    flash
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_parameter
from flask_toastr import Toastr
from bson.objectid import ObjectId
import bcrypt
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
toastr = Toastr(app)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
users = mongo.db.users
book = mongo.db.books1
review = mongo.db.reviews


@app.route("/")
@app.route("/home")
def homepage():
    return render_template("homepage.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_user = users.find_one({'user': request.form['user']})
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user[
            'password']) == login_user[
                'password']:
            session['user'] = request.form['user']
            flash('Welcome Back ' + session[
                'user'].capitalize() + '!', 'success')
            return redirect(url_for('account', user=session['user']))

    flash('Invalid username/password combination', "error")
    return redirect(url_for('homepage'))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
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
            flash('Successfully Signed Up!', 'success')
            return redirect(url_for('account', user=session['user']))

    return render_template('account.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('User logged out!', 'warning')
    return redirect(url_for('homepage'))


@app.route('/account/<user>')
def account(user):
    if session.get('user') is None:
        flash('You need to login!', 'warning')
        return redirect(url_for('homepage'))
    else:
        user = users.find_one({'user': session['user']})
        reviews = review.find({'user': session['user']}).sort('date', -1)
        return render_template('account.html', user=user, reviews=reviews)


@app.route('/account/<user>/upload', methods=['POST'])
def profile_upload(user):
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
        users.find_one_and_update({
            'user': session['user']}, {
            "$set": {"profile_image": profile_image.filename}})

        return redirect(url_for('account', user=session['user']))


@app.route('/account/<user>/delete', methods=['POST', 'GET'])
def delete_account(user):
    users.delete_one({'user': session['user']})
    session.pop('user', None)
    return redirect(url_for('homepage'))


@app.route('/user_uploads/<filename>')
def user_upload(filename):
    return mongo.send_file(filename)


@app.route('/account/<user>/edit_profile')
def edit_profile(user):
    user = users.find_one({'user': session['user']})
    return render_template('edit_profile.html', user=user)


@app.route('/account/<user>/user_details', methods=['POST'])
def user_details(user):
    users.find_one_and_update({'user': session['user']}, {
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
    if session.get('user') is None:
        flash('You need to login!', 'warning')
        return redirect(url_for('homepage'))
    else:
        user = users.find_one({'user': session['user']})
        search = False
        q = request.args.get('q')
        if q:
            search = True
        per_page = 50
        page = request.args.get(get_page_parameter(), type=int, default=1)
        books = book.find().sort(
            "title", 1).skip((page - 1) * per_page).limit(per_page)
        pagination = get_pagination(
            per_page=per_page, page=page, total=books.count(), search=search,
            record_name='books')
        return render_template(
            "books.html", user=user, books=books,
            pagination=pagination)


@app.route('/all_books/year')
def get_books_year():
    if session.get('user') is None:
        flash('You need to login!', 'warning')
        return redirect(url_for('homepage'))
    else:
        user = users.find_one({'user': session['user']})
        search = False
        q = request.args.get('q')
        if q:
            search = True
        per_page = 50
        page = request.args.get(get_page_parameter(), type=int, default=1)
        books = book.find().sort(
            "original_publication_year", 1).skip((
                page - 1) * per_page).limit(per_page)
        pagination = get_pagination(
            per_page=per_page,
            page=page,
            total=books.count(),
            search=search, record_name='books', format_total=True,
            format_number=True)

        return render_template(
            "books.html",
            user=user,
            books=books,
            pagination=pagination)


@app.route('/all_books/isbn')
def get_books_isbn():
    if session.get('user') is None:
        flash('You need to login!', 'warning')
        return redirect(url_for('homepage'))
    else:
        user = users.find_one({'user': session['user']})
        search = False
        q = request.args.get('q')
        if q:
            search = True
        per_page = 50
        page = request.args.get(get_page_parameter(), type=int, default=1)
        books = book.find().sort(
            "isbn", -1).skip((page - 1) * per_page).limit(per_page)
        pagination = get_pagination(
            per_page=per_page,
            page=page,
            total=books.count(),
            search=search, record_name='books', format_total=True,
            format_number=True)

        return render_template(
            "books.html",
            user=user,
            books=books,
            pagination=pagination)


@app.route('/all_books/delete', methods=['POST'])
def delete_book():
    book.find_one({'title': request.form['delete']})
    return redirect(url_for('get_books'))


@app.route('/all_books/edit_book/<book_id>', methods=['POST'])
def edit_book(book_id):
    books = book.find_one({'_id': ObjectId(book_id)})
    return render_template('edit_book.html', book=books)


@app.route(
    '/all_books/edit_book/<book_id>/updating_book', methods=['POST'])
def updating_book(book_id):
    book.find_one_and_update({'_id': ObjectId(book_id)}, {
                              '$set': {'title': request.form.get('title'),
                                       'authors': request.form.get('authors'),
                                       'isbn13': request.form.get('isbn'),
                                       'original_publication_year':
                                       request.form.get('year'),
                                       'language_code': request.form.get(
                                           'language'),
                                       'description': request.form.get(
                                           'description')}
                                       })

    flash('Successfully Updated Book!', 'success')

    return redirect(url_for('get_books'))


@app.route(
    '/all_books/add_review/<book_id>+<user_id>', methods=["POST"])
def add_review(book_id, user_id):
    books = book.find_one({'_id': ObjectId(book_id)})
    user = users.find_one({'_id': ObjectId(user_id)})

    return render_template('add_review.html', books=books, user=user)


@app.route(
    '/all_books/post_review/<book_id>+<user_id>', methods=["POST"])
def post_review(book_id, user_id):
    books = book.find_one({'_id': ObjectId(book_id)})
    user = users.find_one({'_id': ObjectId(user_id)})
    now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    now2 = datetime.now().timestamp()
    users.find_one_and_update({'_id': ObjectId(user_id)}, {
                             '$push': {'review': {
                                       'book_id': ObjectId(book_id),
                                       'book_image_url': books['image_url'],
                                       'book_title': books['title'],
                                       'book_author': books['authors'],
                                       'review': request.form.get('review'),
                                       'user_rating': request.form.get(
                                           'stars'),
                                       'time_of_post': now,
                                       'date': now2
                                       }}})
    book.find_one_and_update({'_id': ObjectId(book_id)}, {
                              '$set': {'description': request.form.get(
                                  'description')},
                              '$push': {'review': {
                                        'user_id': ObjectId(user_id),
                                        'user': session['user'],
                                        'review': request.form.get('review'),
                                        'user_rating': request.form.get(
                                            'stars'),
                                        'time_of_post': now,
                                        'date': now2
                                        }}})
    review.insert_one({'user_id': ObjectId(user_id),
                       'user': session['user'],
                       'user_image': user['profile_image'],
                       'book_id': ObjectId(book_id),
                       'book_image_url': books['image_url'],
                       'book_title': books['title'],
                       'book_author': books['authors'],
                       'review': request.form.get('review'),
                       'user_rating': request.form.get(
                       'stars'),
                       'time_of_post': now,
                       'date': now2
                       })

    flash('Review posted successfully!', 'success')
    return redirect(url_for('get_books'))


@app.route('/recent_reviews')
def recent_reviews():
    reviews = review.find().sort("date", -1)

    return render_template('recent_reviews.html', reviews=reviews)


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
