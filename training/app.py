import os
from flask import Flask, render_template
from redis import Redis
import rq
from dotenv import load_dotenv
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Remember, FLASK_ENV=development is set in .env
    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object('training.config.DevelopmentConfig')
    elif os.environ.get('FLASK_ENV') == 'testing':
        app.config.from_object('training.config.TestConfig')
    elif os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object('training.config.ProductionConfig')
    else:
        app.config.from_object('training.config.DevelopmentConfig')

    app.secret_key = os.environ.get('SECRET_KEY')

    from training.extensions import db
    db.init_app(app)

    from training.extensions import bcrypt
    bcrypt.init_app(app)

    from training.extensions import mail
    mail.init_app(app)

    from training.extensions import migrate
    migrate.init_app(app, db)

    app.redis = Redis.from_url(os.environ.get('REDIS_URL'))
    app.task_queue = rq.Queue('my-app-tasks', connection=app.redis)

    @app.route('/')
    def first_page():
        return render_template("nothing.html"), 200

    # Blueprints
    from training.controllers.auth import bp
    from training.controllers.basic_funcionalities import bp as bp2
    from training.controllers.mail import bp as bp3
    from training.controllers.api import bp as bp4
    app.register_blueprint(bp)
    app.register_blueprint(bp2)
    app.register_blueprint(bp3)
    app.register_blueprint(bp4)

    # Admin
    from flask_admin import Admin
    admin = Admin(app, name='Users admin', template_mode='bootstrap3')
    from training.controllers.admin.admin_web import UserModelView
    from training.models.users import User
    admin.add_view(UserModelView(User, db.session))

    with app.app_context():
        db.create_all()
        db.session.commit()

    return app


app = create_app()
