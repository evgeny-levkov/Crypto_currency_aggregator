from .ui.main_window import MainWindow
from .viewmodel.crypto_viewmodel import CryptoViewModel
from .service.crypto_service import CryptoService
from .service.export_service import ExportService
from .repository.crypto_repository import CryptoRepository
from .repository.api_repository import ApiRepository
from .repository.db_repository import DbRepository
from .repository.api.binance_api import BinanceApi
from .repository.api.coin_gecko_api import CoinGeckoApi
from .repository.db.sqlite_db import SqlLiteDb
from .settings import MAPPING
import sys
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    db = SqlLiteDb('my_db')
    coin_geko = CoinGeckoApi(MAPPING)
    binance = BinanceApi()
    api_repository = ApiRepository({'Binance': binance, 'CoinGeko': coin_geko})
    db_repository = DbRepository(db)
    crypto_repository = CryptoRepository(api_repository, db_repository)
    crypto_service = CryptoService(crypto_repository)
    export_service = ExportService(crypto_repository)
    viewmodel = CryptoViewModel(crypto_service, export_service)
    App = MainWindow(viewmodel)
    sys.exit(app.exec())