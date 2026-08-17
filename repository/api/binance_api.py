from .base_api import BaseApi
import datetime
import requests
import json
from ...model.coin_model import CoinModel
from typing import Any


class BinanceApi(BaseApi):
    def __init__(self, end_point: str = 'https://api.binance.com/api/v3/ticker/price?symbol=') -> None:
        super().__init__(end_point=end_point)

    def form_string_api(self, coin: str) -> str:
        return self.end_point + coin

    def parse_data(self, response: Any, coin: str) -> list[CoinModel]:
        return [CoinModel(name=response['symbol'], time=datetime.datetime.now(), price=float(response['price']), source='Binance')]