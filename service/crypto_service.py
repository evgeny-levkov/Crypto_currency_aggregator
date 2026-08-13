from ..repository.crypto_repository import CryptoRepository
from ..model.coin_model import CoinModel
from ..model.alert_model import AlertModel
from ..fees.fee_factory import FeeFactory
from ..fees.base_fee import BaseFeeStrategy


class CryptoService():
    def __init__(self, crypto_repository: CryptoRepository):
        self.crypto_repository = crypto_repository

    def get_actual_price(self, coin, source):
        price_buy = {}
        price_sell = {}
        arr = {}
        for name in source:
            arr[name] = self.crypto_repository.get_actual_price(coin, name)
            strategy = FeeFactory.give_fee(str(name).lower())
            if isinstance(strategy, BaseFeeStrategy) and isinstance(arr[name], CoinModel):
                price_buy[name] = strategy.calculate_buy(arr[name].price)
                price_sell[name] = strategy.calculate_sell(arr[name].price)
        price = [pr.price for pr in arr.values() if isinstance(pr, CoinModel) and pr.price is not None]
        if len(price)>=2:
            spred = max(price) - min(price)
            net_spred = max(price_sell.values()) - min(price_buy.values())
            arr['spred'] = spred
            arr['net_spred'] = net_spred
        else:
            arr['spred'] = None
            arr['net_spred'] = None
        return arr

    def get_history_price(self, coin, limit):
        return self.crypto_repository.get_history_price(coin, limit)

    def get_all_alert(self):
        return self.crypto_repository.get_all_alert()

    def add_alert(self, alert: AlertModel):
        return self.crypto_repository.add_alert(alert)

    def delete_alert(self, id):
        return self.crypto_repository.delete_alert(id)