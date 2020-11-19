"""Decorators and Functions used within app.py.

All the below functions have been kept away from the routing to keep my code
clean. I use them multiple times throughout the application such as the
@login_required decorator.

"""
from datetime import datetime
from functools import wraps
from flask_paginate import Pagination
from flask import Flask, session, flash, redirect, url_for
import re

# Initilizing Flask
app = Flask(__name__)


def login_required(f):
    """Login required decorator

    Used within app.py on any routes that need user authetification. when
    the decorator is used on a func it will initilize the decorated_function
    function and check if the user is not in session.

    Args:
        f: f is the function in which login required wraps.

    Returns:
        Redirects to the homepage / login screen if no user is in session.
        if it fails you the original function is performed.

    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("You need to login!", "warning")
            return redirect(url_for("homepage"))
        return f(*args, **kwargs)
    return decorated_function


def humanize_ts(timestamp=False):
    """Turn timestamps to human readable format.

    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc

    Args:
        timestamp: timestamp that function wraps

    Returns:
        A string saying how long ago the user posted the review.

    """
    now = datetime.now()
    diff = now - datetime.fromtimestamp(timestamp)
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ""
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
    """Checks for valid email addresses

    On the register form i only want genuine emails so I needed a function to
    check for genuine emails.

    Args:
        email: the email address supplied for validation.

    Returns:
        If email is genuine it returns True if not then it is False.

    """
    if (re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
       is not None):
        return True
    return False


def get_pagination(**kwargs):
    """Pagination configuration.

    used to configure pagination framework, size etc.

    Returns:
        class to display pagination with the bootstrap framework.
        MDBootstrap in my case.

    """
    return Pagination(
        css_framework=app.config.get("CSS_FRAMEWORK", "bootstrap4"),
        link_size=app.config.get("LINK_SIZE", "sm"),
        show_single_page=app.config.get("SHOW_SINGLE_PAGE", False), **kwargs)
