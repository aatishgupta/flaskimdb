from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://imdb:^YHNnhy6@localhost:3306/imdb'
    db.init_app(app)
    migration = Migrate(app, db)
    migration.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from app.users.routes import users
    from app.movies.routes import movie_blueprint
    app.register_blueprint(users)
    app.register_blueprint(movie_blueprint)
    return app

