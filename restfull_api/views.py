# -*- coding: utf-8 -*-

from functools import wraps

from flask import Blueprint, request
from werkzeug.exceptions import BadRequest

from restfull_api.business import get_profile, register_user, login_user
from restfull_api.exceptions import AuthorizationError, ValidationError

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
    # check json structure explicitly
    try:
        data = request.json
        data['name']
        data['email']
        data['password']
        data['phones']

        assert isinstance(data['phones'], list)

        for phone in data['phones']:
            phone['ddd']
            phone['number']

    except (AssertionError, KeyError, TypeError, BadRequest):
        return api_error('Request Inválida: formato dos parâmetros inválido', 400)

    try:
        user_data = register_user(data)
    except ValidationError as exc:
        return api_error(exc.message, 400)

    return user_data, 201


@api.route("/login/", methods=["POST"])
@requires_json
def login():

    try:
        data = request.json
        data['email']
        data['password']
    except (KeyError, BadRequest):
        return api_error('Request Inválida: formato dos parâmetros inválido', 400)

    try:
        user_data = login_user(data)
    except ValidationError as exc:
        return api_error(exc.message, 400)

    return user_data, 200


@api.route("/profile/<user_id>/", methods=["GET"])
@requires_json
def profile(user_id):
    if 'X-Token' not in request.headers:
        return api_error('Obrigatório uso do header X-Token para usar este endpoint', 400)

    token = request.headers['X-Token']

    try:
        user_data = get_profile(user_id, token)
    except AuthorizationError as exc:
        return api_error(exc.message, 401)

    return user_data, 200
