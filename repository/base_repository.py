from abc import abstractmethod, ABC
from ..model.coin_model import CoinModel
from ..model.alert_model import AlertModel


class BaseRepository(ABC):
    @abstractmethod
    def get_actual_price(self, coin, source) -> CoinModel:
        pass

    @abstractmethod
    def get_history_price(self, coin, limit = 10000) -> list[CoinModel]:
        pass

    def get_all_alert(self) -> list[AlertModel]:
        raise NotImplementedError

    def add_alert(self, alert: AlertModel):
        raise NotImplementedError

    def delete_alert(self, id):
        raise NotImplementedError