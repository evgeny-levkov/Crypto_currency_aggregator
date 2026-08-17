from abc import abstractmethod, ABC
from ..model.coin_model import CoinModel
from ..model.alert_model import AlertModel


class BaseRepository(ABC):
    @abstractmethod
    def get_actual_price(self, coin: str, source: str) -> CoinModel | None:
        pass

    @abstractmethod
    def get_history_price(self, coin: str, limit: int = 10000) -> list[CoinModel] | None:
        pass

    def get_all_alert(self) -> list[AlertModel] | None:
        raise NotImplementedError

    def add_alert(self, alert: AlertModel) -> int | None:
        raise NotImplementedError

    def delete_alert(self, id: int) -> bool:
        raise NotImplementedError