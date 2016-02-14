# -*- coding: utf-8 -*-


from .base import BaseTestCase

from restfull_api import db
from restfull_api.models import User, Phone


class BusinessTestCase(BaseTestCase):

    def test_register_user_with_duplicated_email(self):
        pass

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
