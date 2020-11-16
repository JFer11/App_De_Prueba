from flask import Blueprint, request, redirect, render_template, url_for, g, session

from training.extensions import db, bcrypt
# Duda, porque no funciona?
# with current_app.app_context():
#    db = current_app.db
from training.models.users import User
from training.controllers.forms import index_form, login_form
from training.controllers.function_decorators import login_required


bp = Blueprint('auth', __name__)


@bp.before_app_request
def user_to_g():
    username = session.get('username')
    if username is not None:
        # If a user has a session, it will be always in the database
        user = db.session.query(User).filter_by(id=username).first()
        g.user = user
    else:
        g.user = None
    return None


def test_unique_fields(form):
    if User.query.filter_by(id=form['username']).first() or User.query.filter_by(email=form['email']).first() is not None:
        return False
    else:
        return True


@bp.route('/register', methods=['GET', 'POST'])
def signup():
    form = index_form.RegistrationForm(request.form)

    if request.method == 'POST':
        if form.validate():
            if test_unique_fields(request.form):
                id_user = request.form['username']
                username = request.form['username']
                password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
                email = request.form['email']

                user = User(id=id_user, username=username, email=email, password=password)

                db.session.add(user)
                db.session.commit()

                return redirect(url_for('auth.sign_in')), 201
            else:
                return render_template('bad_form.html'), 420
        else:
            form = index_form.RegistrationForm(request.form)
            return render_template('index.html', form=form, alert=True), 400

    return render_template('index.html', form=form, alert=False), 200


@bp.route('/login', methods=['GET', 'POST'])
def sign_in():
    form = login_form.LoginWTForm(request.form)

    if request.method == 'POST' and form.validate():
        our_user = User.query.filter_by(id=request.form['username']).first()

        if our_user is not None:
            if our_user.mail_validation:
                if bcrypt.check_password_hash(our_user.password, request.form['password']):
                    # Se le da la cookie session
                    session['username'] = request.form['username']
                    return redirect(url_for('basic.inside')), 200
                else:
                    # Bad password
                    return render_template('login.html', form=form, alert=True), 452
            else:
                return render_template('login.html', form=form, alert_mail=True), 451
        else:
            return render_template('login.html', form=form, alert=True), 450

    return render_template('login.html', form=form), 800


@bp.route('/logout')
@login_required
def logout():
    if 'username' in session:
        a = session['username']
        session.pop('username', None)
        return f"The username {a} was logged out", 200
    return "There was no session logged", 400
