from wtforms import FileField, Form, validators


class UploadImageForm(Form):
    image = FileField('Avatar', [validators.DataRequired()])
