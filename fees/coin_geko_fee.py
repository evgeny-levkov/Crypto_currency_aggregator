from .base_fee import BaseFeeStrategy
from .fee_factory import FeeFactory


@FeeFactory.register_fee('coingeko')
class CoinGekoFee(BaseFeeStrategy):
    def __init__(self, buy_fee: float =0.03, sell_fee: float =0.02) -> None:
        super().__init__(buy_fee, sell_fee)

    def calculate_buy(self, price: float) -> float:
            return price + (price*self.buy_fee)

    def calculate_sell(self, price: float) -> float:
        return price - (price*self.sell_fee)