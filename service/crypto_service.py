from ..repository.crypto_repository import CryptoRepository
from ..model.сoin_model import CoinModel


class CryptoService():
    def __init__(self, crypto_repository: CryptoRepository):
        self.crypto_repository = crypto_repository

    def get_actual_price(self, coin, source):
        arr = {}
        for name in source:
            arr[name] = self.crypto_repository.get_actual_price(coin, name)
        price = [pr.price for pr in arr.values() if isinstance(pr, CoinModel) and pr.price is not None]
        if len(price)>=2:
            spred = max(price) - min(price)
            arr['spred'] = spred
        else:
            arr['spred'] = None
        return arr