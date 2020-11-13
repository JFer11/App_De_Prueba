from flask import Blueprint, request, render_template, url_for, redirect
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

from training.controllers.forms import new_password_form, recover_form, send_email_form
from training.extensions import mail, bcrypt
from training.models.users import User
from training.extensions import db

""" 
    Problema original, solucionado. Sin embargo, estaria bueno discutir la solucion. Se relaciona con las background tasks para enviar mails por redis, ya que como 
    me habias dicho Joaco, tenia que buscar una amanera de pasarle el app_context a redis. 

    Mi problema original era el siguiente:
    Este modulo es llamado cuando se esta a la mitad e create_app.
    Recordemos que app, es creado como variable global al final de correrse create_app y aqui estamos en la mitad del flujo.
    Por lo que cuando importamos "from training.background_tasks.tasks import send_email_async" este importa app desde app.py, pero aun no esta creada ya que
    nos encontrabamos a mitad del flujo de create_app, y recordemos que app se crea cuando termina create_app. Ergo, ERROR
    
    Solucion:
    Crear la app en 2 pasos. Se hace app=create_app(), y en create_app se inicializa, importa y crea todo salvo este modulo.
    Luego, se llama a una funcion modifications(), que importa solo este modulo y se agrega el blueprint a la app ya existente.
    
    Entonces al importarse este modulo, se comienza a correr, y en determinado momento se importa app desde aca. 
    Pero ya existe una app, por lo que no hay problema en ir a buscarla a app.py. Y se le puede dar el app_context a redis.
"""


s = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

bp = Blueprint('name3', __name__)

#from training.background_tasks.tasks import send_email_async, send_email_function
from training.app import app


# Test mail
@bp.route('/mail')
def mail_test():
    email = 'donnetta7@adriveriep.com'
    msg = Message('Confirm Email', sender='anthony@prettyprinted.com', recipients=[email])
    msg.body = "Bienvenido"
    mail.send(msg)
    return "0", 200


# Validation process (DOES NOT SEND ANY EMAIL)
@bp.route('/mail/validation/<string:username>')
def email_verification(username):
    our_user = User.query.filter_by(id=username).first()

    if our_user is None:
        return "User not exist", 450
    else:
        if our_user.mail_validation:
            return "The email {} was already validated.".format(our_user.username), 205
        else:
            our_user.mail_validation = True
            db.session.commit()
            return "Email from user {} was successfully validated.".format(our_user.username), 200


# Recover password process
def send_email_function(msg):
    with app.app_context():
        # mail.suppress = True
        mail.send(msg)


def send_email_async(msg):
    job = app.task_queue.enqueue(send_email_function, msg)
    job.get_id()


@bp.route('/send/email', methods=['GET', 'POST'])
def send_email():
    form = send_email_form.SendEmailForm(request.form)

    if request.method == 'POST':
        email_sender = request.form['email_sender']
        email_recipient = request.form['email_recipient']
        message_body = request.form['message_body']
        msg = Message('Recover your account', sender=email_sender, recipients=[email_recipient])

        msg.body = message_body
        if 'send_now' in request.form:
            mail.send(msg)
            return render_template('email_form_template.html', form=form, sended=True)
        else:
            send_email_async(msg)
            return render_template('email_form_template.html', form=form, sended=True)
    return render_template('email_form_template.html', form=form)


def send_token_to_email(email):
    token = s.dumps(email, salt='recover-email')
    msg = Message('Recover Email', sender='no_reply@system.com', recipients=[email])
    link = url_for('validate_token', token=token, _external=True)
    msg.body = f"Haga click aqui para recuperar su cuenta: {link} "
    mail.send(msg)


@bp.route('/recover', methods=['GET', 'POST'])
def recover_account():
    form = recover_form.RecoverForm()

    if request.method == 'POST':
        our_user = User.query.filter_by(email=request.form['email']).first()
        if our_user is not None:
            send_token_to_email(request.form['email'])
            return render_template('recover.html', form=form, accepted_request=True)
        else:
            return render_template('recover.html', form=form, accepted_request=True)

    return render_template('recover.html', form=form)


@bp.route('/recover/validate/<token>', methods=['GET', 'POST'])
def validate_token(token):
    try:
        email = s.loads(token, salt='recover-email', max_age=600)
    except SignatureExpired:
        return "The token expired!"

    form = new_password_form.NewPasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        our_user = User.query.filter_by(email=email).first()
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        our_user.password = password
        db.session.commit()
        return redirect(url_for('sign_in'))
    return render_template('new_password.html', form=form)
