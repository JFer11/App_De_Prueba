from flask import Blueprint, session, g

from training.controllers.function_decorators import login_required

#Hay que ver donde carajo poner esto--------------------------------------------------------------------------------------
# from training.controllers.admin import admin_web
#Hay que ver donde carajo poner esto--------------------------------------------------------------------------------------


bp = Blueprint('name2', __name__)


@bp.route('/inside')
@login_required
def inside():
    if 'username' in session:
        return "You are already logged as --> " + str(session['username']), 200

    return "You are not logged in", 400


@bp.route('/ver')
@login_required
def ver():
    return session.get('username')


@bp.route('/g')
def test_g():
    if g.user is None:
        return "No  hay usuario logueado", 411
    else:
        return str(g.user), 200
