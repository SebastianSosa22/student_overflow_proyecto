from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .models import User
    from .routes import main
    app.register_blueprint(main)

    return app


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('main.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
