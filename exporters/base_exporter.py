from abc import ABC, abstractmethod
from ..model.coin_model import CoinModel


class BaseExporter(ABC):
    @abstractmethod
    def export(self, data: list[CoinModel], filepath):
        pass