from .base_api import BaseApi
import requests
import datetime
from ...model.сoin_model import CoinModel


class CoinGekoApi(BaseApi):
    def __init__(self, mapping, end_point = 'https://api.coingecko.com/api/v3/simple/price?ids='):
        super().__init__(end_point=end_point)
        self._mapping = mapping

    def get_data(self, coin):
        get_req = requests.get(self.end_point+self._mapping[coin]+'&vs_currencies=usd').json()
        return [CoinModel(name=coin, time=datetime.datetime.now(), price=get_req[self._mapping[coin]]['usd'], source='CoinGeko')]