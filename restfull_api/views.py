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
