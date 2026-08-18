from ..alerts.alert_manager import AlertManager
from ..core.get_price_worker import GetPriceWorker
from ..service.crypto_service import CryptoService
from ..service.export_service import ExportService
from ..exporters.base_exporter import BaseExporter
from PyQt6.QtCore import QThread
from PyQt6.QtCore import QObject, pyqtSignal
from ..alerts.base_alert import BaseAlert
from ..alerts.alert_factory import AlertFactory
from ..model.alert_model import AlertModel
from ..model.coin_model import CoinModel
from ..core.get_price_worker import GetPriceWorker
from typing import Any


class CryptoViewModel(QObject):
    actual_price = pyqtSignal(dict)
    trigger_alert = pyqtSignal(str)
    history_data = pyqtSignal(list)
    export_res = pyqtSignal(object)

    def __init__(self, crypto_service: CryptoService, export_service: ExportService) -> None:
        super().__init__()
        self.get_price_thread = None
        self.crypto_service = crypto_service
        self.export_service = export_service
        self.alert_manager = AlertManager()
        self.alert_manager.trigger.connect(self.alert)
        self.member_alerts = self.crypto_service.get_all_alert()
        self.get_price_worker = None
        self.load_alerts()

    def start_monitoring(self, coin: str) -> None:
        if self.get_price_thread is None:
            self.get_price_thread = QThread()
            self.sources = self.crypto_service.get_source()
            self.get_price_worker = GetPriceWorker(coin, self.sources, self.crypto_service)
            self.get_price_worker.moveToThread(self.get_price_thread)
            try:
                self.get_price_thread.started.connect(self.get_price_worker.do_work)
                self.get_price_thread.start()
                self.get_price_worker.finished.connect(self.finish_get_price)
                self.get_price_worker.actual_price.connect(self.get_actual_price)
            except Exception as e:
                print(f"Ошибка при запуске потока: {e}")

    def finish_get_price(self) -> None:
         if self.get_price_worker is not None:
            self.get_price_thread.quit()
            self.get_price_worker.deleteLater()
            self.get_price_thread.deleteLater()
            self.get_price_thread = None
            self.get_price_worker = None

    def get_actual_price(self, actual_price: dict[str, CoinModel | float | None]) -> None:
        self.alert_manager.triggers(actual_price)
        self.actual_price.emit(actual_price)

    def stop_monitoring(self) -> None:
        if self.get_price_worker is not None:
            try:
                self.get_price_worker.finished.disconnect()
            except Exception as e:
                print(f'Ошибка{e}')
            self.get_price_worker.stop()
            self.get_price_thread.quit()
            self.get_price_thread.wait()
            self.get_price_worker.deleteLater()
            self.get_price_thread.deleteLater()
        self.get_price_thread = None
        self.get_price_worker = None


    def alert(self, alert_mes: BaseAlert, id: int) -> None:
        self.trigger_alert.emit(alert_mes.get_description())
        self.crypto_service.delete_alert(id)

    def get_history_data(self, coin: str, limit: int) -> None:
        self.history_data.emit(self.crypto_service.get_history_price(coin, limit))

    def export(self, exporter: str, coin: str, limit: int, filepath: str) -> None:
        res = self.export_service.export(exporter, coin, limit, filepath)
        if isinstance(res, str):
            self.export_res.emit(res)
        elif res is None:
            self.export_res.emit(None)

    def load_alerts(self) -> None:
        if self.member_alerts is not None:
            for alerts in self.member_alerts:
                self.alert_manager.add_alert(alerts.id, AlertFactory.give_alerts(alerts.alert_type, alerts.coin, alerts.source, **alerts.alert_params))

    def delete_alert(self, name: int) -> None:
        try:
            self.crypto_service.delete_alert(name)
            self.alert_manager.remove_alert(name)
        except Exception as e:
            print(f'Нет такого алёрта:{e}')

    def add_alert(self, alert_type: str, coin: str, source: str, **params: Any) -> int | None:
        try:
            id = self.crypto_service.add_alert(AlertModel(alert_type, coin, source, **params))
            self.alert_manager.add_alert(id, AlertFactory.give_alerts(alert_type, coin, source, **params))
            return id
        except Exception as e:
            print(f'Ошибка добавления:{e}')

    def get_alert_fields(self, name: str) -> dict[str, Any] | None:
        return AlertFactory.get_alert_fields(name)