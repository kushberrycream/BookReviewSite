import os
from flask import Flask, render_template, url_for, session, redirect, request,\
    flash
from flask_pymongo import PyMongo
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
        if existing_user and existing_email is None:
            hashpass = bcrypt.hashpw(
                request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({
                'user': request.form['user'],
                'password': hashpass,
                'email': request.form['email']})
            session['user'] = request.form['user']
            flash('Successfully Signed Up!', 'register')

    return redirect(url_for('account', user=session['user']))

    if existing_user:
        flash('That username already exists! Try Again!', 'register')
        return redirect(url_for('homepage'))
    if existing_email:
        flash('That email already exists! Try Again!', 'register')
        return redirect(url_for('homepage'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('homepage'))


@app.route('/account/<user>', methods=['GET'])
def account(user):
    user = mongo.db.users.find_one({'user': session['user']})
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('account.html', user=user, posts=posts)


@app.route('/account/<user>/upload', methods=['POST'])
def profile_upload(user):
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
        mongo.db.users.find_one_and_update({
            'user': session['user']}, {
            "$set": {"profile_image": profile_image.filename}})

        return redirect(url_for('account', user=session['user']))


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
    books = mongo.db.books.find().sort("original_title", 1).limit(100)
    return render_template("books.html", books=books)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
