from .base_repository import BaseRepository
from .api.base_api import BaseApi


class ApiRepository(BaseRepository):
    def __init__(self, api_dict: dict[str, BaseApi]):
        self.api_dict = api_dict

    def get_actual_price(self, coin, source):
       return self.api_dict[source].get_data(coin)[-1]

    def get_history_price(self, coin, limit=10000):
        raise NotImplementedError