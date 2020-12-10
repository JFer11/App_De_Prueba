from flask import Blueprint, jsonify, abort, make_response, request, session, g

from training.controllers.function_decorators import login_required
from training.extensions import bcrypt, db
from training.models.users import User, UserSchema
from training.utils.common_variables import serializer

bp = Blueprint('api', __name__, url_prefix='/api')


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
    {
        'id': 3,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': True
    }
]


@bp.route('/example')
def example():
    return jsonify({'tasks': tasks})


@bp.route('/example/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        # 404 means resource not found, exactly what happens here
        abort(404)
    return jsonify({'task': task[0]})


"""
To avoid this response when a 404 error was generated:
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
 
 We craft the function below.
"""


@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found doggy'}), 404)


@bp.route('/example', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        print("Mamarracho")
        abort(400)
    else:
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False
        }
        tasks.append(task)
        return jsonify({'task': task}), 201

    session['title'] = request.json['title']
    return "PEPE", 205

# request.get_json()


# True endpoint start here
def repeated_fields(fields):
    if User.query.filter_by(id=fields.get('username')).first() is not None or User.query.filter_by(id=fields.get('email')).first() is not None:
        return True
    return False


@bp.route('/register', methods=['POST'])
def sign_up():
    if not request.json or not 'username' in request.json or not 'password' in request.json or not 'email' in request.json:
        return make_response(jsonify({'Error': 'Your json body is wrong, we expect username, password and email!'}), 400)
    else:
        if repeated_fields(request.json):
            return make_response(jsonify({'Error': 'username or email already registered!'}),
                                 400)

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
        return make_response(jsonify({'Error': 'Your json body is wrong, we expect username, password and email!'}), 400)
    else:
        our_user = User.query.filter_by(id=request.json.get('username')).first()

        if our_user is None:
            return make_response(jsonify({'Error': 'User does not exist!'}), 404)
        else:
            if our_user.mail_validation is False:
                return make_response(jsonify({'Error': 'Not validated email!'}), 401)
            else:
                if bcrypt.check_password_hash(our_user.password, request.json.get('password')):
                    token = serializer.dumps(request.json.get('username'), salt='login')
                    body = {
                        "auth_token": token
                    }
                    return jsonify(body), 200
                else:
                    return make_response(jsonify({'Error': 'Bad password!'}), 401)


@bp.route('/verify/email/<string:username>')
def verify_email(username):
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        return make_response(jsonify({'Error': 'User does not exist!'}), 404)
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
        return make_response(jsonify({'Error': 'User does not exist!'}), 404)

    user_schema = UserSchema()
    output = user_schema.dump(our_user)

    return jsonify(output), 200


@login_required
@bp.route('/users/data')
def return_logged_users_data():
    username = g.user.username
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        return make_response(jsonify({'Error': 'User does not exist!'}), 404)

    user_schema = UserSchema()
    output = user_schema.dump(our_user)

    return jsonify(output), 200
