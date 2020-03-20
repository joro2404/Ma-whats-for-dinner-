from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'heyyyyvsaucehere'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/vesko/Desktop/gesko/Ma-whats-for-dinner-/app/gesko.db'
    # db.init_app(app)

    login_manger = LoginManager()
    login_manger.login_view = 'auth.login'
    login_manger.init_app(app)

    from .user import User

    @login_manger.user_loader
    def load_user(id):
        print(id)
        return User.find_by_id(id)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

