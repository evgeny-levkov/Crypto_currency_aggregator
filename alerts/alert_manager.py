from .base_alert import BaseAlert
from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from ..model.coin_model import CoinModel


class AlertManager(QObject):
    trigger = pyqtSignal(BaseAlert, int)

    def __init__(self) -> None:
        super().__init__()
        self.alerts: dict[int, BaseAlert] = {}

    def add_alert(self, name: int, alert: BaseAlert) -> None:
        self.alerts[name] = alert

    def remove_alert(self, name: int) -> None:
        del self.alerts[name]

    def triggers(self, data: dict[str, CoinModel | float | None]) -> None:
        worked_trigger = []
        for tr in self.alerts:
            if isinstance(self.alerts[tr], BaseAlert) and self.alerts[tr].check(data):
                worked_trigger.append(tr)
                self.trigger.emit(self.alerts[tr], tr)
        for trig in worked_trigger:
            self.remove_alert(trig)