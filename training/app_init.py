from flask import Flask
from dotenv import load_dotenv
load_dotenv()
from flask_bcrypt import Bcrypt
from training.main import init_db
from flask_mail import Mail, Message
import os

app = Flask(__name__)
from training.controllers.all_controllers import *
bcrypt = Bcrypt(app)
app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEBUG'] = False


mail = Mail(app)

def main():
    init_db()
    app.run(port=8000, debug=True)


if __name__ == '__main__':
    main()






from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from training.models.users import User

admin = Admin(app, name='Users admin', template_mode='bootstrap3')
from training.main import session

class MyModelView(ModelView):
    column_list = ('id', 'username', 'password', 'email', 'mail_validation', 'created_at')
    form_columns = ('id', 'username', 'password', 'email', 'created_at')

    def on_model_change(self, form, User, is_created=False):
        User.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

admin.add_view(MyModelView(User, session))
