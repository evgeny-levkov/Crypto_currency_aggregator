from abc import ABC, abstractmethod
from ..model.coin_model import CoinModel


class BaseAlert(ABC):
    def __init__(self, alert_name: str = "Без имени") -> None:
        self.alert_name = alert_name

    @abstractmethod
    def check(self, price: dict[str, CoinModel | float | None]) -> bool:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @classmethod
    def get_fields(cls) -> dict[str, str | list[str]]:
        return {}