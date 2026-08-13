from .base_api import BaseApi
import requests
import datetime
from ...model.coin_model import CoinModel


class CoinGeckoApi(BaseApi):
    def __init__(self, mapping, end_point = 'https://api.coingecko.com/api/v3/simple/price?ids='):
        super().__init__(end_point=end_point)
        self._mapping = mapping

    def form_string_api(self, coin) -> str:
        return self.end_point+self._mapping[coin]+'&vs_currencies=usd'

    def parse_data(self, response, coin):
        return [CoinModel(name=coin, time=datetime.datetime.now(), price=response[self._mapping[coin]]['usd'], source='CoinGeko')]