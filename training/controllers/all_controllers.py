from flask import render_template, make_response, request, redirect, url_for, g
from flask import session as sesion
from flask_mail import Message
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from training.app import app, db, mail, bcrypt
from training.controllers import index_form, login_form, recover_form, new_password_form, send_email_form
from training.controllers.admin import admin_web
from training.background_tasks.tasks import send_email_async
from training.models.users import User


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
s = URLSafeTimedSerializer(app.secret_key)


@app.before_request
def user_to_g():
    username = sesion.get('username')
    if username is not None:
        # Suponemos que el usuario si tiene la session, siempre va a estar en la base de datos
        user = db.session.query(User).filter_by(id=username).first()
        g.user = user
    return None


def login_required(function):
    @wraps(function)
    #wrap.__name__ = function.__name__
    def wrap(*args, **kwargs):
        username = sesion.get('username')
        if username is None:
            return "Error, must be logged in"
            # Redirigir a un HTML de error y algo que trabaje el error, capaz en el header. QUe se puede hacer cuando no
            # esta logeado?
        return function(*args, **kwargs)
    return wrap


@app.route('/')
def primera():
    return make_response("HOLAAAAAA")


@app.route('/index', methods=['GET', 'POST'])
def signup():
    form = index_form.RegistrationForm(request.form)

    if request.method == 'POST':
        if form.validate():
            # Guardar en la base
            id = request.form['username']
            username = request.form['username']
            password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            # .decode('utf-8') Esto es muy raro, lo vi en un comentario de una respuesta de stack overflow
            # me parece que es porque en versiones anteoriores de bcrypt no hay
            email = request.form['email']
            user = User(id=id, username=username, email=email, password=password)

            db.session.add(user)
            db.session.commit()

            # Redireccionar a otro HTML que entre a la pagina
            return redirect(url_for('sign_in'))
        else:
            form = index_form.RegistrationForm(request.form)
            return render_template('index.html', form=form, alert=True)

    return render_template('index.html', form=form, alert=False)


@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    form = login_form.LoginWTForm(request.form)

    if request.method == 'POST' and form.validate():
        our_user = User.query.filter_by(id=request.form['username']).first()

        if our_user is not None:
            # Si lo encontre en la base, me meto aca
            # Chequea el password a ver si coincide y si el mail esta validado
            if bcrypt.check_password_hash(our_user.password, request.form['password']) and our_user.mail_validation:
                # Se le da la cookie session
                sesion['username'] = request.form['username']
                return redirect(url_for('inside'))

            if not our_user.mail_validation:
                return render_template('login.html', form=form, alert_mail=True)

            #Solo pasa si la contraseña esta mal
            return render_template('login.html', form=form, alert=True)

        else:
            return render_template('login.html', form=form, alert=True)

    return render_template('login.html', form=form)


@app.route('/inside')
@login_required
def inside():
    if 'username' in sesion:
        return "Ya estas registrado como --> " + str(sesion['username'])

    return "No estas registrado"


@app.route('/logout')
@login_required
def logout():
    if 'username' in sesion:
        a = sesion['username']
        sesion.pop('username', None)
        return "Se deslogueo la sesion. --> " + str(a)
    return "No habia sesiones iniciadas"


@app.route('/ver')
@login_required
def ver():
    return sesion.get('username')


@app.route('/mail')
def prueba_mail():
    email = 'donnetta7@adriveriep.com'
    msg = Message('Confirm Email', sender='anthony@prettyprinted.com', recipients=[email])
    msg.body = "Bienvenido"
    mail.send(msg)
    return "0"


@app.route('/mail/validation/<string:username>')
def email_verification(username):
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        return "No existe ese usuario"
    else:
        if our_user.mail_validation:
            return "El email de {} ya estaba validado".format(our_user.username)
        else:
            #No me gusta esta manera de updatear
            our_user.mail_validation = True
            db.session.commit()
            return "Se valido el email de {}".format(our_user.username)


@app.route('/send/email', methods=['GET', 'POST'])
def send_email():
    form = send_email_form.SendEmailForm(request.form)

    if request.method == 'POST':
        email_sender = request.form['email_sender']
        email_recipient = request.form['email_recipient']
        message_body = request.form['message_body']
        message_body = request.form['message_body']
        msg = Message('Mail de prueba', sender=email_sender, recipients=[email_recipient])
        msg.body = message_body
        if 'send_now' in request.form:
            mail.send(msg)
            return render_template('email_form_template.html', form=form, sended=True)
        else:

            send_email_async(msg)
            return render_template('email_form_template.html', form=form, sended=True)
    return render_template('email_form_template.html', form=form)

  
@app.route('/recover', methods=['GET', 'POST'])
def recover_account():
    form = recover_form.RecoverForm()

    if request.method == 'POST':
        our_user = User.query.filter_by(email=request.form['email']).first()
        #our_user = session.query(User).filter_by(email=request.form['email']).first()
        if our_user is not None:
            send_token_to_email(request.form['email'])
            return render_template('recover.html', form=form, accepted_request=True)
        else:
            return render_template('recover.html', form=form, accepted_request=True)

    return render_template('recover.html', form=form)


def send_token_to_email(email):
    token = s.dumps(email, salt='recover-email')
    msg = Message('Recover Email', sender='no_reply@system.com', recipients=[email])
    link = url_for('validate_token', token=token, _external=True)
    msg.body = f"Haga click aqui para recuperar su cuenta: {link} "
    mail.send(msg)


@app.route('/recover/validate/<token>', methods=['GET', 'POST'])
def validate_token(token):
    try:
        email = s.loads(token, salt='recover-email', max_age=600)
    except SignatureExpired:
        return "The token expired!"

    form = new_password_form.NewPasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        #our_user = session.query(User).filter_by(email=email).first()
        our_user = User.query.filter_by(email=email).first()
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        our_user.password = password
        db.session.commit()
        return redirect(url_for('sign_in'))
    return render_template('new_password.html', form=form)
