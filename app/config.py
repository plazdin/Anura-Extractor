# pylint: disable = C0114, R0903
import os

from dotenv import dotenv_values, load_dotenv


class Config:
    '''
    Gets all variables from diverse config files.
    '''
    DEBUG: bool = True

    TOKEN: str
    API_URL: str
    API_URL_V2: str

    LOG_PATH: str
    CRED_FILE: str

    BQ_TABLE: str
    BQ_PROJECT: str

    CLIENT_ID: str
    CLIENT_PASSWORD: str
    TOKEN_URL: str


    def __init__(self) -> None:
        load_dotenv()
        self.__dict__.update({
            **dotenv_values(os.environ['ANURA_CREDENTIALS']),
            **dotenv_values(os.environ['GBQ_CREDENTIALS']),
            'LOG_PATH': os.environ['LOG_PATH'],
            'DEBUG': bool(os.environ['DEBUG']),
            'SPATH': os.environ['SPATH']
        })


conf = Config()