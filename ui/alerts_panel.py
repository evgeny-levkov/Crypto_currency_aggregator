from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton
from ..settings import MAPPING
from ..viewmodel.crypto_viewmodel import CryptoViewModel
from PyQt6.QtCore import pyqtSignal


class AlertPanel(QWidget):
    def __init__(self, viewmodel: CryptoViewModel) -> None:
        super().__init__()
        self.viewmodel = viewmodel
        self.initialize_ui()
        self.add_params()

    def initialize_ui(self) -> None:
        self.main_box = QVBoxLayout()
        self.params = []
        self.dynamic_params = {}
        self.setLayout(self.main_box)
        #Имя алёрта - вводится руками
        self.label_type = QLabel('Тип алёрта')
        self.alert_type = QComboBox()
        self.alert_type.addItem('price')
        self.alert_type.currentTextChanged.connect(self.add_params)
        self.label_alert = QLabel('Название алёрта')
        self.alert_name = QLineEdit()
        self.coin_name_label = QLabel('Монета')
        self.coin_name = QComboBox()
        self.coin_name.addItems(['BTC', 'ETH', 'SOL'])
        self.source_name_label = QLabel('Источник')
        self.source_name = QComboBox()
        self.source_name.addItems(['Binance', 'CoinGeko'])
        self.label_params = QLabel('Параметры алёрта:')
        self.place_new_params = QVBoxLayout()
        self.accept_button = QPushButton('Подтвердить')
        self.accept_button.clicked.connect(self.accept)

        self.main_box.addWidget(self.label_type)
        self.main_box.addWidget(self.alert_type)

        self.main_box.addWidget(self.label_alert)
        self.main_box.addWidget(self.alert_name)

        self.main_box.addWidget(self.coin_name_label)
        self.main_box.addWidget(self.coin_name)

        self.main_box.addWidget(self.source_name_label)
        self.main_box.addWidget(self.source_name)

        self.main_box.addWidget(self.label_params)
        self.main_box.addLayout(self.place_new_params)
        self.main_box.addWidget(self.accept_button)

        self.main_box.addStretch()

        self.show()

    def accept(self) -> None:
        par = {}
        for keys, values in self.dynamic_params.items():
            if isinstance(values, QComboBox):
                param = values.currentText()
            elif isinstance(values, QLineEdit):
                param = values.text()
            par[keys] = param
        par['user_alert_name'] = self.alert_name.text()
        self.viewmodel.add_alert(self.alert_type.currentText(), self.coin_name.currentText(), self.source_name.currentText(), **par)
        self.setVisible(False)

    def add_params(self) -> None:
        self.dynamic_params.clear()
        while self.place_new_params.count():
            item = self.place_new_params.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        self.alert_params = self.viewmodel.get_alert_fields(str(self.alert_type.currentText()))
        for keys in self.alert_params:
            label = QLabel(keys)
            if isinstance(self.alert_params[keys], list):
                param_widget = QComboBox()
                param_widget.addItems(self.alert_params[keys])
            else:
                param_widget = QLineEdit()
            self.place_new_params.addWidget(label)
            self.place_new_params.addWidget(param_widget)
            self.dynamic_params[keys] = param_widget


