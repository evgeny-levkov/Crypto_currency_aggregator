from abc import ABC, abstractmethod
from ..model.coin_model import CoinModel


class BaseAlert(ABC):
    @abstractmethod
    def check(self, price: dict[str, CoinModel | float | None]) -> bool:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass