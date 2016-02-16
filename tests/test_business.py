# -*- coding: utf-8 -*-

import hashlib
import jwt
import mock

from datetime import datetime
from freezegun import freeze_time
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.exc import NoResultFound

from .base import BaseTestCase

from restfull_api import db
from restfull_api.business import (login_user, generate_access_token,
                                   register_user)
from restfull_api.exceptions import DuplicatedEmail, InvalidLogin
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

    @freeze_time('2016-02-15 19:56:52')
    @mock.patch('restfull_api.business.generate_access_token')
    def test_register_user_sucessful(self, token_mock):
        token_mock.return_value = 'mocked token'

        data = {
            'name': 'Joao',
            'email': 'joao@example.com',
            'password': '1234',
            'phones': [{'ddd': '11', 'number': '987654321'}],
        }

        user, token = register_user(data)

        self.assertEqual(1, user.id)
        self.assertEqual('Joao', user.name)
        self.assertEqual('mocked token', token)

    @mock.patch.object(BaseQuery, 'one')
    def test_login_with_invalid_user(self, fetch_mock):
        fetch_mock.side_effect = NoResultFound

        data = {
            'email': 'joao@example.com',
            'password': '1234',
        }

        with self.assertRaises(InvalidLogin):
            login_user(data)

    @mock.patch.object(BaseQuery, 'one')
    def test_login_with_wrong_password(self, fetch_mock):
        db_user = User(
            id=1,
            name='Joao',
            email='joao@example.com',
            password='123'
        )
        fetch_mock.return_value = db_user

        data = {
            'email': 'joao@example.com',
            'password': '1234',
        }

        with self.assertRaises(InvalidLogin):
            login_user(data)

    @freeze_time('2016-02-15 19:20:21')
    @mock.patch.object(BaseQuery, 'one')
    @mock.patch('restfull_api.business.generate_access_token')
    def test_sucessful_login(self, token_mock, fetch_mock):

        token_mock.return_value = 'mocked token'

        db_user = User(
            id=1,
            name='Joao',
            email='joao@example.com',
            password=hashlib.sha1('1234').hexdigest()
        )
        fetch_mock.return_value = db_user

        data = {
            'email': 'joao@example.com',
            'password': '1234',
        }

        user, token = login_user(data)

        self.assertEqual(hashlib.sha1(token).hexdigest(), user.token)
        self.assertEqual(datetime(2016, 2, 15, 19, 20, 21), user.last_login)

    def test_profile_with_inexistent_token(self):
        pass

    def test_profile_with_wrong_token(self):
        pass

    def test_profile_with_expired_session(self):
        pass

    def test_sucessful_profile(self):
        pass
