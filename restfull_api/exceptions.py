# -*- coding: utf-8 -*-


class ValidationError(Exception):
    pass


class DuplicatedEmail(ValidationError):
    message = 'Email já cadastrado'


class InvalidLogin(ValidationError):
    message = 'Usuário e/ou senha inválidos'


class InvalidToken(ValidationError):
    message = 'Não autorizado'


class InvalidSession(ValidationError):
    message = 'Sessão Expirada'
