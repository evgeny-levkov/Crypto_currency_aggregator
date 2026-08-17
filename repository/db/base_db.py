from abc import abstractmethod, ABC
from ...model.coin_model import CoinModel
from ...model.alert_model import AlertModel


class BaseDb(ABC):
    def __init__(self, db: str) -> None:
        self.db = db

    @abstractmethod
    def get_coin_price(self, coin: str, source: str) -> CoinModel | None:
        pass

    @abstractmethod
    def get_history_price(self, coin: str, limit: int = 10000) -> list[CoinModel] | None:
        pass

    @abstractmethod
    def save_cache(self, coin: CoinModel) -> None:
        pass

    def get_all_alert(self) -> list[AlertModel] | None:
        pass

    def delete_alert(self, id: int) -> bool:
        pass

    def add_alert(self, alert: AlertModel) -> int | None:
        pass