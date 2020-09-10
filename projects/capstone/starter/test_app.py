import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import db, db_drop_and_create_all, setup_db, Movie, Actor
from auth import AuthError, requires_auth

database_name = "capstone_test.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "postgres:///{}".format(os.path.join(project_dir, database_name))

casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdZVHlYTW9yNjNkd1pGQXFkd1JVXyJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLXNlZGhtaS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZTkzMTIyMDc2YTcwMDY3OGYxNWYyIiwiYXVkIjoiSW1hZ2UiLCJpYXQiOjE1OTkxNDE0OTUsImV4cCI6MTU5OTE0ODY5NSwiYXpwIjoiRHNJS1RNY3lwUU01WG44T2lXTHI5Q1c2S1piVVA0aEciLCJzY29wZSI6IiJ9.fOI99GpsZWiwu3L_yRyIc1fJoOUyRv5sRlS9CpVluiihMSzFeg_uH9F682lj9BbBRapseowCK9uheh7x18WgsJVqsGrRPgko_4mWxke0hXCQXmsK8jGDeeXByYapCBGorIPujRA4t35tsC3YxQwboadC7QuIajyjw_gtxvHKwIAKhXuGoAnmhCzEKcPa0iI_VdyGETvgjX3olVcF_XupvC4AJ8HuCNF9V-PpJ54qJ9zZzmQaRRFAvgTp6pdYTk4ib6EFWuhcfBRohUPAexyXvtYn31TG2oOAmbP-8zO5CW5_TKixUoRiuPGSAylfQD4ntnNMs5cBrcKrQ8ZmaJPtIA'
casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdZVHlYTW9yNjNkd1pGQXFkd1JVXyJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLXNlZGhtaS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZTkzODZjNjQ3OGIwMDY3ZDhhMWNiIiwiYXVkIjoiSW1hZ2UiLCJpYXQiOjE1OTkxNDEyNDMsImV4cCI6MTU5OTE0ODQ0MywiYXpwIjoiRHNJS1RNY3lwUU01WG44T2lXTHI5Q1c2S1piVVA0aEciLCJzY29wZSI6IiJ9.cTaR0Zbu9aqxglzBb7hYYz-HSGEc1aIwmhoNg11wBFVYANgddYRhJRzyym7X2rJqWkIbRzOTfYDYN2A2hH_xuD_re4DaIuIGzBVy5EHD3WwiA_3pKndPw2QUoP66ePLLYr5p7etDOFJOQ-oiX3-Fgz9bomc2Pa0biNcGmOQeTm8w_J_FHevEy8Y0SG-V5nAE7AIk3u6bGfzR0G7SMXMi3ORyoDysU3d-vultqayVSgq23bQ_wOQGL_C5wAF2oBIeelwZc0ESVa5Gs_jOk7P-MaWn97IdYl42Zzql4OzZgmnzgIpIh_mUa6S0gSQIRBafhQuoj97ZO7B0-wN2QMRH6g'
executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdZVHlYTW9yNjNkd1pGQXFkd1JVXyJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLXNlZGhtaS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZTg4MzIxNDYxNjEwMDZkMjU4NWQ3IiwiYXVkIjoiSW1hZ2UiLCJpYXQiOjE1OTkxNDAyNjEsImV4cCI6MTU5OTE0NzQ2MSwiYXpwIjoiRHNJS1RNY3lwUU01WG44T2lXTHI5Q1c2S1piVVA0aEciLCJzY29wZSI6IiJ9.RSUjdIH3QzutpYGNBJDX6nUxmLG7idBrdDMb_5G2wm6N3l2bm5wWeYOYgZzheGeS1QWMHe6CwJPJKpT-NgjQPNZ63Xla8XnvX__oVFRHVsteL9GC1GBNqrrcBm5H5Ui2gXSJnlafZzFkgJJ3r2TJ9Mhln4XXo4UKXFhoPVAO73Eciq6SDgrIbhe4HRyL7T7_PekTpzAknIFzelECjLNxdl_pnsPPiBCLFDZQjDtKaFrF1-yD9QIso1iYUosZYSX_Cbxa3qV_L6v6J745wrAWXrF9bsFjqUhUAsJmj9XfKmS7zJW3E2UfGUhh5MYDvZdUB3Z1ngVQ0Wu8kk9Nwhr2bg'


def setup_auth(role):
    JWT = ''
    if role == 'casting_assistant':
        JWT = casting_assistant_token
    elif role == 'casting_director':
        JWT = casting_director_token
    elif role == 'executive_producer':
        JWT = executive_producer_token

    return {
        "Content-Type": "application/json",
        'Authorization': 'Bearer {}'.format(JWT)
    }


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', '123', 'localhost:5432', self.database_name)

        self.casting_assistant = {
            'Content-Type': 'application/json', 'Authorization': casting_assistant_token}
        self.casting_director = {
            'Content-Type': 'application/json', 'Authorization': casting_director_token}
        self.executive_producer = {
            'Content-Type': 'application/json', 'Authorization': executive_producer_token}

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """ Executed after each test """
        pass

    # One test for success behavior of each endpoint
    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors', headers=setup_auth("casting_assistant"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_casting_director(self):
        res = self.client().get('/actors', headers=setup_auth("casting_director"))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_executive_producer(self):
        res = self.client().get('/actors', headers=setup_auth("executive_producer"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_update_actor_casting_director(self):
        actor = Actor(name='Maha', age=50, gendar='Female')
        actor.insert()
        actorId = actor.id
        res = self.client().patch(f'/actors/{actor.id}', json={
            'name': 'EDIT name', 'age': 10, 'gendar': 'female'}, headers=self.casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # One test for error behavior of each endpoint
    def test_401_post_actor_casting_assistant(self):
        res = self.client().post('/actors', json=self.new_actor, headers=setup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 401)

    def test_401_post_movie_casting_director(self):
        res = self.client().post('/movies', json=self.new_movie,headers=setup_auth('casting_director'))
        self.assertEqual(res.status_code, 401)
    
    def test_404_patch_actor_fail_executive_producer(self):
        res = self.client().patch('/actors/100', json={}, headers=setup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_403_delete_actor_casting_assistant(self):
        actor = Actor(name='Maha', age=10, gendar='Female')
        actor.insert()
        actorId = actor.id
        res = self.client().delete(f'/actors/{actor.id}', headers=self.casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

# Run the test suite,
if __name__ == "__main__":
    unittest.main()