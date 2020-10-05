import os
from datetime import datetime, timedelta
from flask import (Flask, render_template, url_for, session, redirect, request,
                   flash)
from flask_paginate import get_page_parameter
from flask_pymongo import PyMongo
from flask_toastr import Toastr
from bson.objectid import ObjectId
import bcrypt
from classes import humanize_ts, isValid, login_required, get_pagination

if os.path.exists("env.py"):
    import env


app = Flask(__name__)
toastr = Toastr(app)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost")
app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.add_extension("jinja2.ext.loopcontrols")
app.jinja_env.filters["humanize"] = humanize_ts
app.config["TOASTR_POSITION_CLASS"] = "toast-top-full-width"

mongo = PyMongo(app)
users = mongo.db.users
book = mongo.db.books1
review = mongo.db.reviews

book.create_index(
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
    return render_template("homepage.html")


@app.route("/login", methods=["POST"])
def login():
    login_user = users.find_one({"user": request.form["user"]})
    if login_user:
        if (bcrypt.hashpw(request.form["pass"].encode("utf-8"),
            login_user["password"])
                == login_user["password"]):
            session["user"] = request.form["user"]
            flash("Welcome Back " + session["user"].capitalize() +
                  "!", "success")

            return redirect(url_for("homepage"))
    flash("Invalid username/password combination", "error")
    return redirect(url_for("homepage"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("User logged out!", "warning")
    return redirect(url_for("homepage"))


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        existing_user = users.find_one({"user": request.form["user"]})
        existing_email = users.find_one({"email": request.form["email"]})
        user_len = len(request.form.get("user"))

        if existing_user:
            flash("That username already exists! Try Again!", "register")
            return redirect(url_for("homepage"))
        if existing_email:
            flash("That email already exists! Try Again!", "register")
            return redirect(url_for("homepage"))
        if request.form.get("user") == "" or user_len > 12 or user_len < 5:
            flash("Username must be between 5 + 12 characters long!",
                  "register")
            return redirect(url_for("homepage"))
        if isValid(request.form["email"]) is True:
            print("This is a valid email address")
        else:
            flash("Invalid Email", "register")
            return redirect(url_for("homepage"))
        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form["pass"].encode("utf-8"), bcrypt.gensalt()
            )
            users.insert(
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
    return render_template("account.html")


@app.route("/account/<user>")
@login_required
def account(user):
    if user == session['user']:
        user = users.find_one({"user": session["user"]})
        reviews = review.find({"user": session["user"]}).sort("date", -1)
        return render_template("account.html", user=user, reviews=reviews)
    else:
        flash("Sorry thats is not your profile!", "error")
        return render_template("homepage.html")


@app.route("/account/<user>/upload", methods=["POST"])
@login_required
def profile_upload(user):
    if "profile_image" in request.files:
        profile_image = request.files["profile_image"]
        mongo.save_file(profile_image.filename, profile_image)
        users.find_one_and_update(
            {"user": session["user"]},
            {"$set": {"profile_image": profile_image.filename}})

        return redirect(url_for("account", user=session["user"]))


@app.route("/delete/<id>", methods=["POST"])
@login_required
def delete(id):
    if request.method == "POST":
        books = book.find_one({"_id": ObjectId(id)})
        user = users.find_one({"_id": ObjectId(id)})
        reviews = review.find_one({"_id": ObjectId(id)})
        return render_template("delete.html", book=books, user=user,
                               review=reviews)


@app.route("/account/<user>/delete", methods=["POST"])
@login_required
def delete_account(user):
    users.delete_one({"user": session["user"]})
    session.pop("user", None)
    flash("Account Deleted!!", "error")
    return redirect(url_for("homepage"))


@app.route("/account/<user>/<review_id>", methods=["POST"])
@login_required
def delete_review(user, review_id):
    reviews = review.find_one({"_id": ObjectId(review_id)})
    book.find_one_and_update(
        {"_id": ObjectId(reviews["book_id"])},
        {"$pull": {"reviews": {"review_id": ObjectId(review_id)}}})
    users.find_one_and_update(
        {"_id": ObjectId(reviews["user_id"])},
        {"$pull": {"reviews": {"review_id": ObjectId(review_id)}}})
    review.delete_one({"_id": ObjectId(review_id)})
    book.find_one_and_update(
        {"_id": ObjectId(reviews["book_id"])}, {"$inc": {"no_of_reviews": -1}})
    flash("Review Deleted!!!", "error")
    return redirect(url_for("account", user=session["user"]))


@app.route("/user_uploads/<filename>")
@login_required
def user_upload(filename):
    return mongo.send_file(filename)


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
    books = book.find_one({"_id": ObjectId(book_id)})
    return render_template("one_book.html", book=books)


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
    books = book.find().sort("original_publication_year", 1).skip(
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
    books = book.find().sort("average_rating", -1).skip(
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


@app.route("/all_books/delete/<book_id>", methods=["POST"])
def delete_book(book_id):
    book.delete_one({"_id": ObjectId(book_id)})
    flash("Book Deleted!!!", "error")
    return redirect(url_for("get_books"))


@app.route("/all_books/edit_book/<book_id>", methods=["POST"])
def edit_book(book_id):
    books = book.find_one({"_id": ObjectId(book_id)})
    return render_template("edit_book.html", book=books)


@app.route("/all_books/edit_book/<book_id>/updating_book", methods=["POST"])
def updating_book(book_id):
    book.find_one_and_update(
        {"_id": ObjectId(book_id)},
        {
            "$set": {
                "title": request.form.get("title"),
                "authors": request.form.get("authors"),
                "isbn13": request.form.get("isbn"),
                "original_publication_year": request.form.get("year"),
                "language_code": request.form.get("language"),
                "description": request.form.get("description"),
            }
        },
    )

    flash("Successfully Updated Book!", "success")

    return redirect(url_for("get_books"))


@app.route("/all_books/add_book")
def add_book():
    if session.get("user") is None:
        flash("You need to login!", "warning")
        return redirect(url_for("homepage"))
    else:
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
            "language_code": request.form.get("language"),
            "description": request.form.get("description"),
            "image_url": request.form.get("image"),
            "posted_by": session['user'],
            "time_added": now})
    book_id = book.find_one({"title": request.form.get("title")})

    return redirect(url_for("get_one_book", book_id=book_id["_id"]))


@app.route("/all_books/add_review/<book_id>", methods=["POST"])
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
def edit_review(book_id):
    books = book.find_one({"_id": ObjectId(book_id)})
    user = users.find_one({"user": session["user"]})

    return render_template("edit_review.html", books=books, user=user)


@app.route("/all_books/update_review/<book_id>", methods=["POST"])
def update_review(book_id):
    books = book.find_one({"_id": ObjectId(book_id)})
    user = users.find_one({"user": session["user"]})
    reviews = review.find_one({"book_id": ObjectId(book_id)})
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
                "user_rating": request.form.get("stars"),
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
                  "user_rating": request.form.get("stars"),
                  "date": now}}})
    if request.form.get("description") == "":
        flash("Review edited successfully!", "success")
        return redirect(url_for("get_books"))
    else:
        book.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {"$set": {"description": request.form.get("description")}},
        )

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
         "user_rating": request.form.get("stars"),
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
                   "user_rating": request.form.get("stars"),
                   "date": now}}})
    book.find_one_and_update(
        {"_id": ObjectId(book_id)}, {"$inc": {"no_of_reviews": 1}})

    if request.form.get("description") == "":
        flash("Review posted successfully!", "success")
        return redirect(url_for("get_one_book", book_id=book_id))
    else:
        book.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {"$set": {"description": request.form.get("description")}},
        )
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
    today = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    week_ago = datetime.now() - timedelta(days=7)
    week_ago_str = week_ago.strftime("%d/%m/%Y, %H:%M:%S")

    five_star = (
        book.find({"reviews.user_rating": "5"}).sort("date", -1).limit(5))
    four_star = (
        book.find({"reviews.user_rating": "4"}).sort("date", -1).limit(5))
    three_star = (
        book.find({"reviews.user_rating": "3"}).sort("date", -1).limit(5))
    most_recent = (
        book.find(
            {"reviews.time_of_post": {"$gte": week_ago_str, "$lt": today}})
        .sort("reviews.date", -1).limit(5))

    return render_template(
        "recommendations.html",
        five_star=five_star,
        four_star=four_star,
        three_star=three_star,
        most_recent=most_recent)


@app.errorhandler(405)
def method_not_allowed(e):
    flash("Sorry you cannot do that!", "error")
    return render_template("homepage.html"), 405


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")), debug=True)
