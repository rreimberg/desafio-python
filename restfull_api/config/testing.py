# -*- coding: utf-8 -*-

from restfull_api.config.base import Configuration as Base


class Configuration(Base):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    DEBUG = True
