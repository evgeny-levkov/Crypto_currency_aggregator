from .base_alert import BaseAlert
from ..model.coin_model import CoinModel
import operator
from ..alerts.alert_factory import AlertFactory


@AlertFactory.registry_alerts("price")
class PriceAlert(BaseAlert):
    def __init__(self, alert_price: float, coin: str, source: str, opr: str) -> None:
        self._operators = {'>': operator.gt, '<':operator.lt, '=': operator.eq}
        self.alert_price = alert_price
        self.coin = coin
        self.source = source
        self.symbol_opr = opr
        self.opr = self._operators[opr]

    def check(self, data: dict[str, CoinModel | float | None]) -> bool:
        try:
            model = data.get(self.source)
            if isinstance(model, CoinModel):
                if model.name == self.coin and self.opr(model.price, self.alert_price):
                    return True
                else:
                    return False
        except Exception as e:
            print(f"Ошибка{e}")
            return False

    def get_description(self) -> str:
        return f'{self.coin} на бирже {self.source} {self.symbol_opr} чем {self.alert_price}'