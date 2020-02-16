from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from app import login_manager
from flask_migrate import Migrate
from flask_serialize import FlaskSerializeMixin
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://imdb:^YHNnhy6@localhost:3306/imdb'
db = SQLAlchemy(app)
ma = Marshmallow(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get((int(user_id)))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    # A => Admin #U => Normal User
    role = db.Column(db.String(1), default='U')
    password = db.Column(db.String(60), nullable=False)
    """
     one to many relationship
    """
    movie = relationship("Movie")
    comment = relationship("MovieComment")
    """
        one to one relationship
    """
    movierating = relationship("MovieRating", uselist=False, back_populates="user")


class Movie(db.Model,FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    rating = relationship("MovieRating")
    comment = relationship("MovieComment")


class MovieRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="movierating")


class MovieComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(50), nullable=False)
    movie_id = db.Column(db.Integer, ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    class Meta:
        def __repr__(self):
            return self.comment

        def __repr__(self):
            return self.comment

class UserSchema(ma.ModelSchema):
    class Meta:
        model=User
class MovieSchema(ma.ModelSchema):
    class Meta:
        model=Movie

class MovieRatingSchema(ma.ModelSchema):
    class Meta:
        model=MovieRating
class MovieCommentSchema(ma.ModelSchema):
    class Meta:
        model=MovieComment
        fields=['comment']

