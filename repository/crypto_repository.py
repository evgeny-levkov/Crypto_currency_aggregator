from .base_repository import BaseRepository
from .api_repository import ApiRepository
from .db_repository import DbRepository
from ..model.coin_model import CoinModel


class CryptoRepository(BaseRepository):
    def __init__(self, api_repository: ApiRepository, db_repository: DbRepository):
        self.api_repository = api_repository
        self.db_repository = db_repository

    def get_actual_price(self, coin, source):
        try:
            res = self.api_repository.get_actual_price(coin, source)
            if isinstance(res, CoinModel):
                self.db_repository.db.save_cache(res)
            else:
                pass
            return res
        except Exception as e:
            print(f"Ошибка получения данных API: {e}")
            return self.db_repository.get_actual_price(coin, source)

    def get_history_price(self, coin, limit=10000):
        return self.db_repository.get_history_price(coin, limit)

    def get_all_alert(self):
        try:
            return self.db_repository.get_all_alert()
        except Exception as e:
            print(f'Ошибка: {e}')

    def add_alert(self, alert):
        try:
            return self.db_repository.add_alert(alert)
        except Exception as e:
                print(f'Ошибка: {e}')

    def delete_alert(self, id):
        try:
            return self.db_repository.delete_alert(id)
        except Exception as e:
            print(f'Ошибка: {e}')