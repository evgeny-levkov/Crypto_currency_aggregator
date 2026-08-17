from abc import ABC, abstractmethod


class BaseFeeStrategy(ABC):
    def __init__(self, buy_fee: float, sell_fee: float) -> None:
        self.buy_fee = buy_fee
        self.sell_fee = sell_fee

    @abstractmethod
    def calculate_buy(self, price: float) -> float:
        pass

    @abstractmethod
    def calculate_sell(self, price: float) -> float:
        pass