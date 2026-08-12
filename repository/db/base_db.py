from abc import abstractmethod, ABC
from ...model.сoin_model import CoinModel
from ...model.alert_model import AlertModel


class BaseDb(ABC):
    def __init__(self, db):
        self.db = db

    @abstractmethod
    def get_coin_price(self, coin, source) -> CoinModel:
        pass

    @abstractmethod
    def get_history_price(self, coin, limit = 10000) -> list[CoinModel]:
        pass

    @abstractmethod
    def save_cache(self, coin: CoinModel):
        pass

    def get_all_alert(self) -> list[AlertModel]:
        pass

    def delete_alert(self, id):
        pass

    def add_alert(self, alert: AlertModel):
        pass