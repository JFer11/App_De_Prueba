import json
import os
from flask import Blueprint, jsonify, abort, make_response, request, session, g
from itsdangerous import URLSafeTimedSerializer, BadSignature

from training.controllers.function_decorators import login_required
from training.extensions import bcrypt, db
from training.models.users import User

bp = Blueprint('api', __name__, url_prefix='/api')

serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))


def repeated_fields(fields):
    if User.query.filter_by(id=fields.get('username')).first() is not None or User.query.filter_by(
            id=fields.get('email')).first() is not None:
        return True
    return False


@bp.route('/register', methods=['POST'])
def sign_up():
    if not request.json or not 'username' in request.json or not 'password' in request.json or not 'email' in request.json:
        abort(400)
    else:
        if repeated_fields(request.json):
            abort(400)

        id_user = request.json.get('username')
        username = request.json.get('username')
        password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8')
        email = request.json.get('email')

        user = User(id=id_user, username=username, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return jsonify({'username': username, 'password': password}), 201


@bp.route('/login', methods=['POST'])
def sign_in():
    """
    Important: here, an auth_token will be provided through the response body.
    Then to access the endpoints that require a login (@login_required), you need to attach
    the auth_token in the request header manually.
    """

    if not request.json or not 'username' in request.json or not 'password' in request.json:
        abort(400)
    else:
        our_user = User.query.filter_by(id=request.json.get('username')).first()

        if our_user is None:
            abort(400)
        else:
            if our_user.mail_validation is False:
                abort(401)
            else:
                if bcrypt.check_password_hash(our_user.password, request.json.get('password')):
                    token = serializer.dumps(request.json.get('username'), salt='login')
                    body = {
                        "auth_token": token
                    }
                    return jsonify(body), 200
                else:
                    return "Bad password", 450


@bp.route('/verify/email/<string:username>', methods=['POST'])
def verify_email(username):
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        abort(404)
    else:
        if our_user.mail_validation:
            detail = {'Detail': "Email was already validated."}
            return jsonify(detail), 202
        else:
            our_user.mail_validation = True
            db.session.commit()

            detail = {'Detail': "Email from user was successfully validated."}
            return jsonify(detail), 200


@bp.route('/users/data/<string:username>')
def return_user_data(username):
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        abort(404)

    # user_json = json.dumps(our_user.__dict__)
    user_json = {
        "username": our_user.username,
        "email": our_user.email,
        "password": our_user.password,
        "mail_validation": our_user.mail_validation,
        "created_at": our_user.created_at
    }

    return user_json, 200


@bp.route('/users/data')
@login_required
def return_logged_users_data():
    username = g.user.username
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        abort(404)

    # user_json = json.dumps(our_user.__dict__)
    user_json = {
        "username": our_user.username,
        "email": our_user.email,
        "password": our_user.password,
        "mail_validation": our_user.mail_validation,
        "created_at": our_user.created_at
    }

    return user_json, 211
