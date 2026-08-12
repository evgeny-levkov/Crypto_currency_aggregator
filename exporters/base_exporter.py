from abc import ABC, abstractmethod
from ..model.сoin_model import CoinModel


class BaseExporter(ABC):
    @abstractmethod
    def export(self, data: list[CoinModel], filepath):
        pass