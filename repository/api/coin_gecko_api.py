from .base_api import BaseApi
import requests
import datetime
from ...model.coin_model import CoinModel
from typing import Any


class CoinGeckoApi(BaseApi):
    def __init__(self, mapping: dict, end_point: str = 'https://api.coingecko.com/api/v3/simple/price?ids=') -> None:
        super().__init__(end_point=end_point)
        self._mapping = mapping

    def form_string_api(self, coin: str) -> str:
        return self.end_point+self._mapping[coin]+'&vs_currencies=usd'

    def parse_data(self, response: Any, coin: str) -> list[CoinModel]:
        return [CoinModel(name=coin, time=datetime.datetime.now(), price=response[self._mapping[coin]]['usd'], source='CoinGeko')]