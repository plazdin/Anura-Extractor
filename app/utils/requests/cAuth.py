'''Clase de autenticación para Requests, específica para Anura.'''
import requests

class BearerAuth(requests.auth.AuthBase):
    '''Clase de autenticación de token'''
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers['accept'] = 'application/json'
        r.headers["authorization"] = f'Bearer {self.token}'
        return r
