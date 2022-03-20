import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DB_URL']
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
Seeker
Have title and release year
'''
class seeker(db.Model):
    __tablename__ = 'Seekers'

    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    years_ex = Column(Integer)
    email = Column(String)

    def __init__(self, seeker, job_title):
        self.seeker = seeker
        self.job_title = job_title
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
            'seeker': self.job_title,
            'job_title': self.job_title,
        }
'''
opportunity
'''


class opportunity(db.Model):
    __tablename__ = 'opportunities'

    id = Column(Integer, primary_key=True)
    field = Column(String)
    opportunity = Column(String)

    def __init__(self, field, opportunity):
        self.field = field
        self.opportunity = opportunity
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
            'field': self.field,
            'opportunity': self.opportunity,
        }