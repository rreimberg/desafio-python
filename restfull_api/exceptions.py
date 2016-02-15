# -*- coding: utf-8 -*-


class ValidationError(Exception):
    pass


class DuplicatedEmail(Exception):
    message = 'Email já cadastrado'
