from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton
from ..settings import MAPPING
from ..viewmodel.crypto_viewmodel import CryptoViewModel


class AlertPanel(QWidget):
    def __init__(self, viewmodel: CryptoViewModel) -> None:
        super().__init__()
        self.viewmodel = viewmodel
        self.initialize_ui()

    def initialize_ui(self) -> None:
        self.main_box = QVBoxLayout()
        self.params = []
        self.setLayout(self.main_box)
        #Имя алёрта - вводится руками
        self.label_alert = QLabel('Название алёрта')
        self.alert_name = QLineEdit()
        # Имя монеты - из выпадающего списка()
        self.label_coin = QLabel('Монета')
        self.coin_name = QComboBox()
        self.coin_name.addItems(MAPPING.keys())
        #Имя ресурса - из выпадающего списка(Binance, CoinGeko)
        self.label_source = QLabel('Источник')
        self.source_name = QComboBox()
        self.source_name.addItems(['Binance', 'CoinGeko'])
        #Другие параметры: имя + значение(добавление по кнопке)
        self.label_other_params = QLabel('Другие параметры алёрта')
        self.place_new_params = QVBoxLayout()
        self.add_params_button = QPushButton('+')
        self.add_params_button.clicked.connect(self.add_params)

        self.accept_button = QPushButton('Подтвердить')
        self.accept_button.clicked.connect(self.accept)

        self.main_box.addWidget(self.label_alert)
        self.main_box.addWidget(self.alert_name)
        self.main_box.addWidget(QLabel())
        self.main_box.addWidget(self.label_coin)
        self.main_box.addWidget(self.coin_name)
        self.main_box.addWidget(QLabel())
        self.main_box.addWidget(self.label_source)
        self.main_box.addWidget(self.source_name)
        self.main_box.addWidget(QLabel())
        self.main_box.addWidget(self.label_other_params)
        self.main_box.addLayout(self.place_new_params)
        self.main_box.addWidget(self.add_params_button)
        self.main_box.addWidget(self.accept_button)

        self.main_box.addStretch()

        self.show()

    def accept(self) -> None:
        par = {}
        for i in self.params:
            par[i[0].text()] = i[1].text()
        self.viewmodel.add_alert(self.alert_name.text(), self.coin_name.currentText(), self.source_name.currentText(), **par)

    def add_params(self) -> None:
        self.name = QLineEdit()
        self.value = QLineEdit()
        self.place_new_params.addWidget(self.name)
        self.place_new_params.addWidget(self.value)
        self.params.append((self.name, self.value))