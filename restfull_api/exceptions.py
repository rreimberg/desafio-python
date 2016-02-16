# -*- coding: utf-8 -*-


class ValidationError(Exception):
    pass


class DuplicatedEmail(ValidationError):
    message = 'Email já cadastrado'


class InvalidLogin(ValidationError):
    message = 'Usuário e/ou senha inválidos'


class AuthorizationError(Exception):
    pass


class InvalidToken(AuthorizationError):
    message = 'Não autorizado'


class InvalidSession(AuthorizationError):
    message = 'Sessão inválida'
