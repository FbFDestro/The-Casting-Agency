import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor


assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx2NWY2eG5YVHdNcV9EUEJWTDdRMSJ9.eyJpc3MiOiJodHRwczovL2ZiZmRlc3Ryby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5NTExNDc4ZTM2YWMwMDY5ZThiYTdmIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2MDM2MTY1NTIsImV4cCI6MTYwMzcwMjk1MiwiYXpwIjoieTBHbnN3djFBb1FDY3l1MWV1d0hVWUxBd25NWnJjVVoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.dwR5Fez_JHxEXBio8dKPXMBgVHGwwMGlhQNjqJyOVfBuf5AemfRFKJNpQGMT5iDe4lkB-0Up4wPDju6CwDitCyr-qVDCz_vN3ro4ARabbOe314XmaaMXi6eFR0O9ERU2ZOrKIuKmikeu0A5QN4G7lw80z5ezizc9h_CXMdIb486wRpql_JBUHQcxhfPsAhit2QYFWCM3dkipVhG2cRHhwxffPBTE0bSest4LRKtSZSWTRi-pBkM5fGVYydWFM0jY2wq93Qcyohq4DfzRHlW7P4YxyYEGsOLeywMviB5e2d7RzmeYDlYgrKjKkK9-Ua_VKnjtIO8tpVxIY1GmpUHNjg'
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx2NWY2eG5YVHdNcV9EUEJWTDdRMSJ9.eyJpc3MiOiJodHRwczovL2ZiZmRlc3Ryby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5NTExNzllN2JmNTUwMDZmZGZhYjQ3IiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2MDM2MTY2MTMsImV4cCI6MTYwMzcwMzAxMywiYXpwIjoieTBHbnN3djFBb1FDY3l1MWV1d0hVWUxBd25NWnJjVVoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yZXMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.eAuBNq2RZOisXJfSoulSq4WWWOZXuq6rvgDt3vUj_Mkq7Xg3RpGavqOAeGkODhTsbeOOsvMuw6QnR2BGJliHostUQ1mw1rwinSFPw62O1uXMCIgV93T1q0xtTWkyzxtyLotXg5yvTiJ-taifsfAFiVjdTWlyA56MJK7xJBGuG5bEJ9V3NRO-UZ36VRjuU_JCdvd-yFETjBTllbyT1LloUiiFem5ybH0OZvWdfMI_HJkdsBc1iCQy41MEks2nUAyhKMdwndKEmJDWpJIZUh2Yqde6511xcbwBaF0UQnf0F7KaYFQcKQ3mR8NxRNNQrSJrUvplIAwTBhXOXMoZBS5dJg'
producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imx2NWY2eG5YVHdNcV9EUEJWTDdRMSJ9.eyJpc3MiOiJodHRwczovL2ZiZmRlc3Ryby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5NTExOWZlN2JmNTUwMDZmZGZhYjRiIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2MDM2MTY2NDgsImV4cCI6MTYwMzcwMzA0OCwiYXpwIjoieTBHbnN3djFBb1FDY3l1MWV1d0hVWUxBd25NWnJjVVoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcmVzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.UHZZGu3mh7JGhdRgp6MK_gDjEEzfEbtQLzS3yJZzW4Rfyuxt2kBMvE6FKgkqQxxtaUQrpe3LI46QvWqnn0SLSQaYn5TxKNaCpXiMYUgRF_cGyRMEEuwtf_TpS9GERFTQ0fv2TXcU4aBo_ugPmCiSyIQDj1rr8aJS3I3KycjRZLWv2eRi339j_S5ksbvkquksuPh-P5DWCigX_fs1Zo2YQUWMQBp78Y-RKL5XanO1N69BuUAe-P7A0R18dzPkplhwXgggzR37whaKUJ2M36yH195Z0-x0PvfGJlC51MEGJpXC_zFclBbnlhLl-F-StfJ_XZ0XTlRLQ9IQ8altLuMmAg'


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
            '/movies/1',
            headers=set_auth_header('assistant')
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['id'], 1)

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


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
