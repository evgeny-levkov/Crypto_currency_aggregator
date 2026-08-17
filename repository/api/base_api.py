from abc import abstractmethod, ABC
from ...model.coin_model import CoinModel
import requests
from typing import Any


class BaseApi(ABC):
    def __init__(self, end_point: str) -> None:
        self.end_point = end_point

    def get_data(self, coin: str) -> list[CoinModel]:
        return self.parse_data(requests.get(self.form_string_api(coin)).json(), coin)

    @abstractmethod
    def form_string_api(self, coin: str) -> str:
        pass

    @abstractmethod
    def parse_data(self, response: Any, coin: str) -> list[CoinModel]:
        pass