from flask import Blueprint, request, render_template, url_for, redirect, current_app, copy_current_request_context
from flask_mail import Message
from itsdangerous import SignatureExpired

from training.controllers.forms import new_password_form, recover_form, send_email_form
from training.extensions import mail, bcrypt
from training.models.users import User
from training.extensions import db
from training.utils.common_variables import serializer

bp = Blueprint('mail', __name__)


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
            return "The email {} was already validated.".format(our_user.username), 202
        else:
            our_user.mail_validation = True
            db.session.commit()
            return "Email from user {} was successfully validated.".format(our_user.username), 200


@bp.route('/send/email', methods=['GET', 'POST'])           #
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
            return render_template('email_form_template.html', form=form, sended=True), 204
        else:
            current_app.task_queue.enqueue('training.background_tasks.tasks.send_email_function', msg)
            return render_template('email_form_template.html', form=form, sended=True), 200

    return render_template('email_form_template.html', form=form), 200


def send_token_to_email(email):
    token = serializer.dumps(email, salt='recover-email')
    msg = Message('Recover Email', sender='no_reply@system.com', recipients=[email])
    link = url_for('mail.validate_token', token=token, _external=True)
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
        email = serializer.loads(token, salt='recover-email', max_age=600)
    except SignatureExpired:
        return "The token expired!"

    form = new_password_form.NewPasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        our_user = User.query.filter_by(email=email).first()
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        our_user.password = password
        db.session.commit()
        return redirect(url_for('auth.sign_in'))
    return render_template('new_password.html', form=form)
