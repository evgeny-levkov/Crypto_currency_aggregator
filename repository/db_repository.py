from .base_repository import BaseRepository
from .db.base_db import BaseDb


class DbRepository(BaseRepository):
    def __init__(self, db: BaseDb):
        self.db = db

    def get_history_price(self, coin, limit=10000):
        return self.db.get_history_price(coin, limit)

    def get_actual_price(self, coin, source):
        return self.db.get_coin_price(coin, source)