from abc import ABC, abstractmethod


class BaseFeeStrategy(ABC):
    def __init__(self, buy_fee, sell_fee):
        self.buy_fee = buy_fee
        self.sell_fee = sell_fee

    @abstractmethod
    def calculate_buy(self, price) -> int:
        pass

    @abstractmethod
    def calculate_sell(self, price) -> int:
        pass