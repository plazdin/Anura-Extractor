from .api_v2 import RequestsManager
from utils.requests.token import TokenManager

tm = TokenManager()
manager = RequestsManager(tm)