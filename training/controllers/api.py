from flask import Blueprint, jsonify, request, g
from marshmallow import ValidationError

from training.controllers.function_decorators import login_required
from training.extensions import bcrypt, db
from training.models.users import User, UserSchema, UserSchemaValidationSignIn, UserSchemaValidationSignUp
from training.utils.common_functions import test_unique_fields
from training.utils.common_variables import serializer

bp = Blueprint('api', __name__, url_prefix='/api')


def validate_user(request_json, function):
    try:
        if function == "sign_in":
            UserSchemaValidationSignIn().load(request_json)
        elif function == "sign_up":
            UserSchemaValidationSignUp().load(request_json)
        else:
            return {
                "Valid": False,
                "Details": "Bad function type."
            }
        return {
            "Valid": True,
            "Details": "All fields are valid."
        }
    except ValidationError as err:
        return {
            "Valid": False,
            "Details": [err.messages, err.valid_data]
        }


def repeated_fields(fields):
    if User.query.filter_by(id=fields.get('username')).first() is not None or User.query.filter_by(
            id=fields.get('email')).first() is not None:
        return True
    return False


@bp.route('/register', methods=['POST'])
def sign_up():
    valid = validate_user(request.json, "sign_up")
    if valid["Valid"] is False:
        return jsonify({"Details": valid["Details"]}), 400

    if not test_unique_fields(request.json["username"], request.json["email"]):
        return jsonify({'Error': 'username or email already registered!'}), 400

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

    valid = validate_user(request.json, "sign_in")
    if valid["Valid"] is False:
        return jsonify({"Details": valid["Details"]})

    our_user = User.query.filter_by(id=request.json.get('username')).first()

    if our_user is None:
        return jsonify({'Error': 'User does not exist!'}), 404
    else:
        if our_user.mail_validation is False:
            return jsonify({'Error': 'Not validated email!'}), 401
        else:
            if bcrypt.check_password_hash(our_user.password, request.json.get('password')):
                token = serializer.dumps(request.json.get('username'), salt='login')
                body = {
                    "auth_token": token
                }
                return jsonify(body), 200
            else:
                return jsonify({'Error': 'Bad password!'}), 401


@bp.route('/verify/email/<string:username>', methods=['POST'])
def verify_email(username):
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        return jsonify({'Error': 'User does not exist!'}), 404
    else:
        if our_user.mail_validation:
            return jsonify({"Detail": "The email {} was already validated.".format(our_user.username)}), 202
        else:
            our_user.mail_validation = True
            db.session.commit()
            return jsonify({"Detail": "Email from user {} was successfully validated.".format(our_user.username)}), 200


@bp.route('/users/data/<string:username>')
def return_user_data(username):
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        return jsonify({'Error': 'User does not exist!'}), 404

    user_schema = UserSchema()
    output = user_schema.dump(our_user)

    return jsonify(output), 200


@bp.route('/users/data')
@login_required
def return_logged_users_data():
    username = g.user.username
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        return jsonify({'Error': 'User does not exist!'}), 404

    user_schema = UserSchema()
    output = user_schema.dump(our_user)

    return jsonify(output), 200
