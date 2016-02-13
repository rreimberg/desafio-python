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

    user_data = {
        'id': '',
        'created': '',
        'modified': '',
        'last_login': '',
        'token': '',
    }

    return user_data, 201
