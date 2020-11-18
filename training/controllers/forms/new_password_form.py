from wtforms import Form, PasswordField, validators


class NewPasswordForm(Form):
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=4, max=25),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [
        validators.DataRequired()
    ])
