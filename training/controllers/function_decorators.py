from functools import wraps
from flask import session, render_template, request
from itsdangerous import BadSignature

from training.utils.common_variables import serializer


def login_required(function):
    @wraps(function)
    # @wraps does this: wrap.__name__ = function.__name__
    def wrap(*args, **kwargs):
        username = session.get('username', None)
        header = request.headers.get('auth_token', None)

        if header is not None:
            # Check valid header:
            try:
                serializer.loads(header, salt='login')
            except BadSignature:
                # Wrong header
                header = None

        if username is None and header is None:
            return render_template("no_login.html"), 411

        return function(*args, **kwargs)
    return wrap
