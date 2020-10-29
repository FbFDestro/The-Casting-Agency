import os
import unittest
import json

from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor


assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx2NWY2eG5YVHdNcV9EUEJWTDdRMSJ9.eyJpc3MiOiJodHRwczovL2ZiZmRlc3Ryby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5NTExNDc4ZTM2YWMwMDY5ZThiYTdmIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2MDM5NDk4MjcsImV4cCI6MTYwNDAzNjIyNywiYXpwIjoieTBHbnN3djFBb1FDY3l1MWV1d0hVWUxBd25NWnJjVVoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.0BYKIj23dS98Paux9DCPiECYGV9db9wE4IlItf_gTcMO_pTssRvwduzF5qjJ47lyb9q8c5nyL8NbzWWy3Vhh769SjztLdS8tTEjeAQ1mfWkEMoLPZW2m-KxuXZIYQAWPEJYqZFtl_6BSXl52LKWyDQsC7x0wKNMtbhGzhhcMdqILjdn0XbIi5KyTXfPIskpaj0EmR-pPOtp4RK60iSOAJpHdPeN7S4P8OaGaMX293eQsb_4PbnGcG59nHmF-Jqif3UpxlS1Hr5Wcw5LpCNQzygQp_Tyavob2OrZR5ZhalNl1o77MHxdLVelMIvD0b1UQOQjsw6cRHhc0Qkh-fX8mqA'
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx2NWY2eG5YVHdNcV9EUEJWTDdRMSJ9.eyJpc3MiOiJodHRwczovL2ZiZmRlc3Ryby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5NTExNzllN2JmNTUwMDZmZGZhYjQ3IiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2MDM5NDk4NTgsImV4cCI6MTYwNDAzNjI1OCwiYXpwIjoieTBHbnN3djFBb1FDY3l1MWV1d0hVWUxBd25NWnJjVVoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.p348fGE0SwLDwEEI8HR-vrRMoeeloie8suZARrTZKSzwT5XLmO2piSNliItxBSbwuWGjlnumuwlMEFmWl06tgipzgG1EQ-XadefiNi-1pKB6a_edombc0xeu3Xtt--p_1_XWeXTqiM9Xq8AVbJGajEYgFek0BRfr9zY0vehUudUz82g7l0qm2i0EzRbjN7kq2V1K1i0UXPaWGHV68JcCemyy5su2Zx6PUmecTPPDl_JR4o6Aq7y6cWrkIBsGjkgG3CqXIv-yUCZBWya_n7i_-bwpFJQBPk6EvFssa17L9D353xaePiX3maD86LTFEOx5jSgP7QQMKUaQl5yBIvwsTw'
producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx2NWY2eG5YVHdNcV9EUEJWTDdRMSJ9.eyJpc3MiOiJodHRwczovL2ZiZmRlc3Ryby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5NTExOWZlN2JmNTUwMDZmZGZhYjRiIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2MDM5NTAwODIsImV4cCI6MTYwNDAzNjQ4MiwiYXpwIjoieTBHbnN3djFBb1FDY3l1MWV1d0hVWUxBd25NWnJjVVoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.xeHPOheQkmxoFqOpkKk2TALSeTLRZyfp9XP2Om8L8UMyh3rRCVsOxHQq9H3eheboM50v44YK1YQ9_vw4nJryXio5atS5K_DzlF1-nBdj4jplwXkz17D3zmxeATsd4LGWuOXrtHC-oIysVjYLriQpxPWjKUqOSF3aiz1wJhFrVVbY9RXR6Jxn_QqTbcW71gb-ZFsesOgZvAS3gPF_PuuOlP5DHw4Y3DiXxEd46jVF8AV083oFCQDV4T0p8P_BoRbm950E0g43PryuVtGp-W3YcFUFxAc_b80WS67O1q2n2k6swQzWRxvdv6RgTJl9auuMoRlzZ8_S5bGPPAlz2z-gXg'


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
