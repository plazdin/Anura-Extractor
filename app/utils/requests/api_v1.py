from requests import Session

from utils.requests.cAuth import BearerAuth
from utils.logger import log
from config import conf


headers = {'Content-Type': 'application/json'}


s = Session()
s.auth, s.headers.update = BearerAuth(conf.TOKEN), headers


def fetch(jsn: dict) -> list:
    '''Función base para las requests.'''
    fetched = []
    
    with s.post(conf.API_URL, json=jsn) as response:
        log.debug(f'Extracting: {jsn["startDate"]}.')
        data = response.json()
        if not data:
            return []
        return data
