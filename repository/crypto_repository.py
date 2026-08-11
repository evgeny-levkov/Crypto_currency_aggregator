from .base_repository import BaseRepository
from .db.base_db import BaseDb
from .api.base_api import BaseApi

class CryptoRepository(BaseRepository):
    def __init__(self, source, api_dict: dict[str, BaseApi], db: BaseDb):
        self.source = source
        self.api_dict = api_dict
        self.db = db

    def get_actual_price(self, coin, source):
        api : BaseApi = self.api_dict[source]
        try:
            res = api.get_data(coin)
            for coins in res:
                self.db.save_cache(coins)
            return res[-1]
        except Exception as e:
            print(f"Ошибка api: {e}")
        return self.db.get_coin_price(coin)

    def get_history_price(self, coin, limit=10000):
        return self.db.get_history_price(coin, limit)