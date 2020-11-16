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

# Creates Search index for search form on books.html
mongo.db.books.create_index(
    [("title", "text"),
     ("authors", "text")],
    name="search_index",
    default_language="english",
    weights={
        "title": 100,
        "authors": 10})


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
        If the above all fail then you are redirected to your new account page,
        with your inputted username being passed as the user variable.

    """
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
        {"user": request.form["user"],
         "password": hashpass,
         "email": request.form["email"],
         "profile_image": ""})
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
    login_user = mongo.db.users.find_one({"user": request.form["user"]})
    if login_user:
        if (bcrypt.hashpw(request.form["pass"].encode("utf-8"),
                          login_user["password"])
                == login_user["password"]):
            session["user"] = request.form["user"]
            flash("Welcome Back " + session["user"].capitalize() +
                  "!", "success")
            return redirect(url_for("account", user=session["user"]))
        flash("Invalid username/password combination", "error")
        return redirect(url_for("homepage"))
    else:
        flash("Sorry you cannot do that!", "error")
        return render_template("homepage.html")


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
    """Users account page.

    Once an account has been created the user is able to display a profile
    page with any reviews they have posted or personal info. This uses the
    @login_required decorator to make sure the user is logged in.

    Args:
        user: The current user obtained via the session['user'] variable.

    Returns:
        if arg 'user' is equal to the session['user'] then the account page is
        displayed and the user and review variables are passed.
        else an error message and the homepage are displayed, this stops users
        accessing other users accounts.

    """
    if user == session["user"]:
        user = mongo.db.users.find_one({"user": session["user"]})
        reviews = mongo.db.reviews.find({
            "user": session["user"]}).sort("date", -1)
        return render_template("account.html", user=user, reviews=reviews)
    else:
        flash("Sorry thats is not your profile!", "error")
        return render_template("homepage.html")


@app.route("/account/<user>/upload", methods=["POST"])
def profile_image_upload(user):
    """Upload profile photo to database.

    Used as the action attribute on the Photo upload form.
    When the form is submitted the photo chosen is uploaded to the user
    database within the document matching the session['user'].

    Args:
        user: The current user obtained via the session['user'] variable.

    Returns:
        redirects user back to the account page once successfully uploading
        a profile image whilst passing the user variable.

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
    """Access users uploaded profile images

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
    """Delete Book, User, Or Review Data.

    This is used as the action attribute on all delete buttons, once selected
    it checks if the ObjectId is in the books, user or reviews database!

    Args:
        id: dependent on which button is pressed either the User id, book id or
          review id is passed into the form displaying the appropriate delete
          page

    Returns:
        the delete page template is rendered with the relevant database
        connected and passing the variables book, user and review.
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
    """Delete a review from your account.

    On the users profile the user is able to delete reviews they have
    posted, it updates all linked databases and deletes all relevant
    info.

    Args:
        user: The current user obtained via the session['user'] variable.
        review_id: ObjectId passed from delete button located on account
        page.

    Returns:
        Once the delete button is selected the user is sent back to the
        account page with the user variable passed again.

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
    return redirect(url_for("account", user=user))


@app.route("/account/delete/<user>", methods=["POST"])
def delete_account(user):
    """Delete the Account from the website.

    The user is able to delete the whole account, it completely removed user
    info from the site but does not delete the reviews they have posted.

    Args:
        user: The current user obtained via the session['user'] variable.

    Return:
        Once the users account is deleted they are redirected back to the
        homepage.

    """
    mongo.db.users.delete_one({"user": user})
    session.pop("user", None)
    flash("Account Deleted!!", "warning")
    return redirect(url_for("homepage"))


@app.route("/all_books/delete/<book_id>", methods=["POST"])
def delete_book(book_id):
    """Delete a book from the website.

    If the user is the admin then they can delete all books, if the user
    uploaded the book then they are able to delete the book.

    Args:
        book_id: ObjectId passed from the delete button located on the books
          page.

    returns:
        Once the book has been deleted they are redirected to the all books /
        get books page.

    """
    mongo.db.books.delete_one({"_id": ObjectId(book_id)})
    flash("Book Deleted!!!", "warning")
    return redirect(url_for("get_books"))


@app.route("/account/<user>/edit_profile", methods=["POST"])
def edit_profile(user):
    """Form to upload user information

    If the user arg matches the session["user"] then a form is displayed
    to fill out to edit their profile information.

    Args:
        user: The current user obtained via the session['user'] variable.

    Returns:
        renders edit_profile.html if user=session["user"]
        else it redirects back to the current user account
        both passing the user variable.

    """
    if user == session["user"]:
        user = mongo.db.users.find_one({"user": user})
        return render_template("edit_profile.html", user=user)
    return redirect(url_for("account", user=session["user"]))


@app.route("/account/<user>/editing_profile ", methods=["POST"])
def updating_user_details(user):
    """Upload user informaton to the database

    This is the action attribute to the edit profile form. Once submitted
    the information input to the form is uploaded to the user database,
    using the user arg to find the correct document.

    Args:
        user: The current user obtained via the session['user'] variable.

    Returns:
        redirects the user back to their account page and passing the user
        variable.

    """
    mongo.db.users.find_one_and_update(
        {"user": user},
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

    return redirect(url_for("account", user=user))


@app.route("/all_reviews")
def all_reviews():
    """Display all the reviews on the database.

    This page shows the user all the reviews posted by everyone on the site.
    It displays 5 reviews per page with all the information such as username of
    poster, star rating, a link to thebook page and amazon link.

    Returns:
        Renders the template for all_reviews.html and passes the reviews and
        pagination variables.

    """
    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    reviews = mongo.db.reviews.find().sort("date", -1).skip(
        (page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page, page=page, total=reviews.count(),
        record_name="reviews")
    return render_template(
        "all_reviews.html", reviews=reviews, pagination=pagination)


@app.route("/recommendations")
def recommendations():
    """Displays all books recommended by users.

    The first row is the most recently recommended books then the
    next is all 5 star rated books and then finally 4 star rated.

    Returns:
        renders template for recommendations.html, passing five_star, four_star
        an recommended as variables.

    """
    recommended = (
        mongo.db.reviews.find(
            {"recommended": "yes"}).sort("date", -1).limit(5))
    five_star = (
        mongo.db.reviews.find({"user_rating": 5}).sort("date", -1).limit(5))
    four_star = (
        mongo.db.reviews.find({"user_rating": 4}).sort("date", -1).limit(5))

    return render_template(
        "recommendations.html", five_star=five_star, four_star=four_star,
        recommended=recommended)


@app.route("/all_books")
def get_books():
    """Display all books within the database.

    The page displays a link to all the available books in the database it
    shows the book cover, title, authors and the rating. clicking the book
    cover and data displays the book page. 48 books display per page.

    Returns:
        renders the template for books.html and passes books and pagination
        as variables.

    """
    per_page = 48
    page = request.args.get(get_page_parameter(), type=int, default=1)
    books = mongo.db.books.find().sort("title", 1).skip(
        (page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page, page=page, total=books.count(),
        record_name="books", format_total=True, format_number=True
    )
    return render_template("books.html", books=books, pagination=pagination)


@app.route("/all_books/year")
def get_books_year():
    """Display all books within the database sorted by year.

    The page displays a link to all the available books in the database but
    this time it displays by newest book first. All displayed the same as
    the normal books page.

    Returns:
        renders the template for books.html and passes books and pagination
        as variables.

    """
    per_page = 48
    page = request.args.get(get_page_parameter(), type=int, default=1)
    books = mongo.db.books.find().sort("original_publication_year", -1).skip(
        (page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page, page=page, total=books.count(),
        record_name="books", format_total=True, format_number=True)

    return render_template("books.html", books=books,
                           pagination=pagination)


@app.route("/all_books/rating")
def get_books_rating():
    """Display all books within the database sorted by rating.

    The page displays a link to all the available books in the database but
    this time it displays the top rated books first. All displayed the same
    as the normal books page.

    Returns:
        renders the template for books.html and passes books and pagination
        as variables.

    """
    per_page = 48
    page = request.args.get(get_page_parameter(), type=int, default=1)
    books = mongo.db.books.find().sort(
        [("user_rating_average", -1), ("average_rating", -1)]).skip(
        (page - 1) * per_page).limit(per_page)
    pagination = get_pagination(
        per_page=per_page, page=page, total=books.count(),
        record_name="books", format_total=True, format_number=True)

    return render_template("books.html", books=books,
                           pagination=pagination)


@app.route("/all_books/")
def get_books_search():
    """Display all books which match the users search.

    The page displays a link to books which match the users search.
    This time it may not display any pagination as a result may be less
    than 48 which is the amount for a page.

    Returns:
        renders the template for books.html and passes books and pagination
        as variables.

    """
    per_page = 48
    search_form = request.args["search"]
    page = request.args.get(get_page_parameter(), type=int, default=1)
    books = mongo.db.books.find({
        "$text": {"$search": search_form}}).sort("title", 1).skip((
            page - 1) * per_page).limit(per_page)
    pagination = get_pagination(per_page=per_page, page=page,
                                total=books.count(), record_name="books",
                                format_total=True, format_number=True)
    return render_template("books.html", books=books, pagination=pagination)


@app.route("/book/<book_id>")
def get_one_book(book_id):
    """Displays one book and information.

    When a user selects a book from a book link on various pages they
    are taken to that books page which displays a book description,
    any reviews and links for amazon and if the book info is incomplete
    a edit button is available to signed up users.

    Args:
        book_id: ObjectId passed from the book links.

    Returns:
        if book_id is a valid ObjectId and is not None then the books
        page is displayed and the books vatriable is passed, else if the
        book is none, null or the ObjectId is not valid then the homepage
        is displayed with an error message.

    """
    if ObjectId.is_valid(book_id):
        books = mongo.db.books.find_one({"_id": ObjectId(book_id)})
        if books is not None:
            return render_template("one_book.html", book=books)
        elif books == "null" or books is None:
            flash("Sorry this book does not exist", "warning")
            return render_template("homepage.html")
    else:
        flash("Sorry this book does not exist", "warning")
        return render_template("homepage.html")


@app.route("/all_books/add_book")
@login_required
def add_book():
    """Allow a user to input book data to the database.

    This opens up a form to input book data too the database.
    Only logged in users can add books.

    returns:
        renders template for add_book.html.
    """
    return render_template("add_book.html")


@app.route("/all_books/posting_book", methods=["POST"])
def post_book():
    """Post book data from users input.

    This is used as the acton attribute on the add book form,
    then uses that new book to pass the ObjectId as a variable.

    Returns:
        the user is redirected to the new book they have input.
        along with the book_id variable.

    """
    now = datetime.now().timestamp()
    mongo.db.books.insert_one(
        {"isbn13": request.form.get("isbn"),
         "title": request.form.get("title"),
         "authors": request.form.get("authors"),
         "original_publication_year": request.form.get("year"),
         "description": request.form.get("description"),
         "image_url": request.form.get("image"),
         "posted_by": session['user'],
         "time_added": now})
    book_id = mongo.db.books.find_one({"title": request.form.get("title")})

    return redirect(url_for("get_one_book", book_id=book_id["_id"]))


@app.route("/all_books/edit_book/<book_id>", methods=["POST"])
@login_required
def edit_book(book_id):
    """Edit a book on the database.

    The user can edit a book on the database if it is not complete.
    Such as add a book cover URL or add a book description. The
    @login_required decorator stops un-registered users accessing the page.

    Args:
        book_id: ObjectId passed from the books page.

    Returns:
        renders the template for edit_book.html and also passes
        the book variable.

    """
    books = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template("edit_book.html", book=books)


@app.route("/all_books/edit_book/<book_id>/updating_book", methods=["POST"])
def updating_book(book_id):
    """Posts book data to the database.

    This is used as the action attribute to the edit book form. If the book
    already has a URL for the cover then you cannot input a new URL but you are
    still able to edit the desciption.

    Args:
        book_id: ObjectId passed from the edit_book page.

    Returns:
        redirects back to the book you have just edited to view the changes.
        The book_id is passed again too.

    """
    mongo.db.books.find_one_and_update(
        {"_id": ObjectId(book_id)},
        {"$set": {"title": request.form.get("title"),
                  "authors": request.form.get("authors"),
                  "isbn13": request.form.get("isbn"),
                  "original_publication_year": request.form.get("year"),
                  "description": request.form.get("description")
                  }},)
    if request.form.get('url') == "":
        mongo.db.books.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {"$set": {
                "image_url": ("https://cdn.bookauthority.org/dist/images/"
                              "book-cover-not-available.6b5a104fa66be4eec"
                              "4fd16aebd34fe04.png")
            }},)
    elif request.form.get("url") is not None:
        mongo.db.books.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {"$set": {
                "image_url": request.form.get("url")
            }},)
    flash("Successfully Updated Book!", "success")
    return redirect(url_for("get_one_book", book_id=book_id))


@app.route("/all_books/add_review/<book_id>", methods=["POST"])
@login_required
def add_review(book_id):
    """Add a review to a book.

    On each book page is a link to add a review. Id the user is logged
    in they are able to add a review unless they have already added a review
    in which case they have to edit their original post. It also stops any
    users which dont have a profile photo from adding reviews until they do.

    Args:
        book_id: the ObjectId passed from the book page

    Returns:
        redirects back to account page if no profile photo or the book already
        has a review by the user and a relevant error message is shown and
        passing the user variable.
        If a profile photo is available and a review doesnt exist then the
        add_review.html page is rendered and the user variable is passed again
        along with the books variable.

    """
    user = mongo.db.users.find_one({"user": session["user"]})
    if user["profile_image"] == "":
        flash("Please Upload A Profile Photo!", "error")
        return redirect(url_for("account", user=session["user"]))
    existing_review = mongo.db.books.find_one(
        {"_id": ObjectId(book_id), "reviews.user": session["user"]})
    if existing_review:
        flash("You have already reviewed this book please \
              Edit your original post", "error")
        return redirect(url_for("account", user=session["user"]))
    if existing_review is None:
        books = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template("add_review.html", books=books, user=user)


@app.route("/all_books/edit_review/<book_id>", methods=["POST"])
def edit_review(book_id):
    """Edit existing review that you have posted

    When a user has already posted a review to a book and want to
    make changes or have changed opinion then they can edit the review.

    Args:
        book_id: book ObjectId is passed from the accounts page.

    Retuns:
        renders the template for edit_review.html and the variables books
        and users.

    """
    books = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    user = mongo.db.users.find_one({"user": session["user"]})

    return render_template("edit_review.html", books=books, user=user)


@app.route("/all_books/post_review/<book_id>", methods=["POST"])
def post_review(book_id):
    """Post new review to the website.

    Used as the action attribute for the update review form. Once the form
    is submitted a new review is uploaded to the website. the data is uploaded
    into a reviews database and also the books database and referenced in the
    users document in the database.

    Args:
        book_id: book ObjectId is passed from the add review page.

    Retuns:
        Redirects back to the books page to view the new review.
        The book_id is passed to display the correct page.

    """
    books = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    user = mongo.db.users.find_one({"user": session["user"]})
    now = datetime.now().timestamp()
    mongo.db.reviews.insert_one(
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
    reviews = mongo.db.reviews.find_one(
        {"user_id": ObjectId(user["_id"]),
         "book_id": ObjectId(book_id)})
    mongo.db.users.find_one_and_update(
        {"_id": ObjectId(user["_id"])},
        {"$push": {"reviews": {
                   "review_id": ObjectId(reviews["_id"]),
                   "book_id": ObjectId(book_id)}}})
    mongo.db.books.find_one_and_update(
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
    mongo.db.books.find_one_and_update(
        {"_id": ObjectId(book_id)}, {"$inc": {"no_of_reviews": 1}})

    pipeline = [
        {"$addFields": {
            "user_rating_average": {"$toDecimal": {
                "$avg": "$reviews.user_rating"}}}}, {
            "$out": "books"}
    ]
    mongo.db.books.aggregate(pipeline)

    flash("Review posted successfully!", "success")
    return redirect(url_for("get_one_book", book_id=book_id))


@app.route("/all_books/update_review/<book_id>", methods=["POST"])
def update_review(book_id):
    """Post updated review to the website.

    Used as the action attribute for the update review form. Once the form
    is submitted the existing review is turned into a new review. updating
    all the existing data.

    Args:
        book_id: book ObjectId is passed from the edit review page.

    Retuns:
        Redirects back to the account page to view the new review.
        The user variable is also passed to display the correct page.

    """
    books = mongo.db.books.find_one({"_id": ObjectId(book_id),
                                     "reviews.user": session["user"]})
    user = mongo.db.users.find_one({"user": session["user"]})
    reviews = mongo.db.reviews.find_one({"book_id": ObjectId(book_id),
                                         "user": session["user"]})
    now = datetime.now().timestamp()
    mongo.db.reviews.find_one_and_update(
        {"user_id": ObjectId(user["_id"]), "book_id": ObjectId(book_id)},
        {"$set": {"user_id": ObjectId(user["_id"]),
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
    mongo.db.users.find_one_and_update(
        {"_id": ObjectId(user["_id"]),
         "reviews.review_id": ObjectId(reviews["_id"])},
        {"$set": {"reviews.$": {
                  "review_id": ObjectId(reviews["_id"]),
                  "book_id": ObjectId(book_id)}}})
    mongo.db.books.find_one_and_update(
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
    mongo.db.books.aggregate(pipeline)

    flash("Review edited successfully!", "success")
    return redirect(url_for("account", user=session["user"]))


@app.errorhandler(405)
def method_not_allowed(e):
    """Error handler for 405 method not allowed.

    For when the user is likely to encounter 405 errors such as when
    the user may type in a book id into the url, i dont want blank pages
    so i do not allow "GET" requests.

    Returns:
        renders template for the homepage and give a error message to the user.

    """
    flash("ERROR 405!! Sorry you cannot do that!", "error")
    return render_template("homepage.html"), 405


# Run Application with enviroment variables.
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")), debug=True)
