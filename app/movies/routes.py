from flask import request, Blueprint, session
from flask_login import current_user
from flask import jsonify
from models import Movie, MovieSchema, MovieComment, MovieRating
import requests, shutil, random, time, string
from app import db
import os, sys
from sqlalchemy import func

movie_blueprint = Blueprint('movie', __name__)


@movie_blueprint.route('/movie', methods=['POST', 'GET'])
def movies():
    if not current_user.is_authenticated:
        data = {'status': False, 'msg': 'please login to upload movie details'}
        return jsonify(data), 400
    if session['role'] != 'A':
        # Unauthorized  user
        return jsonify({'status': False, 'msg': 'Unauthorized  user'}), 401
    error_dict = {
        "title": "Title can't be empty",
        "description": "Description can't be empty",
        "release_date": "Release Date can't be empty",
        "image_file": "Image url can't empty"
    }
    args = request.args
    error = None
    if args['title'] == '':
        error = error_dict['title']
    elif args['description'] == '':
        error = error_dict['description']
    elif args['release_date'] == '':
        error = args['release_date']
    elif args['image_file'] == '':
        error = error_dict['image_file']

    if error:
        return jsonify({'status': False, 'msg': error})

    ext = args['image_file'].split('.')
    CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))
    UPLOAD_FOLDER = CURRENT_FOLDER + '\\..\\static\\'
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    if ext[-1].lower() not in ALLOWED_EXTENSIONS:
        return jsonify({'status': False, 'msg': 'invalid image file extension ' + ext[-1]})

    # r = requests.get('https://requests.readthedocs.io/en/master/_static/requests-sidebar.jpg', stream=True)
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=50)) + str(time.time())
    image = res + '.' + ext[-1]

    try:
        r = requests.get(args['image_file'], stream=True)
    except ConnectionError as ex:
        return jsonify({'status': False, 'msg': 'Image is not accessible'})
    if r.status_code == 200:
        with open(UPLOAD_FOLDER + image, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(args['release_date'], 10)))
    movie = Movie(title=args['title'], description=args['description'], release_date=date, image_file=image,
                  user_id=session['user_id'])
    db.session.add(movie)
    try:
        db.session.commit()
        return jsonify({'status': True, 'msg': '%s added successfully' % (args['title'])}), 200
    except ValueError:
        db.session.rollback()
        data = {'status': False, 'msg': 'Error while adding movie details' + sys.exc_info()[0]}
        return jsonify(data), 422


@movie_blueprint.route('/movie/search/<string:keyword>', methods=['GET'])
def search_movies(keyword):
    movie_schema = MovieSchema(many=True)
    search = "%{}%".format(keyword)
    # movies_list = Movie.query(db.func.avg(MovieRating.star),db.func.count(MovieComment.id)).filter(Movie.title.like(search)).group_by(Movie.id).group_by(User.id).all()
    #movies_list = Movie.query(db.func.avg(MovieRating.star)).join(MovieRating).group_by(User.id).all()
    movies_list=db.session.query(func.avg(MovieRating.star),func.count(MovieComment.id)).join(MovieRating).join(MovieComment).group_by(Movie.id).group_by(Movie.user_id).filter(Movie.title.like(search)).all()
    output = movie_schema.dump(movies_list)
    return jsonify(output)


@movie_blueprint.route('/movie/<int:movie_id>/rating', methods=['POST', 'GET'])
def rate_movie(movie_id):
    if not current_user.is_authenticated:
        data = {'status': False, 'msg': 'please login to rate movie'}
        return jsonify(data), 400
    args = request.args
    if int(args['rating']) > 10 or int(args['rating']) < 0:
        return jsonify({'status': False, 'msg': 'Invalid rating value'})
    rating_exist = MovieRating.query.filter_by(movie_id=movie_id, user_id=session['user_id']).first()
    # (MovieRating.movie_id == ) & (MovieRating.user_id == session['user_id'])).first()
    if rating_exist:
        rating_exist.star = args['rating']
    else:
        movie_rating = MovieRating(star=args['rating'], user_id=session['user_id'], movie_id=movie_id)
        db.session.add(movie_rating)
    try:
        db.session.commit()
        return jsonify({'status': True, 'msg': 'Movie with id %d is rated successfully' % (movie_id)})
    except:
        return jsonify(
            {'status': False, 'msg': 'Error while rating movie with id %d' % (movie_id) + str(sys.exc_info())})


@movie_blueprint.route('/movie/<int:movie_id>/comment', methods=['POST', 'GET'])
def comment_movie(movie_id):
    if not current_user.is_authenticated:
        data = {'status': False, 'msg': 'please login to rate movie'}
        return jsonify(data), 400
    args = request.args
    if not args['comment'] or args['comment'] == '':
        return jsonify({'status': False, 'msg': 'Please provide comment'})

    movie_comment = MovieComment(comment=args['comment'], user_id=session['user_id'], movie_id=movie_id)
    db.session.add(movie_comment)

    try:
        db.session.commit()
        return jsonify({'status': True, 'msg': 'Movie with id %d is commented successfully' % movie_id})
    except:
        return jsonify(
            {'status': False, 'msg': 'Error while commenting on movie with id %d' % movie_id})
