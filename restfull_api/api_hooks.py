# -*- coding: utf-8 -*-

from flask import jsonify, Response


class ApiResponse(Response):

    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(ApiResponse, cls).force_type(rv, environ)
