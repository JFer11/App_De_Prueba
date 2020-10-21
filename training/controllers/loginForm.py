from wtforms import Form, BooleanField, StringField, PasswordField, validators

class loginWTForm(Form):
    username = StringField('Username', [
        validators.Length(min=4, max=25),
        validators.DataRequired()
    ])
    password = PasswordField('Insert Password', [
        validators.DataRequired()
    ])