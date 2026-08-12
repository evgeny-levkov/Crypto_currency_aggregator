from .base_repository import BaseRepository
from .db.base_db import BaseDb


class DbRepository(BaseRepository):
    def __init__(self, db: BaseDb):
        self.db = db

    def get_history_price(self, coin, limit=10000):
        return self.db.get_history_price(coin, limit)

    def get_actual_price(self, coin, source):
        return self.db.get_coin_price(coin, source)

    def get_all_alert(self):
        return self.db.get_all_alert()

    def add_alert(self, alert):
        return self.db.add_alert(alert)

    def delete_alert(self, id):
        return self.db.delete_alert(id)