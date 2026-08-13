from .base_api import BaseApi
import datetime
import requests
import json
from ...model.coin_model import CoinModel


class BinanceApi(BaseApi):
    def __init__(self, end_point = 'https://api.binance.com/api/v3/ticker/price?symbol='):
        super().__init__(end_point=end_point)

    def form_string_api(self, coin) -> str:
        return self.end_point + coin

    def parse_data(self, response, coin):
        return [CoinModel(name=response['symbol'], time=datetime.datetime.now(), price=float(response['price']), source='Binance')]