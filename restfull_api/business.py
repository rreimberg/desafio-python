# -*- coding: utf-8 -*-

import jwt
from datetime import datetime
from flask import current_app as app

from restfull_api.exceptions import DuplicatedEmail
from restfull_api.models import User


def register_user(data):

    if User.query.filter_by(email=data['email']).count():
        raise DuplicatedEmail()


def generate_access_token(email):
    data = {'email': email, 'access': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

    return jwt.encode(data, app.config['TOKEN_SECRET'], app.config['TOKEN_ALGORITHM'])
