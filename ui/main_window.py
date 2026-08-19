from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QTableWidget, QComboBox, QLabel, QPushButton, QFileDialog, QLineEdit, QMessageBox, QTableWidgetItem
from ..settings import MAPPING
from .alerts_panel import AlertPanel
from ..viewmodel.crypto_viewmodel import CryptoViewModel
from ..model.coin_model import CoinModel
from .notification_pop_up import NotificationPopUp
from typing import Any


class MainWindow(QMainWindow):
    def __init__(self, cryptoviewmodel: CryptoViewModel) -> None:
        super().__init__()
        self.viewmodel = cryptoviewmodel
        self.initialize_ui()
        self.viewmodel.actual_price.connect(self.refresh_price)
        self.viewmodel.trigger_alert.connect(self.trigger_alert)
        self.viewmodel.history_data.connect(self.get_historic_data)
        self.viewmodel.export_res.connect(self.finish_export)
        self.notifications = []

    def initialize_ui(self) -> None:
        self.setGeometry(200, 200, 1000, 1000)
        self.setWindowTitle('CRYPTO_AGGREGATOR')
        #Основной виджет
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        #Основной горизонтальный слой(для цены + таблицы + левой панели)
        self.main_box = QHBoxLayout()
        self.main_widget.setLayout(self.main_box)
        #Левый вертикальный слой для цены и таблицы
        self.price_table_layout = QVBoxLayout()
        self.alert_layout = AlertPanel(self.viewmodel)
        self.alert_layout.setVisible(False)
        self.main_box.addLayout(self.price_table_layout)
        self.main_box.addWidget(self.alert_layout)
        #Слои для цены + таблицы + нижних кнопок
        self.price_layout = QHBoxLayout()
        self.table_widghet = QTableWidget()
        self.table_widghet.setColumnCount(4)
        self.table_widghet.setHorizontalHeaderLabels(['Монета', 'Время', 'Цена', 'Источник'])
        self.button_layout = QHBoxLayout()
        self.price_table_layout.addLayout(self.price_layout)
        self.price_table_layout.addWidget(self.table_widghet)
        self.price_table_layout.addLayout(self.button_layout)
        # Наполнение ряда с ценой
        self.coin = QComboBox()
        self.coin.addItems(MAPPING.keys())
        self.price = QLabel()
        self.spred = QLabel()
        self.open_panel_button = QPushButton('+')
        self.open_panel_button.clicked.connect(self.open_right_panel)
        self.price_layout.addWidget(self.coin)
        self.price_layout.addWidget(self.price)
        self.price_layout.addWidget(self.spred)
        self.price_layout.addWidget(self.open_panel_button)
        # Наполнение ряда с кнопками
        self.file_expansion = QComboBox()
        self.file_expansion.addItems(['csv', 'html', 'json'])
        self.limit = QLineEdit()
        self.export_button = QPushButton('Экспортировать')
        self.refresh_price_button = QPushButton('Обновить')
        self.export_button.clicked.connect(self.export)
        self.refresh_price_button.clicked.connect(self.update_price_ui)
        self.button_layout.addWidget(self.limit)
        self.button_layout.addWidget(self.file_expansion)
        self.button_layout.addWidget(self.refresh_price_button)
        self.button_layout.addWidget(self.export_button)

        self.show()

    def open_right_panel(self) -> None:
        self.alert_layout.setVisible(not self.alert_layout.isVisible())

    def export(self) -> None:
        filepath,_ = QFileDialog.getSaveFileName(self, 'Сохранить файл как')
        if filepath != '':
            try:
                self.viewmodel.export(self.file_expansion.currentText(), self.coin.currentText(), int(self.limit.text()), filepath)
            except:
                self.viewmodel.export(self.file_expansion.currentText(), self.coin.currentText(), 1000, filepath)
        else:
            pass

    def finish_export(self, res: str | None) -> None:
        if isinstance(res, str):
            QMessageBox.information('Успех', 'Успешное сохранение файла!')
        else:
            QMessageBox.critical('Ошибка', 'Ошибка при сохранении файла!')

    def refresh_price(self, prices: dict[str, CoinModel | float | None]) -> None:
        my_prices = [prices[key].price for key in prices if key not in ('spred', 'net_spred') and prices[key] is not None and prices[key].price is not None]
        if len(my_prices) != 0 and all(my_prices):
            self.price.setText(str(max(my_prices)))
            self.spred.setText(str(prices['spred']))

    def update_price_ui(self) -> None:
        self.viewmodel.stop_monitoring()
        self.viewmodel.start_monitoring(self.coin.currentText())
        try:
            self.viewmodel.get_history_data(self.coin.currentText(), int(self.limit.text()))
        except:
            self.viewmodel.get_history_data(self.coin.currentText(), 1000)

    def trigger_alert(self, mes: Any) -> None:
        notification = NotificationPopUp(mes)
        self.notifications.append(notification)
        notification.show()

    def get_historic_data(self, data: list[CoinModel]) -> None:
        counter = 0
        self.table_widghet.setRowCount(len(data))
        for i in data:
            if isinstance(i, CoinModel):
                first_cell = QTableWidgetItem(str(i.name))
                second_cell = QTableWidgetItem(str(i.time))
                third_cell = QTableWidgetItem(str(i.price))
                fourth_cell = QTableWidgetItem(str(i.source))
                self.table_widghet.setItem(counter, 0, first_cell)
                self.table_widghet.setItem(counter, 1, second_cell)
                self.table_widghet.setItem(counter, 2, third_cell)
                self.table_widghet.setItem(counter, 3, fourth_cell)
                counter += 1

    def closeEvent(self, a0):
        self.viewmodel.stop_monitoring()
        self.viewmodel = None
        a0.accept()
        return super().closeEvent(a0)