from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt



class NotificationPopUp(QWidget):
    def __init__(self, alert: list[str]) -> None:
        super().__init__()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.alert = alert
        self.initialize_ui()

    def initialize_ui(self) -> None:
        self.main_layout = QVBoxLayout()

        self.name = QLabel(f'Сработал алёрт {self.alert[0]}')
        self.messege = QLabel(f'{self.alert[1]}')
        self.close_button = QPushButton('Закрыть')
        self.close_button.clicked.connect(self.close)

        self.main_layout.addWidget(self.name)
        self.main_layout.addWidget(self.messege)
        self.main_layout.addWidget(self.close_button)
        self.setLayout(self.main_layout)