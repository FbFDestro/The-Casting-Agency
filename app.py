import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth


AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_BASE_URL = 'https://' + os.environ['AUTH0_DOMAIN']
AUTH0_AUDIENCE = os.environ['AUTH0_AUDIENCE']


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @ app.route('/')
    def get_greeting():
        return render_template("index.html")

    #  MOVIES

    # Get list of movies
    @ app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        """Get all movies route"""

        movies = Movie.query.all()

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies],
        }), 200

    # Get a movie
    @app.route('/movies/<int:id>')
    @requires_auth('get:movies')
    def get_movie_by_id(jwt, id):
        movie = Movie.query.get(id)

        # return 404 if there is no movie with id
        if movie is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movie': movie.format(),
            }), 200

    # Add a movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):
        data = request.get_json()
        title = data.get('title', None)
        release_date = data.get('release_date', None)

        # return 400 if title or release date is empty
        if title is None or release_date is None:
            abort(400)

        movie = Movie(title=title, release_date=release_date)

        try:
            movie.insert()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 201
        except Exception:
            abort(500)

    # modify a movie
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):

        data = request.get_json()
        title = data.get('title', None)
        release_date = data.get('release_date', None)

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        if title is None or release_date is None:
            abort(400)

        movie.title = title
        movie.release_date = release_date

        try:
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception:
            abort(500)

    # Delete movie
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        """Delete a movie route"""
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception:
            db.session.rollback()
            abort(500)

    # Defines an endpoint that informs the correct url for login

    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        url = (f'https://{AUTH0_DOMAIN}/authorize'
               f'?audience={AUTH0_AUDIENCE}'
               f'&response_type=token&client_id='
               f'{AUTH0_CLIENT_ID}&redirect_uri='
               f'{AUTH0_CALLBACK_URL}')
        return jsonify({
            'login_url': url
        })

    # Actors

    # Get a list of actors
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):

        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors],
        }), 200

    # Get an actor by id
    @app.route('/actors/<int:id>')
    @requires_auth('get:actors')
    def get_actor_by_id(jwt, id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format(),
            }), 200

    # Add an actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(jwt):

        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        actor = Actor(name=name, age=age, gender=gender)

        if name is None or age is None or gender is None:
            abort(400)

        try:
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201
        except Exception:
            abort(500)

    # Update an actor
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)

        if name is None or age is None or gender is None:
            abort(400)

        actor.name = name
        actor.age = age
        actor.gender = gender

        try:
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
        except Exception:
            abort(500)

    # Delete an actor
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception:
            db.session.rollback()
            abort(500)

    # Handles response from token endpoint
    @app.route('/callback')
    def callback_handling():

        return render_template('logged.html')

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
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

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
