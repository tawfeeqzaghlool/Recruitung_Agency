from email import header
from http.client import ImproperConnectionState
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import Jobs, Seekers, setup_db, db
from app import create_app
# TODO:
# make sure you create a database named recruitingtest in psql
database_name = "recruitingtest"
database_path = 'postgresql://postgres:43150@localhost:5432/{}'.format(
    database_name)

recruiter_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVKeFdPd3Z0eG5rQlhudHIxbGc5OCJ9.eyJpc3MiOiJodHRwczovL2ZzbmR0ei51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFmMjY4NDY5ZDVhZjAwMDZhNTdmODI1IiwiYXVkIjoicmVjcnVpdCIsImlhdCI6MTY0ODEzMTA4NiwiZXhwIjoxNjQ4MTM4Mjg2LCJhenAiOiIyR3FvV0tUdjhoQ2xUNWxkazJwcE1Md1pzaXNCNnVJWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmpvYnMiLCJkZWxldGU6c2Vla2VycyIsImdldDpqb2JzIiwiZ2V0OnNlZWtlcnMiLCJwYXRjaDpqb2JzIiwicG9zdDpqb2JzIiwicG9zdDpzZWVrZXJzIl19.VemCfGqfdUtl7XHTVB1bVJlS7EGJgfchO6l1MluJrBnIZb7MgxWqBekUmVJiQXbnC1qT2iTswCqYUZLYWTBPh8kEi5tZfH-blp82QYYA86ZQ6tJ1ubTEER7PKnZfX5tATvwOkOYTHpQOvQP6vqRwinYJVOdNd7DFoJg11GcRNsHnZaG1lekn0NKVRQ1an8CuRVvuLdtUBKh8HU92RhYIOZQ8bBnBDGj51rd3Ae-d3cMvZmirXYl2xQpOL2oQFiALCW7ct8bhmFb7rza1FPW9s5srExRQ3bchTdypmYlp3w3h_-9pD_J1pBC4ZRpXouwSO8JFBft1U7YzFK4aYHTklA"
assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVKeFdPd3Z0eG5rQlhudHIxbGc5OCJ9.eyJpc3MiOiJodHRwczovL2ZzbmR0ei51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIwZWE4NzBjNDFmZjAwMDcyODRkZTdiIiwiYXVkIjoicmVjcnVpdCIsImlhdCI6MTY0ODEzMTMyNywiZXhwIjoxNjQ4MTM4NTI3LCJhenAiOiIyR3FvV0tUdjhoQ2xUNWxkazJwcE1Md1pzaXNCNnVJWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmpvYnMiLCJnZXQ6c2Vla2VycyIsInBhdGNoOmpvYnMiLCJwb3N0OmpvYnMiXX0.CuXJeWDOrgK_n1eGAbnBZDw-DcgUpOq5EQN8nJm464zp7BLK9hK0rHtFgsiRBjtnpQXNee-vCUI17TvqSxkqOiEB7Qk4D6S_hoeZ4qHDkqhIAvB23VJ2IzsDpmQKJucSz0yZdrL3XLDzYBM_WoUK3upy7FnT1eXlxHlNyt9WnBPfywKwVvogiVjdbzrIHSvJJfOHDE7KRfoLW9cQctIsTImL4xznJpaHvfCOV7VwaL9lhBh-k7dqx1AUcMXKfiRwO7hxW1WJWNa50mWre5qdvhCCLnq5yeMh3sy0vwPhWY0NjsDplQKzckqnnEGgJ3jet8eEX4hr3aNay3r1NYilWw"
seeker_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVKeFdPd3Z0eG5rQlhudHIxbGc5OCJ9.eyJpc3MiOiJodHRwczovL2ZzbmR0ei51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIwZTgwZTU5ZmYyYzYwMDY4ZWY5MzZkIiwiYXVkIjoicmVjcnVpdCIsImlhdCI6MTY0ODEzMTU2NiwiZXhwIjoxNjQ4MTM4NzY2LCJhenAiOiIyR3FvV0tUdjhoQ2xUNWxkazJwcE1Md1pzaXNCNnVJWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnNlZWtlcnMiLCJnZXQ6am9icyIsInBhdGNoOnNlZWtlcnMiLCJwb3N0OnNlZWtlcnMiXX0.CGDWZA7BRIsoXLuW3AzlTt68jQBKBFQnHqRm7hVd8hcA0iNXBAfQiKmbgy227W3SNo82rkTHF5BD7lWrGys5K7gYKdELxZ67GqlxjJWCPLZ01RqrO0er1SKp5YmTRLJhXl1_UNI8FkUHELtzHz2DSuHJnKyeHS3F0W0d78TbUN_-ng0QqUuB4yDNuIITdMVVCZ20OKEDlAb_umMGGV_WHXvXzfkJp2-RpFM1PqR2rrXiIj3LSPdiT7e4Z5VlFLYl5SqA0l2_SMmgIIOz7LoDIweLx1sjbVpgWmZrza2abRcOcZ1ZRYpjqkJU-l0Sdf8u5FPlzyPs1SQz3XI3NQ8BAQ"


jobs = [{'field': 'Software', 'title': 'Web Developmer'},
             {'field': 'Teaching', 'title': 'Dutch Language Teacher'},
             {'field': 'Managing', 'title': 'Program Manager'},
             {'field': 'Driving', 'title': 'Track Driver'},
             {'field': 'Medical', 'title': 'Sergury Doctor'},
             {'field': 'Engineer', 'title': 'Civil Engineer'},
             {'field': 'Cleaning', 'title': 'Cleaner'}]

seekers = [{'seeker_name': 'John', 'job_title': 'Software Developer', 'year_ex': '5', 'email': 'john@gmail.com'},
           {'seeker_name': 'Soso', 'job_title': 'English Teacher', 'year_ex': '3', 'email': 'soso@gmail.com'},
           {'seeker_name': 'Maria', 'job_title': 'Coach', 'year_ex': '4', 'email': 'maria@gmail.com'},
           {'seeker_name': 'Tio', 'job_title': 'Developer', 'year_ex': '7', 'email': 'tio@gmail.com'}]

class recruitingTestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app.
            it is run before each test
        """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        # each flask app has a context that includes all of the apps configuration like database, password, etc
        with self.app.app_context():
            # self.db = SQLAlchemy()
            self.db = db
            self.db.init_app(self.app)
            # clean the database beforehand
            self.db.drop_all()
            self.db.session.commit()

            # create all tables
            self.db.create_all()
            self.db.session.commit()

        with self.app.app_context():
            # insert the categories
            for job in jobs:
                cat = Jobs(**job)
                self.db.session.add(cat)
                self.db.session.commit()

    # in case you want to clean the database after each request
    def tearDown(self):
        """Executed after each test"""
        # with self.app.app_context():
        #     # clean the database beforehand
        #     self.db.drop_all()
        #     self.db.session.commit()
        pass
    
    def test_get_paginated_jobs(self):
        res = self.client().get('/jobs')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_jobs'])
        self.assertTrue(len(data['jobs']))
        self.assertTrue(len(data['fields']))

    def test_404_sent_requesting_jobs_beyond_valid_page(self):
        res = self.client().get('/jobs?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_paginated_seekers(self):
        res = self.client().get('/seekers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_seekers'])
        self.assertTrue(len(data['seeker_name']))
        self.assertTrue(len(data['job_title']))
        self.assertTrue(len(data['years_ex']))
        self.assertTrue(len(data['email']))

    def test_404_sent_requesting_seekers_beyond_valid_page(self):
        res = self.client().get('/seekers?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    # testing the jobs
    def test_get_jobs_ok(self):
        # print('hello')
        headers = {
            'Authorization': 'Bearer {}'.format(recruiter_token)
        }
        print('hello test_get_jobs_ok')

        res = self.client().get('/jobs', headers=headers)  # res is of a type stream
        # print(res.data) # res.data is a of type string of characters
        # data is a of type string of characters
        new_jobs = json.loads(res.data)
        # print(new_jobs)
        self.assertEqual(res.status_code, 200)

    # test getting one job
    def test_one_job_ok(self):
        print('hello test_one_job')
        headers = {
            'Authorization': 'Bearer {}'.format(recruiter_token)
        }
        res = self.client().get(f'/jobs/Software', headers=headers)
        # print("res " , res)
        new_job= json.loads(res.data)
        # print("new_job",new_job)
        self.assertEqual(res.status_code, 200)

        self.assertEqual(new_job["job"]
                         ['job'], jobs[0]["job"])

    # test getting one job

    def test_one_job_401(self):
        print('hello test_one_job_404')
        res = self.client().get(f'/jobs/Software')
        # print("res " , res)
        new_job= json.loads(res.data)
        # print("new_job",new_job)
        self.assertEqual(res.status_code, 401)

    def test_one_job_404(self):
        print('hello test_one_job_404')
        headers = {
            'Authorization': 'Bearer {}'.format(recruiter_token)
        }
        res = self.client().get(f'/jobs/notfound', headers=headers)
        # print("res " , res)
        new_job= json.loads(res.data)
        # print("new_job",new_job)
        self.assertEqual(res.status_code, 404)

        # self.assertEqual(new_job["job"]['job'], jobs[0]["job"])

    # test getting one job

    def test_create_job_ok(self):
        print('hello test_create_job_ok')
        headers = {
            'Authorization': 'Bearer {}'.format(recruiter_token)
        }
        res = self.client().post(f'/jobs', headers=headers,
                                 json=dict(field="Cleaning", job="Cleaner"))
        print("res ", res)
        print("res.data ", res.data)
        new_job= json.loads(res.data)
        # print("new_job",new_job)
        self.assertEqual(res.status_code, 201)

    def test_create_job_403(self):
        print('hello test_create_job_403')
        headers = {
            'Authorization': 'Bearer {}'.format(recruiter_token)
        }
        res = self.client().post(f'/jobs', headers=headers,
                                 json=dict(field="Trainer", job="Project Management"))

        # print("new_job",new_job)
        self.assertEqual(res.status_code, 403)

    # TODO: implement a test case to test getting one smart job
    def test_smart_job(self):
        print('hello test_smart_job')

        self.assertEqual(200, 200)
    # test getting seekers
    def test_get_seekers(self):
        res = self.client().get('/seekers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['seeker_name']))
        self.assertTrue(len(data['job_title']))
        self.assertTrue(len(data['years_ex']))
        self.assertTrue(len(data['email']))

    def test_404_sent_requesting_non_existing_seeker(self):
        res = self.client().get('/seekers/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_seeker_ok(self):
        print('hello test_create_seeker_ok')
        headers = {
            'Authorization': 'Bearer {}'.format(recruiter_token)
        }
        res = self.client().post(f'/seekers', headers=headers,
                                 json=dict(seeker_name="John", job_title="Painter", 
                                           years_ex="3", email="John@111.com"))
        print("res ", res)
        print("res.data ", res.data)
        new_seeker= json.loads(res.data)
        # print("new_seeker",new_seeker)
        self.assertEqual(res.status_code, 201)

    def test_create_seeker_403(self):
        print('hello test_create_seeker_403')
        headers = {
            'Authorization': 'Bearer {}'.format(recruiter_token)
        }
        res = self.client().post(f'/seekers', headers=headers,
                                 json=dict(seeker_name="John", job_title="Painter", 
                                           years_ex="3", email="John@111.com"))

        # print("new_seeker",new_seeker)
        self.assertEqual(res.status_code, 403)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
