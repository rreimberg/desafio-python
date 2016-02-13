# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def set_config(app):
    app.config.from_object('restfull_api.config.base.Configuration')


def register_uris(app):
    from restfull_api.views import api
    app.register_blueprint(api)


def create_app(set_config=set_config):
    app = Flask(__name__)
    set_config(app)

    db.init_app(app)
    app.db = db

    register_uris(app)

    return app
