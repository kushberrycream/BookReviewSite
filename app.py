import os
from flask import Flask, render_template, url_for, session, redirect, request,\
    flash
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
import bcrypt
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
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

        flash('That username already exists! Try Again!')
        return redirect(url_for('homepage'))

    return render_template('account.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('homepage'))


@app.route('/account/<user>')
def account(user):
    user = mongo.db.users.find_one({'user': session['user']})
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('account.html', user=user, posts=posts)


@app.route('/account/<user>/upload', methods=['POST'])
def profile_upload(user):
    target = os.path.join(APP_ROOT, 'static/profile-images/')
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'POST':
        users = mongo.db.users
        for upload in request.files.getlist("profile_image"):
            filename = secure_filename(upload.filename)
            destination = "/".join([target, filename])
            upload.save(destination)
            users.find_one_and_update({
                'user': session['user']}, {
                    "$set": {"profile_image": filename}})

        return redirect(url_for('account', user=session['user']))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
