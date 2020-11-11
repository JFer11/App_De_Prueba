import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# environment can only take these values: "DevelopmentConfig", "ProductionConfig", "TestConfig"
#environment = os.environ.get('FLASK_ENV_TYPE', 'DevelopmentConfig')
#app.config.from_object('training.config.' + str(environment))
app.config.from_object('training.config.DevelopmentConfig')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)
