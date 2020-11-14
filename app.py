"""This app implements CRUD operations with mongodb using flask and pymongo.

This website is a book review website which users can create an account,
upload a profile photo, upload books, add reviews to books and also
delete data they have entered. All functions are named accordingly and have
comments.

"""
import os
from datetime import datetime
from flask import (Flask, render_template, url_for, session, redirect, request,
                   flash)
from flask_paginate import get_page_parameter
from flask_pymongo import PyMongo
from flask_toastr import Toastr
from bson.objectid import ObjectId
import bcrypt
from functions import humanize_ts, isValid, login_required, get_pagination
if os.path.exists("env.py"):
    import env

# Initilizing Flask and Toastr
app = Flask(__name__)
toastr = Toastr(app)

# Enviroment Configuration, jinja extensions and filters, toastr configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.add_extension("jinja2.ext.loopcontrols")
app.jinja_env.filters["humanize"] = humanize_ts
app.config["TOASTR_POSITION_CLASS"] = "toast-top-full-width"
app.config["TOASTR_PREVENT_DUPLICATES"] = "true"

# Pass the Flask App to the pymongo() method
mongo = PyMongo(app)
users = mongo.db.users
book = mongo.db.books
review = mongo.db.reviews

# Creates Search index for search form on books.html
mongo.db.books.create_index(
    [
        ("title", "text"),
        ("authors", "text"),
    ],
    name="search_index",
    default_language="english",
    weights={
        "title": 100,
        "authors": 10
    }
)


@app.route("/")
@app.route("/home")
def homepage():
    """My Websites Homepage.

    Returns:
        renders template homepage.html
        
    """
    return render_template("homepage.html")


@app.route("/register", methods=["POST"])
def register():
    """Register an account on the website.

    URL used as form action attribute on the homepage register form,
    if request.method is POST then the form data is passed through various
    validations such as existing user, existing email, valid email using
    isvalid() function and then the passwords not matching, if all fail then
    the password it encoded and hashed. The form data is then inserted into the
    users database along with the hashed password and the username input is set
    to session['user']

    Returns:
        If existing_user found then you are redirected to the homepage with a
        user already exists Toastr message.
        If existing_email found then you are redirected to the homepage with a
        email already exists Toastr message.
        If email passed into isValid function is false then you are redirected
        to the homepage and an invalid email message.
        If both password inputs do not match then you are again redirected to
        the homepage and a passwords do not match message is displayed.
        If the above all fail then you are redirected to your new account page

    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one({"user": request.form["user"]})
        existing_email = mongo.db.users.find_one({
            "email": request.form["email"]})

        if existing_user:
            flash("That username already exists! Try Again!", "error")
            return redirect(url_for("homepage"))
        if existing_email:
            flash("That email already exists! Try Again!", "error")
            return redirect(url_for("homepage"))
        if isValid(request.form["email"]) is False:
            flash("Invalid Email", "error")
            return redirect(url_for("homepage"))
        if request.form["pass"] != request.form["pass2"]:
            flash("Passwords do not match!", "error")
            return redirect(url_for("homepage"))
        hashpass = bcrypt.hashpw(
            request.form["pass"].encode("utf-8"), bcrypt.gensalt()
        )
        mongo.db.users.insert(
            {
                "user": request.form["user"],
                "password": hashpass,
                "email": request.form["email"],
                "profile_image": ""
            }
        )
        session["user"] = request.form["user"]
        flash("Successfully Signed Up!", "success")
        return redirect(url_for("account", user=session["user"]))


@app.route("/login", methods=["POST"])
def login():
    """Login to the website.

    Used as the action attribute on login form on Login modal.
    When the login form is submitted the data is inserted into the database.

    Returns:
        If the users inputted username and password matches the password stored
        in the database then the user is redirected to their profile.
        If not then a Toastr error message is displayed and you stay on the
        homepage.

    """
    if request.method == "POST":
        login_user = mongo.db.users.find_one({"user": request.form["user"]})
        if login_user:
            if (bcrypt.hashpw(request.form["pass"].encode("utf-8"),
                              login_user["password"])
               == login_user["password"]):
                session["user"] = request.form["user"]
                flash("Welcome Back " + session["user"].capitalize() +
                      "!", "success")
                return redirect(url_for("account", user=session["user"]))
            else:
                flash("Invalid username/password combination", "error")
                return redirect(url_for("homepage"))


@app.route("/logout")
def logout():
    """Logout of website.

    Using session.pop the variable session['user'] is removed
    logging out the user and restricting access to some of the site.

    Returns:
        User is redirected to the homepage.

    """
    session.pop("user", None)
    flash("User logged out!", "warning")
    return redirect(url_for("homepage"))


@app.route("/account/<user>")
@login_required
def account(user):
    """ Users account page.

    Once an account has been created the user is able to display a profile
    page with any reviews they have posted or personal info. This uses the
    @login_required decorator to make sure the user is logged in.

    Args:
        user: The current user obtained via the session['user'] variable.

    Returns:
        if arg 'user' is equal to the session['user'] then the account page is
        displayed
        else an error message and the homepage are displayed, this stops users
        accessing other users accounts.

    """
    if user == session['user']:
        user = mongo.db.users.find_one({"user": session["user"]})
        reviews = review.find({"user": session["user"]}).sort("date", -1)
        return render_template("account.html", user=user, reviews=reviews)
    else:
        flash("Sorry thats is not your profile!", "error")
        return render_template("homepage.html")


@app.route("/account/<user>/upload", methods=["POST"])
def profile_image_upload(user):
    """ Upload profile photo to database.

    Used as the action attribute on the Photo upload form.
    When the form is submitted the photo chosen is uploaded to the user
    database within the document matching the session['user'].

    Args:
        user: The current user obtained via the session['user'] variable.

    Returns:
        redirects user back to the account page once successfully uploading
        a profile image.

    """
    if "profile_image" in request.files:
        profile_image = request.files["profile_image"]
        mongo.save_file(profile_image.filename, profile_image)
        mongo.db.users.find_one_and_update(
            {"user": session["user"]},
            {"$set": {"profile_image": profile_image.filename}})

        return redirect(url_for("account", user=session["user"]))


@app.route("/user_profile_images/<filename>")
def user_profile_images(filename):
    """ Access users uploaded profile images

    This is used as an img elements src, using url_for I open up the static
    folder and the relevant filename stored on the database.
    example: url_for('user_upload', filename=user['profile_image'])

    Returns:
        An instance of the response_class containing the named file, and
        implement conditional GET semantics (using make_conditional()).

    """
    return mongo.send_file(filename)


@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    """ Delete Book, User, Or Review Data.

    This is used as the action attribute on all delete buttons, once selected
    it checks if the ObjectId is in the books, user or reviews database!

    Args:
        id: dependent on which button is pressed either the User id, book id or
          review id is passed into the form displaying the appropriate delete
          page

    Returns:
        the delete page template is rendered with the relevant database
        connected.
    """
    if request.method == "POST":
        books = mongo.db.books.find_one({"_id": ObjectId(id)})
        user = mongo.db.users.find_one({"_id": ObjectId(id)})
        reviews = mongo.db.reviews.find_one({"_id": ObjectId(id)})
        return render_template("delete.html", book=books, user=user,
                               review=reviews)


@app.route("/account/delete/<user>/<review_id>", methods=["POST"])
@login_required
def delete_review(user, review_id):
    """ Delete a review from your account.

    On the users profile the user is able to delete reviews they have
    posted, it updates all linked databases and deletes all relevant
    info.

    Args:
        user: The current user obtained via the session['user'] variable.
        review_id: ObjectId passed from delete button located on account
        page.

    Returns:
        Once the delete button is selected the user is sent back to the
        account page

    """
    reviews = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    mongo.db.books.find_one_and_update(
        {"_id": ObjectId(reviews["book_id"])},
        {"$pull": {"reviews": {"review_id": ObjectId(review_id)}}})
    mongo.db.users.find_one_and_update(
        {"_id": ObjectId(reviews["user_id"])},
        {"$pull": {"reviews": {"review_id": ObjectId(review_id)}}})
    mongo.db.reviews.delete_one({"_id": ObjectId(review_id)})
    mongo.db.books.find_one_and_update(
        {"_id": ObjectId(reviews["book_id"])}, {"$inc": {"no_of_reviews": -1}})
    flash("Review Deleted!!!", "warning")
    return redirect(url_for("account", user=session["user"]))


@app.route("/account/delete/<user>", methods=["POST"])
def delete_account(user):
    """ Delete the Account from the website.

    The user is able to delete the whole account, it completely removed user 
    info from the site but does not delete the reviews they have posted.

    Args:
        user: The current user obtained via the session['user'] variable.

    Return:
        Once the users account is deleted they are redirected back to the
        homepage.

    """
    mongo.db.users.delete_one({"user": session["user"]})
    session.pop("user", None)
    flash("Account Deleted!!", "warning")
    return redirect(url_for("homepage"))


@app.route("/all_books/delete/<book_id>", methods=["POST"])
def delete_book(book_id):
    """ Delete a book from the website.

    If the user is the admin then they can delete all books, if the user
    uploaded the book then they are able to delete the book.

    Args:
        book_id: ObjectId passed from the delete button located on the books
        page.

    returns:
        Once the book has been deleted they are redirected to the all books /
        get books page.

    """
    book.delete_one({"_id": ObjectId(book_id)})
    flash("Book Deleted!!!", "warning")
    return redirect(url_for("get_books"))


@app.route("/account/<user>/edit_profile", methods=["POST"])
@login_required
def edit_profile(user):
    if user == session['user']:
        user = users.find_one({"user": user})
        return render_template("edit_profile.html", user=user)


@app.route("/account/<user>/user_details", methods=["POST"])
@login_required
def user_details(user):
    users.find_one_and_update(
        {"user": session["user"]},
        {
            "$set": {
                "first_name": request.form["firstName"].capitalize(),
                "last_name": request.form["lastName"].capitalize(),
                "age": request.form["age"],
                "gender": request.form["gender"],
                "email": request.form["email"],
                "favourite_book": request.form["fav-book"].capitalize(),
            }
        },
    )

    return redirect(url_for("account", user=session["user"]))


@app.route("/book/<book_id>")
def get_one_book(book_id):
    if ObjectId.is_valid(book_id):
        books = book.find_one({"_id": ObjectId(book_id)})
        if books is not None:
            return render_template("one_book.html", book=books)
        elif books == "null" or books is None:
            flash("Sorry this book does not exist", "warning")
            return render_template("homepage.html")
    else:
        flash("Sorry this book does not exist", "warning")
        return render_template("homepage.html")


@app.route("/all_books")
def get_books():
    per_page = 48
    page = request.args.get(get_page_parameter(), type=int, default=1)
    books = book.find().sort("title", 1).skip(
        (page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page, page=page, total=books.count(),
        record_name="books", format_total=True, format_number=True
    )
    return render_template("books.html", books=books,
                           pagination=pagination)


@app.route("/all_books/year")
def get_books_year():
    per_page = 48
    page = request.args.get(get_page_parameter(), type=int, default=1)
    books = book.find().sort("original_publication_year", -1).skip(
        (page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page, page=page, total=books.count(),
        record_name="books", format_total=True, format_number=True)

    return render_template("books.html", books=books,
                           pagination=pagination)


@app.route("/all_books/rating")
def get_books_rating():
    per_page = 48
    page = request.args.get(get_page_parameter(), type=int, default=1)
    books = book.find().sort(
        [("user_rating_average", -1), ("average_rating", -1)]).skip(
        (page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page, page=page, total=books.count(),
        record_name="books", format_total=True, format_number=True)

    return render_template("books.html", books=books,
                           pagination=pagination)


@app.route("/all_books/")
def get_books_search():
    per_page = 48
    search_form = request.args['search']
    page = request.args.get(get_page_parameter(), type=int, default=1)
    books = (book.find({"$text": {"$search": search_form}}).sort("title", 1)
             .skip((page - 1) * per_page).limit(per_page))
    pagination = get_pagination(
        per_page=per_page, page=page, total=books.count(),
        record_name="books", format_total=True, format_number=True)
    return render_template(
        "books.html", books=books, pagination=pagination)


@app.route("/all_books/edit_book/<book_id>", methods=["POST"])
@login_required
def edit_book(book_id):
    books = book.find_one({"_id": ObjectId(book_id)})
    return render_template("edit_book.html", book=books)


@app.route("/all_books/edit_book/<book_id>/updating_book", methods=["POST"])
def updating_book(book_id):
    book.find_one_and_update(
        {"_id": ObjectId(book_id)},
        {"$set": {"title": request.form.get("title"),
                  "authors": request.form.get("authors"),
                  "isbn13": request.form.get("isbn"),
                  "original_publication_year": request.form.get("year"),
                  "description": request.form.get("description")
                  }},)
    if request.form.get('url') == "":
        book.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {"$set": {
                "image_url": ("https://cdn.bookauthority.org/dist/images/"
                              "book-cover-not-available.6b5a104fa66be4eec"
                              "4fd16aebd34fe04.png")
            }},)
    elif request.form.get('url') is not None:
        book.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {"$set": {
                "image_url": request.form.get("url")
            }},)
    flash("Successfully Updated Book!", "success")
    return redirect(url_for("get_one_book", book_id=book_id))


@app.route("/all_books/add_book")
@login_required
def add_book():
    return render_template("add_book.html")


@app.route("/all_books/posting_book", methods=["POST"])
def post_book():
    now = datetime.now().timestamp()
    book.insert_one(
        {
            "isbn13": request.form.get("isbn"),
            "title": request.form.get("title"),
            "authors": request.form.get("authors"),
            "original_publication_year": request.form.get("year"),
            "description": request.form.get("description"),
            "image_url": request.form.get("image"),
            "posted_by": session['user'],
            "time_added": now})
    book_id = book.find_one({"title": request.form.get("title")})

    return redirect(url_for("get_one_book", book_id=book_id["_id"]))


@app.route("/all_books/add_review/<book_id>", methods=["POST"])
@login_required
def add_review(book_id):
    user = users.find_one({"user": session["user"]})
    if user["profile_image"] == "":
        flash("Please Upload A Profile Photo!", "error")
        return redirect(url_for("account", user=session["user"]))
    if request.method == "POST":
        existing_review = book.find_one(
            {"_id": ObjectId(book_id), "reviews.user": session["user"]})
        if existing_review:
            flash("You have already reviewed this book please \
                  Edit your original post", "error")
            return redirect(url_for("account", user=session["user"]))
        if existing_review is None:
            books = book.find_one({"_id": ObjectId(book_id)})
            user = users.find_one({"user": session["user"]})
        return render_template("add_review.html", books=books, user=user)


@app.route("/all_books/edit_review/<book_id>", methods=["POST"])
@login_required
def edit_review(book_id):
    books = book.find_one({"_id": ObjectId(book_id)})
    user = users.find_one({"user": session["user"]})

    return render_template("edit_review.html", books=books, user=user)


@app.route("/all_books/update_review/<book_id>", methods=["POST"])
@login_required
def update_review(book_id):
    books = book.find_one({
        "_id": ObjectId(book_id), "reviews.user": session["user"]})
    user = users.find_one({"user": session["user"]})
    reviews = review.find_one({
        "book_id": ObjectId(book_id), "user": session["user"]})
    now = datetime.now().timestamp()
    review.find_one_and_update(
        {"user_id": ObjectId(user["_id"]), "book_id": ObjectId(book_id)},
        {"$set": {
            "user_id": ObjectId(user["_id"]),
            "user": session["user"],
            "user_image": user["profile_image"],
            "book_id": ObjectId(book_id),
            "book_image_url": books["image_url"],
            "book_title": books["title"],
            "book_author": books["authors"],
            "review": request.form.get("review"),
            "user_rating": int(request.form.get("stars")),
            "recommended": request.form.get("recommend"),
            "date": now}})
    users.find_one_and_update(
        {"_id": ObjectId(user["_id"]),
         "reviews.review_id": ObjectId(reviews["_id"])},
        {"$set": {"reviews.$": {
                  "review_id": ObjectId(reviews["_id"]),
                  "book_id": ObjectId(book_id)}}})
    book.find_one_and_update(
        {"_id": ObjectId(book_id),
         "reviews.review_id": ObjectId(reviews["_id"])},
        {"$set": {"reviews.$": {
                  "review_id": ObjectId(reviews["_id"]),
                  "user_id": ObjectId(user["_id"]),
                  "user": session["user"],
                  "user_image": user["profile_image"],
                  "review": request.form.get("review"),
                  "user_rating": int(request.form.get("stars")),
                  "recommended": request.form.get("recommend"),
                  "date": now}}})
    pipeline = [
        {"$addFields": {
            "user_rating_average": {"$toDecimal": {
                "$avg": "$reviews.user_rating"}}}}, {
                "$out": "books"}
    ]
    book.aggregate(pipeline)

    flash("Review edited successfully!", "success")
    return redirect(url_for("account", user=session["user"]))


@app.route("/all_books/post_review/<book_id>", methods=["POST"])
def post_review(book_id):
    books = book.find_one({"_id": ObjectId(book_id)})
    user = users.find_one({"user": session["user"]})
    now = datetime.now().timestamp()
    review.insert_one(
        {"user_id": ObjectId(user["_id"]),
         "user": session["user"],
         "user_image": user["profile_image"],
         "book_id": ObjectId(book_id),
         "book_image_url": books["image_url"],
         "book_title": books["title"],
         "book_author": books["authors"],
         "review": request.form.get("review"),
         "user_rating": int(request.form.get("stars")),
         "recommended": request.form.get("recommend"),
         "date": now})
    reviews = review.find_one(
        {"user_id": ObjectId(user["_id"]),
         "book_id": ObjectId(book_id)})
    users.find_one_and_update(
        {"_id": ObjectId(user["_id"])},
        {"$push": {"reviews": {
                   "review_id": ObjectId(reviews["_id"]),
                   "book_id": ObjectId(book_id)}}})
    book.find_one_and_update(
        {"_id": ObjectId(book_id)},
        {"$push": {"reviews": {
                   "review_id": ObjectId(reviews["_id"]),
                   "user_id": ObjectId(user["_id"]),
                   "user": session["user"],
                   "user_image": user["profile_image"],
                   "review": request.form.get("review"),
                   "user_rating": int(request.form.get("stars")),
                   "recommended": request.form.get("recommend"),
                   "date": now}}})
    book.find_one_and_update(
        {"_id": ObjectId(book_id)}, {"$inc": {"no_of_reviews": 1}})

    pipeline = [
        {"$addFields": {
            "user_rating_average": {"$toDecimal": {
                "$avg": "$reviews.user_rating"}}}}, {
                "$out": "books"}
    ]
    book.aggregate(pipeline)

    flash("Review posted successfully!", "success")
    return redirect(url_for("get_one_book", book_id=book_id))


@app.route("/all_reviews")
def all_reviews():
    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    reviews = review.find().sort("date", -1).skip(
        (page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page, page=page, total=reviews.count(),
        record_name="reviews", format_total=True, format_number=True
    )
    return render_template(
        "all_reviews.html", reviews=reviews, pagination=pagination)


@app.route("/recommendations")
def recommendations():
    five_star = (
        review.find({"user_rating": 5}).sort(
            "date", -1).limit(5))
    four_star = (
        review.find({"user_rating": 4}).sort(
            "date", -1).limit(5))
    recommended = (
        review.find(
            {"recommended": "yes"})
        .sort("date", -1).limit(5))

    return render_template(
        "recommendations.html",
        five_star=five_star,
        four_star=four_star,
        recommended=recommended)


@app.errorhandler(405)
def method_not_allowed(e):
    flash("Sorry you cannot do that!", "error")
    return render_template("homepage.html"), 405


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")), debug=True)
