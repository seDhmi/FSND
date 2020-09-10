import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import db_drop_and_create_all, db, setup_db
from database.models import Movie, Actor, Show
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    setup_db(app)

    db_drop_and_create_all()

    # CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods','GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return f'hello capstone!'

    # Retrive All Shows
    @app.route('/shows')
    def retrive_all_shows():
        data = Show.query.all()
        shows = list(map(Show.get_show, data))
        if shows is None or len(shows) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'shows': shows
        })

    # Add Shows
    @app.route('/shows', methods=['POST'])
    def add_new_show():
        body = request.get_json()
        if body is None:
            abort(404)
        actor_id = body.get('actor_id', None)
        movie_id = body.get('movie_id', None)

        try:
            new_show = Show(actor_id=actor_id, movie_id=movie_id)
            new_show.insert()
            return jsonify({
                'success': True,
                'new show': [new_show.get_show()]
            })

        except Exception:
            abort(422)


        # Actors

    # Retrive All Actors.
    @app.route('/actors')
    @requires_auth('get:actors')
    def retrive_actors(payload):
        actors = Actor.query.all()
        if not actors:
            abort(404)
        formatActors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'Actors': formatActors
        })

    # Add Actors.
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actors(payload):
        body = request.get_json()
        if body is None:
            abort(404)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()
            return jsonify({
                'success': True,
                'actors': [new_actor.get_actor()]
            })

        except Exception:
            abort(422)

    # Retrive Actors.
    @app.route('/actors/<int:actor_id>/movies')
    def retrive_movies_of_an_actor(actor_id):
        data = Show.query.filter(Show.actor_id == actor_id).all()
        data = db.session.execute(
            '''select movie_id from shows where
            actor_id=''' + str(actor_id)).fetchall()

        for d in data:
            movies = Movie.query.get(d.movie_id)
            print(movies)
        if movies is None or len(movies) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': movies
        })

        # Actors

    # Delete an Actor.
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor_by_id(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor_id
            }), 200

        except:
            abort(422)

    # Retrive All Movies.
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrive_movies(payload):

        movies = Movie.query.all()
        if not movies:
            abort(404)
        formatMovies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formatMovies
        })

    # Add Movie.
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        body = request.get_json()
        if 'title' not in body:
            abort(404)
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        try:
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()
            return jsonify({
                'success': True,
                'movies': [new_movie.get_movie()]
            })
        except Exception:
            abort(422)

    # Edit Movie.
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload, movie_id):
        body = request.get_json()
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)
            if 'title' in body:
                movie.title = body.get('title', None)
            if 'release_data' in body:
                movie.release_data = body.get('release_data', None)

            movie.update()
            format_movie = [movie.format()]

            return jsonify({
                'success': True,
                'movie': format_movie
            }), 200
        except Exception:
            abort(422)

    # Delete Movie.
    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id
            }), 200
            
        except:
            abort(422)

    # Error Handling.

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)