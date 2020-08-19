import os
from flask import Flask, render_template, url_for, session, redirect, request,\
    flash, current_app, get_flashed_messages
from flask_pymongo import PyMongo
from jinja2 import Markup, Template
from flask_paginate import Pagination, get_page_parameter
from bson.objectid import ObjectId
import bcrypt
if os.path.exists("env.py"):
    import env
from flask_toastr import Toastr


app = Flask(__name__)
toastr = Toastr(app)

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
            flash('Welcome Back ' + session['user'].capitalize() + '!', 'success')
            return redirect(url_for('account', user=session['user']))

    flash('Invalid username/password combination', "error")
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
            flash('Successfully Signed Up!', 'success')
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
    if session.get('user') is None:
        flash('You need to login!', 'warning')
        return redirect(url_for('homepage'))
    else:
        user = mongo.db.users.find_one({'user': session['user']})
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
    if session.get('user') is None:
        flash('You need to login!', 'warning')
        return redirect(url_for('homepage'))
    else:
        user = mongo.db.users.find_one({'user': session['user']})
        reviews = mongo.db.reviews.find()
        search = False
        q = request.args.get('q')
        if q:
            search = True
        per_page = 100
        page = request.args.get(get_page_parameter(), type=int, default=1)
        books = mongo.db.books.find().sort(
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
            reviews=reviews,
            books=books,
            pagination=pagination)


@app.route('/all_books/isbn')
def get_books_isbn():
    if session.get('user') is None:
        flash('You need to login!', 'warning')
        return redirect(url_for('homepage'))
    else:
        user = mongo.db.users.find_one({'user': session['user']})
        reviews = mongo.db.reviews.find()
        search = False
        q = request.args.get('q')
        if q:
            search = True
        per_page = 100
        page = request.args.get(get_page_parameter(), type=int, default=1)
        books = mongo.db.books.find().sort(
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
            reviews=reviews,
            books=books,
            pagination=pagination)


@app.route('/all_books/id')
def get_books_id():
    if session.get('user') is None:
        flash('You need to login!', 'warning')
        return redirect(url_for('homepage'))
    else:
        user = mongo.db.users.find_one({'user': session['user']})
        reviews = mongo.db.reviews.find()
        search = False
        q = request.args.get('q')
        if q:
            search = True
        per_page = 100
        page = request.args.get(get_page_parameter(), type=int, default=1)
        books = mongo.db.books.find().sort(
            "id", 1).skip((page - 1) * per_page).limit(per_page)
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


class _toastr(object):
    @staticmethod
    def include_toastr_js(version=None, js_filename=None):
        if version is None:
            version = current_app.config.get('TOASTR_VERSION')
        if js_filename is None:
            js_filename = current_app.config.get('TOASTR_JS_FILENAME')
        js = '<script src="//cdnjs.cloudflare.com/ajax/libs/' \
             'toastr.js/%s/%s"></script>\n' % (version, js_filename)
        return Markup(js)

    @staticmethod
    def include_toastr_css(version=None, css_filename=None):
        if version is None:
            version = current_app.config.get('TOASTR_VERSION')
        if css_filename is None:
            css_filename = current_app.config.get('TOASTR_CSS_FILENAME')
        css = '<link href="//cdnjs.cloudflare.com/ajax/libs/' \
              'toastr.js/%s/%s" rel="stylesheet" />\n' % (
                  version, css_filename)
        if current_app.config.get('TOASTR_OPACITY'):
            return Markup(css)
        else:
            return Markup('''
<style type = text/css>
  #toast-container>div {
    opacity: 1 !important;
  }
</style> %s''' % css)

    @staticmethod
    def message():
        toastr_options = 'toastr.options.closeButton = %s; \
        toastr.options.timeOut = %s; \
        toastr.options.extendedTimeOut = %s; \
        toastr.options.positionClass = \"%s\"; \
        toastr.options.preventDuplicates = %s; \
        toastr.options.newestOnTop = %s; \
        toastr.options.progressBar = %s; ' % (
            current_app.config.get('TOASTR_CLOSE_BUTTON'),
            current_app.config.get('TOASTR_TIMEOUT'),
            current_app.config.get('TOASTR_EXTENDED_TIMEOUT'),
            current_app.config.get('TOASTR_POSITION_CLASS'),
            current_app.config.get('TOASTR_PREVENT_DUPLICATES'),
            current_app.config.get('TOASTR_NEWS_ON_TOP'),
            current_app.config.get('TOASTR_PROGRESS_BAR'))
        message = Template('''
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <script type="text/javascript">
      (function($) {
        $(document).ready(function() {
          {{ toastr_options }}
          {% for category, message in messages %}
            {% if category is undefined or category == 'message' %}
              toastr.info(\'{{ message }}\')
            {% else %}
              toastr.{{ category }}(\'{{ message }}\')
            {% endif %}
          {% endfor %}
        });
      })(jQuery);
    </script>
  {% endif %}
{% endwith %}
''')
        return Markup(render_template(message,
                      get_flashed_messages=get_flashed_messages,
                      toastr_options=toastr_options))


class Toastr(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['toastr'] = _toastr
        app.context_processor(self.context_processor)

        app.config.setdefault('TOASTR_VERSION', '2.1.4')
        app.config.setdefault('TOASTR_JQUERY_VERSION', '2.1.0')
        app.config.setdefault('TOASTR_CSS_FILENAME', 'toastr.min.css')
        app.config.setdefault('TOASTR_JS_FILENAME', 'toastr.min.js')

        app.config.setdefault('TOASTR_CLOSE_BUTTON', 'true')
        app.config.setdefault('TOASTR_TIMEOUT', 10000)
        app.config.setdefault('TOASTR_EXTENDED_TIMEOUT', 1000)
        app.config.setdefault('TOASTR_POSITION_CLASS', 'toast-top-full-width')
        app.config.setdefault('TOASTR_PREVENT_DUPLICATES', 'false')
        app.config.setdefault('TOASTR_NEWS_ON_TOP', 'false')
        app.config.setdefault('TOASTR_PROGRESS_BAR', 'true')
        app.config.setdefault('TOASTR_OPACITY', True)

    @staticmethod
    def context_processor():
        return {
            'toastr': current_app.extensions['toastr']
        }

    def create(self, timestamp=None):
        return current_app.extensions['toastr'](timestamp)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
