'''Módulo de extracción de token Api ANURA'''
import time

import requests
from requests.auth import HTTPBasicAuth

from config import conf
from utils.logger import log

class TokenManager:
    __CLIENT_ID = conf.CLIENT_ID
    __CLIENT_PASSWORD = conf.CLIENT_PASSWORD
    __TOKEN_URL= conf.TOKEN_URL

    def __init__(self) -> None:
        self.__token = None
        self.__token_expiration = 0

    
    def update_token(self) -> None:
        new_token = self.__token_request()
        
        # the token is valid for only 5 minutes,
        # hence the necesity to update 10 secs before
        expiration = time.time() + 290 

        # locks the token access while updates it
        self.__token = new_token
        self.__token_expiration = expiration
    

    def get_token(self) -> str:
        '''
        Returns the access token and updates if necesary.
        '''
        current_time = time.time()

        # Ckeck if the token has expired and updates if necessary
        if current_time >= self.__token_expiration:
            log.info('Actualizando access token.')
            self.update_token()
        
        return self.__token


    def __token_refresh(self) -> str | None:
        '''
        Obtains a refresh token, necessary to obtain the access token/
        '''
        data = {
        'grant_type': 'client_credentials',
        'scope': 'offline_access'
        }

        refresh_token = requests.post(self.__TOKEN_URL, data=data,
                            auth=HTTPBasicAuth(self.__CLIENT_ID, self.__CLIENT_PASSWORD)
                            ).json()['refresh_token']
        
        return refresh_token


    def __token_request(self) -> str | None:
        '''
        Actual function that actually gets the token.
        
        '''
        refresh = self.__token_refresh()
        params_access = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh,
            'client_id': self.__CLIENT_ID
        }
        access_token = requests.post(self.__TOKEN_URL, auth=HTTPBasicAuth(self.__CLIENT_ID,
                            self.__CLIENT_PASSWORD),data=params_access).json()
        return access_token['access_token']
