from ..alerts.alert_manager import AlertManager
from ..core.get_price_worker import GetPriceWorker
from ..service.crypto_service import CryptoService
from ..service.export_service import ExportService
from PyQt6.QtCore import QThread
from PyQt6.QtCore import QObject, pyqtSignal
from ..alerts.base_alert import BaseAlert


class CryptoViewModel(QObject):
    actual_price = pyqtSignal(dict)
    trigger_alert = pyqtSignal(str)
    history_data = pyqtSignal(list)
    export_res = pyqtSignal(object)

    def __init__(self, crypto_service: CryptoService, export_service: ExportService):
        super().__init__()
        self.get_price_thread = None
        self.crypto_service = crypto_service
        self.export_service = export_service
        self.alert_manager = AlertManager()
        self.alert_manager.trigger.connect(self.alert)
        #self.member_alerts = self.crypto_service.get_all_alert()

    def start_monitoring(self, coin, source, ):
        if self.get_price_thread is None:
            self.get_price_thread = QThread()
            self.get_price_worker = GetPriceWorker(coin, source, self.crypto_service)
            self.get_price_worker.moveToThread(self.get_price_thread)
            try:
                self.get_price_thread.started.connect(self.get_price_worker.do_work)
                self.get_price_thread.start()
                self.get_price_worker.finished.connect(self.finish_get_price)
                self.get_price_worker.actual_price.connect(self.get_actual_price)
            except Exception as e:
                print(f"Ошибка при запуске потока: {e}")

    def finish_get_price(self):
            self.get_price_thread.quit()
            self.get_price_worker.deleteLater()
            self.get_price_thread.deleteLater()
            self.get_price_thread = None
            self.get_price_worker = None

    def get_actual_price(self, actual_price: dict):
        self.alert_manager.triggers(actual_price)
        self.actual_price.emit(actual_price)

    def stop_monitoring(self):
        self.get_price_worker.stop()

    def alert(self, alert_mes: BaseAlert):
        self.trigger_alert.emit(alert_mes.get_description())

    def get_history_data(self, coin, limit):
        self.history_data.emit(self.crypto_service.get_history_price(coin, limit))

    def export(self, exporter, coin, limit, filepath):
        res = self.export_service.export(exporter, coin, limit, filepath)
        if isinstance(res, str):
            self.export_res.emit(res)
        elif res is None:
            self.export_res.emit(None)