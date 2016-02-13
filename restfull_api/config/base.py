# -*- coding: utf-8 -*-

import os


class Configuration(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/user_api.db'.format(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    )

    DEBUG = True
