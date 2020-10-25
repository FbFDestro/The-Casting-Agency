import os
from flask import Flask, request, abort, jsonify
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

    @ app.after_request
    def after_request(response):

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @ app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"
        return greeting

    @ app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @ app.route('/movies')
    def get_movies():
        """Get all movies route"""

        movies = Movie.query.all()

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies],
        }), 200

    # Defines an endpoint that informs the correct url for login
    @ app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        url = (f'https://{AUTH0_DOMAIN}/authorize'
               f'?audience={AUTH0_AUDIENCE}'
               f'&response_type=token&client_id='
               f'{AUTH0_CLIENT_ID}&redirect_uri='
               f'{AUTH0_CALLBACK_URL}')
        return jsonify({
            'login_url': url
        })

    # Handles response from token endpoint
    @app.route('/callback')
    def callback_handling():

        print(res)

        # Store the user information in flask session.
        return jsonify({
            'res': res
        })

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
