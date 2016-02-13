# -*- coding: utf-8 -*-

import os

from unittest import TestCase

from restfull_api.app import db, create_app


def set_testing_config(app):
    app.config.from_object('restfull_api.config.testing.Configuration')


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.app = self.create_app()
        self.fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')

        self.context = self.app.app_context()
        self.context.push()

        self.client = self.app.test_client()

        db.create_all()

    def create_app(self):
        app = create_app(set_config=set_testing_config)
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()
        super(BaseTestCase, self).tearDown()
