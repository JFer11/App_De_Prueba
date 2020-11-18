from functools import wraps
from flask import session, render_template


def login_required(function):
    @wraps(function)
    # @wraps does this: wrap.__name__ = function.__name__
    def wrap(*args, **kwargs):
        username = session.get('username')
        if username is None:
            return render_template("no_login.html"), 411
        return function(*args, **kwargs)
    return wrap
