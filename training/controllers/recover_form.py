from wtforms import Form, StringField, validators


class RecoverForm(Form):
    email = StringField('Email Para Recuperar', [
        validators.DataRequired()
    ])
