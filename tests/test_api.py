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

    def test_register_endpoint_required_params_validation(self):
        params = {}
        headers = {'Content-Type': 'application/json'}

        expected_response = '{"mensagem": "Request Inválida: formato dos parâmetros inválido"}'

        # empty request

        response = self.client.post('/register/', headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

        response = self.client.post('/register/', data=json.dumps(params), headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

        # incomplete params

        params = {
            'name': '',
        }

        response = self.client.post('/register/', data=json.dumps(params), headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

        # invalid phone format

        params = {
            'name': '',
            'email': '',
            'password': '',
            'phones': '',
        }

        response = self.client.post('/register/', data=json.dumps(params), headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

        # empty phone list

        params = {
            'name': '',
            'email': '',
            'password': '',
            'phones': [{}],
        }

        response = self.client.post('/register/', data=json.dumps(params), headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

        # correct parameters

        params = {
            'name': '',
            'email': '',
            'password': '',
            'phones': [
                {'ddd': '', 'number': ''}
            ],
        }

        response = self.client.post('/register/', data=json.dumps(params), headers=headers)
        self.assertEqual(201, response.status_code)

    def test_register_pre_existent_email(self):
        headers = {'Content-Type': 'application/json'}

        params = {
            'name': 'Test',
            'email': 'existent@email.com',
            'password': '1234',
            'phones': [
                {'ddd': '11', 'number': '12345678'}
            ],
        }

        response = self.client.post('/register/', data=json.dumps(params), headers=headers)

        self.assertEqual(400, response.status_code)
        self.assertEqual('{"mensagem": "Email já cadastrado"}', response.data)

    def test_login_endpoint_required_params_validation(self):
        params = {}
        headers = {'Content-Type': 'application/json'}

        expected_response = '{"mensagem": "Request Inválida: formato dos parâmetros inválido"}'

        # empty request

        response = self.client.post('/login/', headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

        response = self.client.post('/login/', data=json.dumps(params), headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

        # incomplete params

        params = {
            'email': '',
        }

        response = self.client.post('/login/', data=json.dumps(params), headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

    def test_login_endpoint_invalid_data(self):

        params = {'email': 'invalid@email.com', 'password': 'invalid_password'}
        headers = {'Content-Type': 'application/json'}
        expected_response = '{"mensagem": "Usuário e/ou senha inválidos"}'

        response = self.client.post('/login/', data=json.dumps(params), headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

    def test_profile_endpoint_requires_token(self):

        headers = {'Content-Type': 'application/json'}

        expected_response = '{"mensagem": "Obrigatório uso do header X-Token para usar este endpoint"}'

        response = self.client.get('/profile/1/', headers=headers)

        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, response.data)

    def test_profile_endpoint_with_inexistent_token(self):

        headers = {
            'Content-Type': 'application/json',
            'X-Token': 'inexistent token',
        }

        expected_response = '{"mensagem": "Não autorizado"}'

        response = self.client.get('/profile/1/', headers=headers)

        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_response, response.data)

    def test_profile_endpoint_with_wrong_token(self):

        headers = {
            'Content-Type': 'application/json',
            'X-Token': 'another user token',
        }

        expected_response = '{"mensagem": "Não autorizado"}'

        response = self.client.get('/profile/1/', headers=headers)

        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_response, response.data)

    def test_profile_endpoint_with_expired_token(self):

        headers = {
            'Content-Type': 'application/json',
            'X-Token': 'expired token',
        }

        expected_response = '{"mensagem": "Sessão inválida"}'

        response = self.client.get('/profile/1/', headers=headers)

        self.assertEqual(401, response.status_code)
        self.assertEqual(expected_response, response.data)
