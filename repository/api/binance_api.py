from .base_api import BaseApi
import datetime
import requests
import json
from ...model.сoin_model import CoinModel


class BinanceApi(BaseApi):
    def __init__(self, end_point = 'https://api.binance.com/api/v3/ticker/price?symbol='):
        super().__init__(end_point=end_point)

    def get_data(self, coin):
        get_req = requests.get(self.end_point+coin).json()
        return [CoinModel(name=get_req['symbol'], time=datetime.datetime.now(), price=float(get_req['price']), source='Binance')]