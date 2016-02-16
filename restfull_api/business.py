# -*- coding: utf-8 -*-

import hashlib
import jwt
from datetime import datetime
from flask import current_app as app

from restfull_api import db
from restfull_api.exceptions import DuplicatedEmail
from restfull_api.models import User


def register_user(data):

    if User.query.filter_by(email=data['email']).count():
        raise DuplicatedEmail()

    token = generate_access_token(data['email'])

    user = User(
        name=data['name'],
        email=data['email'],
        password=generate_hash(data['password']),
        token=generate_hash(token),
    )

    db.session.add(user)
    db.session.commit()

    return user, token


def generate_access_token(email):
    data = {'email': email, 'access': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

    return jwt.encode(data, app.config['TOKEN_SECRET'], app.config['TOKEN_ALGORITHM'])


def generate_hash(text):
    return hashlib.sha1(text).hexdigest()
