import os
from flask import Flask, render_template
from redis import Redis
import rq
from flask_swagger_ui import get_swaggerui_blueprint
from flask import send_from_directory
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

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    SWAGGER_URL = '/swagger'  # URL of the swagger UI
    API_URL = '/static/swagger.json'  # URL of the swagger json
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Training App'
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Blueprints
    from training.controllers.auth import bp
    from training.controllers.basic_funcionalities import bp as bp2
    from training.controllers.mail import bp as bp3
    from training.controllers.api import bp as bp4
    from training.controllers.user import bp as bp5
    from training.controllers.user import bp as bp6
    from training.controllers.articles import bp as bp7
    app.register_blueprint(bp)
    app.register_blueprint(bp2)
    app.register_blueprint(bp3)
    app.register_blueprint(bp4)
    app.register_blueprint(bp5)
    app.register_blueprint(bp6)
    app.register_blueprint(bp7)

    # Admin
    from flask_admin import Admin
    admin = Admin(app, name='Users admin', template_mode='bootstrap3')
    from training.controllers.admin.admin_web import UserModelView
    from training.models.users import User
    admin.add_view(UserModelView(User, db.session))

    with app.app_context():
        db.create_all()
        db.session.commit()

    print("Bien!")

    return app


app = create_app()
