import os
import unittest
import json

from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor

# Tokens may need to be updated due to expiration
# Instructions are provided on the index page)
assistant_token = os.environ['ASSISTAN_TOKEN']
director_token = os.environ['DIRECTOR_TOKEN']
producer_token = os.environ['PRODUCER_TOKEN']


def set_auth_header(role):
    if role == 'assistant':
        return {
            'Authorization': f'Bearer {assistant_token}'
        }
    elif role == 'director':
        return {'Authorization': f'Bearer {director_token}'}
    elif role == 'producer':
        return {'Authorization': f'Bearer {producer_token}'}


class CastingAgencyTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.test_movie = {
            'title': 'Test Movie',
            'release_date': '2222-11-11',
        }
        self.test_actor = {
            'name': 'New name',
            'age': 66, "gender": "male"
        }

        # A TEST DATABASE COULD BE USED
        self.database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/2',
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['id'], 2)

    def test_404_get_movie_by_id(self):
        response = self.client().get(
            '/movies/666',
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Test Movie')

    def test_400_post_movie(self):
        response = self.client().post(
            '/movies',
            json={},
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_401_post_movie_unauthorized(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers=set_auth_header('director')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_patch_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'New title', 'release_date': "2001-01-01"},
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'New title')

    def test_400_patch_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={},
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_401_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies/2',
            json=self.test_movie,
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_404_patch_movie(self):
        response = self.client().patch(
            '/movies/666',
            json=self.test_movie,
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/1',
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_delete_movie(self):
        response = self.client().delete(
            '/movies/3',
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_404_delete_movie(self):
        response = self.client().delete(
            '/movies/666',
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/2',
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_get_actor_by_id(self):
        response = self.client().get(
            '/actors/666',
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json=self.test_actor,
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'New name')
        self.assertEqual(data['actor']['age'], 66)
        self.assertEqual(data['actor']['gender'], 'male')

    def test_400_post_actor(self):
        response = self.client().post(
            '/actors',
            json={},
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_401_post_actor_unauthorized(self):
        response = self.client().post(
            '/actors',
            json=self.test_actor,
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_patch_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'New name', 'age': 66, "gender": "female"},
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'New name')
        self.assertEqual(data['actor']['age'], 66)
        self.assertEqual(data['actor']['gender'], 'female')

        response = self.client().patch(
            '/actors/2',
            json={'name': 'Actor', 'age': 25, "gender": "female"},
            headers=set_auth_header('producer')
        )

    def test_400_patch_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={},
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_401_patch_actor_unauthorized(self):
        response = self.client().patch(
            '/actors/2',
            json=self.test_actor,
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_404_patch_actor(self):
        response = self.client().patch(
            '/actor/666',
            json=self.test_actor,
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/1',
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_404_delete_actor(self):
        response = self.client().delete(
            '/actors/666',
            headers=set_auth_header('producer')
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
