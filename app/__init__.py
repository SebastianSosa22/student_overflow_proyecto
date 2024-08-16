from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    _init_extensions(app)
    _register_blueprints(app)
    _register_login_manager(app)

    return app


def _init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


def _register_blueprints(app):
    from .routes import main
    app.register_blueprint(main)


def _register_login_manager(app):
    from .models import User

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('main.login'))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
