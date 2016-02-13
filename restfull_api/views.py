# -*- coding: utf-8 -*-

from functools import wraps

from flask import Blueprint, request

api = Blueprint('api', __name__)


def api_error(message, code=400):
    return ('{{"mensagem": "{}"}}'.format(message), code)


def requires_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.mimetype not in ('application/json',):
            return api_error('Request Inválida: toda request deve ser um json',
                             415)

        return f(*args, **kwargs)

    return decorated


@api.route("/", methods=["GET"])
@requires_json
def index():
    return {'mensagem': 'Bem vindo'}


@api.route("/register/", methods=["POST"])
@requires_json
def register():
    data = request.json
    # check json structure explicitly
    try:
        data['name']
        data['email']
        data['password']
        data['phones']

        assert isinstance(data['phones'], list)

        for phone in data['phones']:
            phone['ddd']
            phone['number']

    except (AssertionError, KeyError, TypeError):
        return api_error('Request Inválida: formato dos parâmetros inválido', 400)

    if data['email'] == 'existent@email.com':
        return api_error('Email já cadastrado')

    user_data = {
        'id': '',
        'created': '',
        'modified': '',
        'last_login': '',
        'token': '',
    }

    return user_data, 201


@api.route("/login/", methods=["POST"])
@requires_json
def login():
    data = request.json

    try:
        data['email']
        data['password']
    except KeyError:
        return api_error('Request Inválida: formato dos parâmetros inválido', 400)

    if data['email'] == 'invalid@email.com':
        return api_error('Usuário e/ou senha inválidos')

    user_data = {
        'id': '',
        'created': '',
        'modified': '',
        'last_login': '',
        'token': '',
    }

    return user_data, 201


@api.route("/profile/<user_id>/", methods=["GET"])
@requires_json
def profile(user_id):
    if 'X-Token' not in request.headers:
        return api_error('Obrigatório uso do header X-Token para usar este endpoint', 400)

    token = request.headers['X-Token']

    if token == 'inexistent token':
        return api_error('Não autorizado', 401)

    if token == 'another user token' and user_id == '1':
        return api_error('Não autorizado', 401)

    if token == 'expired token' and user_id == '1':
        return api_error('Sessão inválida', 401)

    user_data = {
        'id': '',
        'created': '',
        'modified': '',
        'last_login': '',
        'token': '',
    }

    return user_data, 201
