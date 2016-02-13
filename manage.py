#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from restfull_api import create_app, db

app = create_app()

manager = Manager(app)


@manager.command
def create_db():
    db.create_all()


if __name__ == "__main__":
    manager.run()
