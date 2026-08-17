from abc import ABC, abstractmethod
from ..model.coin_model import CoinModel
from typing import Any


class BaseExporter(ABC):
    @abstractmethod
    def export(self, data: list[CoinModel], filepath: str) -> Any:
        pass