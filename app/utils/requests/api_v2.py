from typing import Literal

from requests import Session, Response

from utils.requests.token import TokenManager
from config import conf
from utils.requests.cAuth import BearerAuth

    
class RequestsManager:
    
    __s = Session()
    __base_url = conf.API_URL_V2
    
    def __init__(self, token_manager: TokenManager) -> None:
        self.token_manager = token_manager


    def __update_headers(self):
        token = self.token_manager.get_token()
        self.__s.auth = BearerAuth(token)


    def fetch_stats_groups(self, query: dict, group: int = None) -> Response:
        '''
        Endpoint: tenants/stats/groups.\n
        Param:
        ------
        query: a dict that uses 3 fields:
            - startDate: str ("%Y-%m-%d")
            - endDate: str ("%Y-%m-%d")
            - allActions: bool (optional)
        '''
        endpoint = f'tenants/stats/groups'
        if group:
            endpoint += f'/{group}'

        self.__update_headers()
        with self.__s.get(
            f'{self.base_url}{endpoint}',
            params=query) as response:
            return response


    def fetch_stats_queues(
            self, query: dict, queueId: int = None,
            next_end: Literal['agents', 'agents-call', 'cdrs', 'status'] = None
        ) -> Response:

        endpoint = f'tenants/stats/queues'
        if queueId:
            endpoint = f'/{queueId}'
        
        if next_end:
            endpoint += f'/{next_end}'
        
        self.__update_headers()
        with self.__s.get(
            f'{self.__base_url}{endpoint}',
            params=query) as response:
            return response

    
    def fetch_call(self, id: int = None):
        endpoint = 'accounts/call'
        
        if id:
            endpoint += f'/{id}'
        
        self.__update_headers()
        with self.__s.get(
            f'{self.__base_url}{endpoint}') as response:
            return response


    def fetch_cdrs(self, query: dict = None, id: int = None, extra=False):
        endpoint = 'tenants/stats/cdrs'   
        if id:
            endpoint += f'/{id}'
        if id and extra:
            endpoint += '/extra-info'
        
        self.__update_headers()
        with self.__s.get(
            f'{self.__base_url}{endpoint}', params=query) as response:
            return response
