import os
from sqlalchemy import Column, String, create_engine, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Seekers
Have tablename, includes primary key, job title, years of experience, email address as an attributes
'''
class Seekers(db.Model):
    __tablename__ = 'Seekers'

    id = Column(Integer, primary_key=True)
    seeker_name = Column(String(100), nullable=False)
    job_title = Column(String(50))
    years_ex = Column(Integer)
    email = Column(String, unique=True, nullable=False)

    def __init__(self, seeker_name, job_title, years_ex, email):
        self.seeker_name = seeker_name
        self.job_title = job_title
        self.years_ex = years_ex
        self.email = email
    def update(self):
        db.session.commit()
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {
            'id': self.id,
            'seeker_name': self.seeker_name,
            'job_title': self.job_title,
            'years_ex': self.years_ex,
            'email': self.email
        }
'''
Jobs
Have tablename, includes primary keys, title, fields as an attributes
'''


class Jobs(db.Model):
    __tablename__ = 'Jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    field = Column(String, nullable=False)

    def __init__(self, field, title):
        self.field = field
        self.title = title
    def update(self):
        db.session.commit()
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {
            'id': self.id,
            'field': self.field,
            'title': self.title,
        }