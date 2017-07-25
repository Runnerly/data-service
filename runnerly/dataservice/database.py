# encoding: utf8
import os
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    strava_token = db.Column(db.String(128))
    age = db.Column(db.Integer)
    weight = db.Column(db.Numeric(4, 1))
    max_hr = db.Column(db.Integer)
    rest_hr = db.Column(db.Integer)
    vo2max = db.Column(db.Numeric(4, 2))
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = False

    def to_json(self, secure=False):
        res = {}
        for attr in ('id', 'email', 'firstname', 'lastname', 'age', 'weight',
                     'max_hr', 'rest_hr', 'vo2max'):
            value = getattr(self, attr)
            if isinstance(value, Decimal):
                value = float(value)
            res[attr] = value
        if secure:
            res['strava_token'] = self.strava_token
        return res

    def get_id(self):
        return self.id


class Run(db.Model):
    __tablename__ = 'run'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(128))
    description = db.Column(db.Unicode(512))
    strava_id = db.Column(db.Integer)
    distance = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    elapsed_time = db.Column(db.Integer)
    average_speed = db.Column(db.Float)
    average_heartrate = db.Column(db.Float)
    total_elevation_gain = db.Column(db.Float)
    runner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    runner = relationship('User', foreign_keys='Run.runner_id')

    def to_json(self):
        res = {}
        for attr in ('id', 'strava_id', 'distance', 'start_date',
                     'elapsed_time', 'average_speed', 'average_heartrate',
                     'total_elevation_gain', 'runner_id', 'title',
                     'description'):
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            res[attr] = value
        return res


def init_database():
    exists = db.session.query(User).filter(User.email == 'tarek@ziade.org')
    if exists.all() != []:
        return

    tarek = User()
    tarek.email = 'tarek@ziade.org'
    tarek.firstname = 'Tarek'
    tarek.lastname = 'Ziadé'
    tarek.age = 40
    tarek.weight = 58
    tarek.max_hr = 192
    tarek.rest_hr = 47
    tarek.vo2max = 63
    tarek.strava_token = os.environ.get('STRAVA_TOKEN')
    db.session.add(tarek)
    db.session.commit()
