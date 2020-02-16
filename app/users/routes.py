from flask import redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user
from flask import jsonify
from app import db, bcrypt
from models import User, Movie, MovieRating, MovieSchema, MovieComment
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        data = {'status': False, 'msg': 'Please logged out to create new user'}
        return jsonify(data), 400
    # 400 is for bad request
    # request.args.get
    roles = ['A', 'U']
    error_dict = {
        "username": "Username can't be empyt",
        "duplicate_username": "Username already exist",
        "password": "Password can't be empty",
        "role": "Invalid role provided"
    }

    args = request.args
    if not args:
        return jsonify({'status': False, 'msg': 'Invalid argument passed'})

    username = args['username']
    password = args['password']
    role = args['role']
    error = None
    if not username:
        error = error_dict['username']
    elif not password:
        error = error_dict['password']
    elif role not in roles:
        error = error_dict['role']
    if error:
        data = {'status': False, 'msg': error}
        return jsonify(data), 422

    hashed_password = bcrypt.generate_password_hash(password)
    user = User(username=username, role=args['role'], password=hashed_password)

    db.session.add(user)
    try:
        db.session.commit()
        return jsonify({'status': True, 'msg': '%s user registered successfully' % (username)}), 200
    except IntegrityError:
        db.session.rollback()
        data = {'status': False, 'msg': error_dict['duplicate_username']}
        return jsonify(data), 422
        # error, there already


@users.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return jsonify({'status': False, 'msg': 'User is already logged in'})
    args = request.args
    user = User.query.filter_by(username=args['username']).first()
    if user and bcrypt.check_password_hash(user.password, args['password']):
        login_user(user, remember=user)
        session['role'] = user.role
        session['user_id'] = user.id
        return jsonify({'status': True, 'msg': 'Login successful'}), 200
    else:
        return jsonify({'status': False, 'msg': 'Login Unsuccessful. Please check username and password'}), 422


@users.route("/logout")
def logout():
    logout_user()
    return jsonify({'status': True, 'msg': 'user logged out successfully'})


@users.route('/users/movies')
def user_movies():
    if not current_user.is_authenticated:
        return jsonify({'status': False, 'msg': 'Please login see details'})
    movie_schema = MovieSchema(many=True)
    movies_list = Movie.query.filter(
        or_(and_(MovieRating.user_id == session['user_id'],MovieRating.movie_id == Movie.id),
             and_(MovieComment.user_id == session['user_id'],MovieComment.movie_id == Movie.id)))
    output = movie_schema.dump(movies_list)
    return jsonify(output)
