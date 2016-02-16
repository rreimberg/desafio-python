# -*- coding: utf-8 -*-

import hashlib
import jwt
from datetime import datetime, timedelta
from flask import current_app as app
from sqlalchemy.orm.exc import NoResultFound

from restfull_api import db
from restfull_api.exceptions import (DuplicatedEmail, InvalidLogin,
                                     InvalidSession, InvalidToken)
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

    return user_data(user, token)


def login_user(data):

    try:
        user = User.query.filter_by(email=data['email']).one()
    except NoResultFound:
        raise InvalidLogin()

    if user.password != generate_hash(data['password']):
        raise InvalidLogin()

    token = generate_access_token(data['email'])

    user.token = generate_hash(token)
    user.last_login = datetime.utcnow()

    return user_data(user, token)


def get_profile(id_, token):

    try:
        user = User.query.filter_by(token=generate_hash(token)).one()
    except NoResultFound:
        raise InvalidToken()

    if user.id != int(id_):
        raise InvalidToken()

    expires = user.last_login + timedelta(minutes=app.config['SESSION_EXPIRES'])

    if datetime.utcnow() > expires:
        raise InvalidSession()

    return user_data(user, token)


def generate_access_token(email):
    data = {'email': email, 'access': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

    return jwt.encode(data, app.config['TOKEN_SECRET'], app.config['TOKEN_ALGORITHM'])


def generate_hash(text):
    return hashlib.sha1(text).hexdigest()


def user_data(user, token):
    return {
        'id': user.id,
        'created': user.created.strftime('%Y-%m-%d %H:%M:%S'),
        'modified': user.modified.strftime('%Y-%m-%d %H:%M:%S'),
        'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
        'token': token,
    }
