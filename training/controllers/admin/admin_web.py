from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from training.models.users import User
from training.app import db, app, bcrypt

admin = Admin(app, name='Users admin', template_mode='bootstrap3')


class MyModelView(ModelView):
    column_list = ('id', 'username', 'password', 'email', 'mail_validation', 'created_at')
    form_columns = ('id', 'username', 'password', 'email', 'created_at')

    def on_model_change(self, form, User, is_created=False):
        User.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')


admin.add_view(MyModelView(User, db.session))
