from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from ..service.crypto_service import CryptoService
import time


class GetPriceWorker(QObject):
    actual_price = pyqtSignal(object)
    finished = pyqtSignal()

    def __init__(self, coin: str, source: list[str], crypto_service: CryptoService) -> None:
        super().__init__()
        self.crypto_service = crypto_service
        self._coin = coin
        self._source = source
        self._stop = False

    @pyqtSlot()
    def do_work(self) -> None:
        while not self._stop:
            res = self.crypto_service.get_actual_price(self._coin, self._source)
            self.actual_price.emit(res)
            for i in range(100):
                time.sleep(0.1)
                if self._stop:
                    break
        self.finished.emit()

    def stop(self) -> None:
        self._stop = True