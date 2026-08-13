from abc import abstractmethod, ABC
from ...model.coin_model import CoinModel
import requests


class BaseApi(ABC):
    def __init__(self, end_point):
        self.end_point = end_point

    def get_data(self, coin) -> list[CoinModel]:
        return self.parse_data(requests.get(self.form_string_api(coin)).json(), coin)

    @abstractmethod
    def form_string_api(self, coin) -> str:
        pass

    @abstractmethod
    def parse_data(self, response, coin):
        pass