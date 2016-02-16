# -*- coding: utf-8 -*-

import os


class Configuration(object):

    TOKEN_SECRET = '|sZU0Ddb'
    TOKEN_ALGORITHM = 'HS256'

    SESSION_EXPIRES = 30

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/user_api.db'.format(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    )

    DEBUG = True
