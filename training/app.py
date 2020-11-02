from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object('training.config.DevelopmentConfig')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)
