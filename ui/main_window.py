from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QTableWidget, QComboBox, QLabel, QPushButton, QFileDialog, QLineEdit, QMessageBox, QTableWidgetItem
from ..settings import MAPPING
from .alerts_panel import AlertPanel
from ..viewmodel.crypto_viewmodel import CryptoViewModel
from ..model.coin_model import CoinModel


class MainWindow(QMainWindow):
    def __init__(self, cryptoviewmodel: CryptoViewModel) -> None:
        super().__init__()
        self.viewmodel = cryptoviewmodel
        self.initialize_ui()
        self.viewmodel.actual_price.connect(self.refresh_price)
        self.viewmodel.trigger_alert.connect(self.trigger_alert)
        self.viewmodel.history_data.connect(self.get_historic_data)
        self.viewmodel.export_res.connect(self.export)

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
        self.export_button = QPushButton()
        self.refresh_price_button = QPushButton()
        self.export_button.clicked.connect(self.export)
        self.refresh_price_button.clicked.connect(self.refresh_price)
        self.button_layout.addWidget(self.limit)
        self.button_layout.addWidget(self.file_expansion)
        self.button_layout.addWidget(self.refresh_price_button)
        self.button_layout.addWidget(self.export_button)

        self.show()

    def open_right_panel(self) -> None:
        self.alert_layout.setVisible(not self.alert_layout.isVisible())

    def export(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл как')
        try:
            self.viewmodel.export(self.file_expansion.currentText(), self.coin.currentText(), int(self.limit.text()), file_path)
        except:
            QMessageBox.critical(self,'Ошибка', 'Ошибка сохранения файла')

    def refresh_price(self) -> None:
        self.viewmodel.stop_monitoring()
        self.viewmodel.start_monitoring(self.coin.currentText())

    def trigger_alert(self):
        pass

    def get_historic_data(self, data: list[CoinModel]):
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