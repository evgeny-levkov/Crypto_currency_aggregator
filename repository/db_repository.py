from .base_repository import BaseRepository
from .db.base_db import BaseDb
from ..model.coin_model import CoinModel
from ..model.alert_model import AlertModel


class DbRepository(BaseRepository):
    def __init__(self, db: BaseDb) -> None:
        self.db = db

    def get_history_price(self, coin: str, limit: int =10000) -> list[CoinModel] | None:
        return self.db.get_history_price(coin, limit)

    def get_actual_price(self, coin: str, source: str) -> CoinModel | None:
        return self.db.get_coin_price(coin, source)

    def get_all_alert(self) -> list[AlertModel] | None:
        return self.db.get_all_alert()

    def add_alert(self, alert: AlertModel) -> int | None:
        return self.db.add_alert(alert)

    def delete_alert(self, id: int) -> bool:
        return self.db.delete_alert(id)