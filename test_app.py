from email import header
from http.client import ImproperConnectionState
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import Jobs, Seeker, setup_db, db
from app import create_app
# TODO:
# make sure you create a database named opportunitytest in psql
database_name = "opportunitytest"
database_path = 'postgresql://postgres:43150@localhost:5432/{}'.format(
    database_name)

recruiter_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVKeFdPd3Z0eG5rQlhudHIxbGc5OCJ9.eyJpc3MiOiJodHRwczovL2ZzbmR0ei51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFmMjY4NDY5ZDVhZjAwMDZhNTdmODI1IiwiYXVkIjoiZ3JlZXRpbmciLCJpYXQiOjE2NDc3ODYxOTAsImV4cCI6MTY0Nzc5MzM5MCwiYXpwIjoiNmhzMVQ4VHVUZGUyTmJZNTk4RWE1dUJEYmZJUzU2ZWIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpncmVldGluZ3MiLCJwb3N0OmdyZWV0aW5ncyJdfQ.BJnMXuYtcSkChG8Le3TZAJBAlIS_3aj5MNT-WbApCtaiRa2XFpCfztiKoP-waiO2fbmGIM8xXj0_-HlCfnlw89CHr3JqSB9sRGgfL1Y_XYPSVYz_VvxczYLUxqVryv2ekYTDRJYmIXQ4H59JOpUyKxrytZN4cuRNLdlLIbGqa034QjKMJ3JF1ZQf5UaGxhsn9i03RnNacOU907DbHRTyQLiUSsJmcDrNvGYmVjCIMFE71r9r_niMkQSXQrt7VTVlBRfNwUeOknHkRVW6NoClngIXRcO0rsScoH9mhIz9R9cJWExOphcFcL439fayBHSrUyqMZD9vDdGkRVJ1JboyCQ"
assistant_token = ""
seeker_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVKeFdPd3Z0eG5rQlhudHIxbGc5OCJ9.eyJpc3MiOiJodHRwczovL2ZzbmR0ei51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIwZWE4NzBjNDFmZjAwMDcyODRkZTdiIiwiYXVkIjoiZ3JlZXRpbmciLCJpYXQiOjE2NDc3ODY4MDUsImV4cCI6MTY0Nzc5NDAwNSwiYXpwIjoiNmhzMVQ4VHVUZGUyTmJZNTk4RWE1dUJEYmZJUzU2ZWIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpncmVldGluZ3MiXX0.cNLW8wdVrh__09WKXTmC0fn2sWKooHjhVXXo56pA55y6Luu7oon7qbkF1x3PSlRvK3Qbr_NnFamjmTNFPJVM-8gmm7tHKJ-Ep3wUeaek5cOqz6NSIMz2N4QCmnCcZz2yiEaFd9CYSemY6rH_UhxxiA67mvNlZgqdJqAWTHCuwuICvL_m0zmxUk2jN2QnVHZrmojmQBWYYQ42EL0CUGTdzoiqLOV5-47PIYbmnLN5Zm-PFD7Ra9x-n-juk5Uy2I6t6ByVRFO1uxW8K4Q8zQQAKAzF15N8jysr0BpKyj2yJTbZJvDwB7F8DLjU-mBx_VvO2851kFksyBUF6hOdN39KTg"


opportunities = [{'field': 'Software', 'title': 'Web Developmer'},
             {'field': 'Teaching', 'title': 'Dutch Language Teacher'},
             {'field': 'Managing', 'title': 'Program Manager'},
             {'field': 'Driving', 'title': 'Track Driver'},
             {'field': 'Medical', 'title': 'Sergury Doctor'},
             {'field': 'Engineer', 'title': 'Civil Engineer'},
             {'field': 'Cleanning', 'title': 'Cleaner'}]

seekers = [{'seeker_name': 'John', 'job_title': 'Software Developer', 'year_ex': '5', 'email': 'john@gmail.com'},
           {'seeker_name': 'Soso', 'job_title': 'English Teacher', 'year_ex': '3', 'email': 'soso@gmail.com'},
           {'seeker_name': 'Maria', 'job_title': 'Coach', 'year_ex': '4', 'email': 'maria@gmail.com'},
           {'seeker_name': 'Tio', 'job_title': 'Developer', 'year_ex': '7', 'email': 'tio@gmail.com'}]

class opportunityTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

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
            for opportunity in opportunities:
                cat = opportunity(**opportunity)
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

    # testing the opportunities
    def test_get_opportunities_ok(self):
        # print('hello')
        headers = {
            'Authorization': 'Bearer {}'.format(seeker_token)
        }
        print('hello test_get_opportunities_ok')

        res = self.client().get('/opportunities', headers=headers)  # res is of a type stream
        # print(res.data) # res.data is a of type string of characters
        # data is a of type string of characters
        new_greeetings = json.loads(res.data)
        # print(new_greeetings)
        self.assertEqual(res.status_code, 200)

    # test getting one opportunity
    def test_one_opportunity_ok(self):
        print('hello test_one_opportunity')
        headers = {
            'Authorization': 'Bearer {}'.format(seeker_token)
        }
        res = self.client().get(f'/opportunities/en', headers=headers)
        # print("res " , res)
        new_opportunity= json.loads(res.data)
        # print("new_opportunity",new_opportunity)
        self.assertEqual(res.status_code, 200)

        self.assertEqual(new_opportunity["opportunity"]
                         ['opportunity'], opportunities[0]["opportunity"])

    # test getting one opportunity

    def test_one_opportunity_401(self):
        print('hello test_one_opportunity_404')
        res = self.client().get(f'/opportunities/en')
        # print("res " , res)
        new_opportunity= json.loads(res.data)
        # print("new_opportunity",new_opportunity)
        self.assertEqual(res.status_code, 401)

    def test_one_opportunity_404(self):
        print('hello test_one_opportunity_404')
        headers = {
            'Authorization': 'Bearer {}'.format(seeker_token)
        }
        res = self.client().get(f'/opportunities/notfound', headers=headers)
        # print("res " , res)
        new_opportunity= json.loads(res.data)
        # print("new_opportunity",new_opportunity)
        self.assertEqual(res.status_code, 404)

        # self.assertEqual(new_opportunity["opportunity"]['opportunity'], opportunities[0]["opportunity"])

    # test getting one opportunity

    def test_create_opportunity_ok(self):
        print('hello test_create_opportunity_ok')
        headers = {
            'Authorization': 'Bearer {}'.format(recruiter_token)
        }
        res = self.client().post(f'/opportunities', headers=headers,
                                 json=dict(field="french", opportunity="bonjour"))
        print("res ", res)
        print("res.data ", res.data)
        new_opportunity= json.loads(res.data)
        # print("new_opportunity",new_opportunity)
        self.assertEqual(res.status_code, 201)

    def test_create_opportunity_403(self):
        print('hello test_create_opportunity_40')
        headers = {
            'Authorization': 'Bearer {}'.format(seeker_token)
        }
        res = self.client().post(f'/opportunities', headers=headers,
                                 json=dict(field="trainer", opportunity="prject management"))

        # print("new_opportunity",new_opportunity)
        self.assertEqual(res.status_code, 403)

    # TODO: implement a test case to test getting one beautiful opportunity
    def test_beautiful_opportunity(self):
        print('hello test_beautiful_opportunity')

        self.assertEqual(200, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
