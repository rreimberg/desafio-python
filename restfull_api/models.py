# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import relationship


from restfull_api import db


utcnow = datetime.utcnow


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(512))
    email = db.Column(db.String(128))
    password = db.Column(db.String(50))
    token = db.Column(db.String(2))

    created = db.Column(db.DateTime, default=utcnow)
    modified = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    last_login = db.Column(db.DateTime, default=utcnow)


class Phone(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    ddd = db.Column(db.String(2))
    number = db.Column(db.String(9))

    user = relationship("User", backref='phones')
