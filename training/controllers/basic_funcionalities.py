from flask import Blueprint, session, g

from training.controllers.function_decorators import login_required

bp = Blueprint('basic', __name__)


@bp.route('/inside')
@login_required
def inside():
    return "You are already logged as --> " + str(session['username']), 200


@bp.route('/ver')
@login_required
def ver():
    return session.get('username')


@bp.route('/g')
def test_g():
    if g.user is None:
        return "No user logged", 401
    else:
        user_dict = {}
        for field in g.user.__dict__:
            if field != '_sa_instance_state':
                user_dict[field] = g.user.__dict__[field]
        return user_dict, 200
