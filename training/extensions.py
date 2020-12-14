from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
migrate = Migrate()
marshmallow = Marshmallow()
