from wtforms import Form, BooleanField, StringField, validators


class SendEmailForm(Form):
    email_sender = StringField('Email sender', [validators.DataRequired()])
    email_recipient = StringField('Email recipient', [validators.DataRequired()])
    message_body = StringField('Message', [validators.DataRequired()])
    send_now = BooleanField('Shall we send it now?', default=False)
