from abc import abstractmethod, ABC
from ..model.сoin_model import CoinModel

class BaseRepository(ABC):
    @abstractmethod
    def get_actual_price(self, coin, source) -> CoinModel:
        pass

    @abstractmethod
    def get_history_price(self, coin, limit = 10000) -> list[CoinModel]:
        pass