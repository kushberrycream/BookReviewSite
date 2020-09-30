from datetime import datetime
from functools import wraps
from flask_paginate import Pagination
from flask import Flask, session, flash, redirect, url_for
from flask_toastr import Toastr
import re

app = Flask(__name__)
toastr = Toastr(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("You need to login!", "warning")
            return redirect(url_for("homepage"))
        return f(*args, **kwargs)
    return decorated_function


def humanize_ts(timestamp=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    diff = now - datetime.fromtimestamp(timestamp)
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(int(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"


def isValid(email):
    if (re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
       is not None):
        return True
    return False


def get_pagination(**kwargs):
    kwargs.setdefault("record_name", "books")
    return Pagination(
        css_framework=app.config.get("CSS_FRAMEWORK", "bootstrap4"),
        link_size=app.config.get("LINK_SIZE", "md"),
        show_single_page=app.config.get("SHOW_SINGLE_PAGE", False),
        **kwargs)
