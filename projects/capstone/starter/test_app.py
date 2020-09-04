import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import db, db_drop_and_create_all, setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth
from sqlalchemy import Column, String, Integer, DateTime
import logging
from setup import CASTING_ASSISTANT_JWT, CASTING_DIRECTOR_JWT, EXECUTIVE_PRODUCER_JWT

database_name = "capstone_test.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_name))

casting_assistant_token = CASTING_ASSISTANT_JWT
casting_director_token = CASTING_DIRECTOR_JWT
executive_producer_token = EXECUTIVE_PRODUCER_JWT

# define set authetification method


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
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.config['TESTING'] = True  # add it to fix Error 500
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['DEBUG'] = False
        self.client = self.app.test_client
        self.database_name = database_name
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        self.new_actor = {
            "name": "Test Acotor",
            "age": 22,
            "gender": "Male"
        }
        self.new_movie = {
            "title": "Test Movie"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
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