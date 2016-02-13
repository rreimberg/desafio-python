# -*- coding: utf-8 -*-

import json

from .base import BaseTestCase


class ApiTestCase(BaseTestCase):

    def test_json_request_validation(self):
        invalid_response = self.client.get('/')

        self.assertEqual(415, invalid_response.status_code)
        self.assertEqual('application/json', invalid_response.headers['Content-Type'])

        response_data = json.loads(invalid_response.data)
        self.assertEqual(u'Request Inválida: toda request deve ser um json', response_data['mensagem'])

        valid_response = self.client.get('/', headers={'Content-Type': 'application/json'})

        self.assertEqual(200, valid_response.status_code)
        self.assertEqual('application/json', valid_response.headers['Content-Type'])

        response_data = json.loads(valid_response.data)
        self.assertEqual('Bem vindo', response_data['mensagem'])
