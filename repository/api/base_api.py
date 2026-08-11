from abc import abstractmethod, ABC
from ...model.сoin_model import CoinModel


class BaseApi(ABC):
    def __init__(self, end_point):
        self.end_point = end_point

    @abstractmethod
    def get_data(self, coin) -> list[CoinModel]:
        pass