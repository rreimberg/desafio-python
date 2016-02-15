# -*- coding: utf-8 -*-

import jwt
import mock

from freezegun import freeze_time
from flask_sqlalchemy import BaseQuery

from .base import BaseTestCase

from restfull_api import db
from restfull_api.business import register_user, generate_access_token
from restfull_api.exceptions import DuplicatedEmail
from restfull_api.models import User, Phone


class BusinessTestCase(BaseTestCase):

    @mock.patch.object(BaseQuery, 'count')
    def test_register_user_with_duplicated_email(self, fetch_mock):

        data = {
            'name': 'Joao',
            'email': 'joao@example.com',
            'password': '1234',
            'phones': [{'ddd': '11', 'number': '987654321'}],
        }

        fetch_mock.return_value = 1

        with self.assertRaises(DuplicatedEmail):
            register_user(data)

    @freeze_time('2016-02-15 19:56:52')
    def test_generate_access_token(self):

        config = self.app.config

        token = generate_access_token('joao@example.com')
        decoded = jwt.decode(token, config['TOKEN_SECRET'], config['TOKEN_ALGORITHM'])

        self.assertEqual('joao@example.com', decoded['email'])
        self.assertEqual('2016-02-15 19:56:52', decoded['access'])

    def test_register_user_sucessful(self):
        pass

    def test_login_with_invalid_user(self):
        pass

    def test_login_with_wrong_password(self):
        pass

    def test_sucessful_login(self):
        pass

    def test_profile_with_inexistent_token(self):
        pass

    def test_profile_with_wrong_token(self):
        pass

    def test_profile_with_expired_session(self):
        pass

    def test_sucessful_profile(self):
        pass
