from abc import abstractmethod, ABC
from ...model.сoin_model import CoinModel


class BaseDb(ABC):
    def __init__(self, db):
        self.db = db

    @abstractmethod
    def get_coin_price(self, coin) -> CoinModel:
        pass

    @abstractmethod
    def get_history_price(self, coin, limit = 10000) -> list[CoinModel]:
        pass

    @abstractmethod
    def save_cache(self, coin: CoinModel):
        pass