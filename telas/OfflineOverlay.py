from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class OfflineOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgba(0,0,0,220);")

        layout = QVBoxLayout(self)

        self.label = QLabel("SEM INTERNET")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            color: white;
            font-size: 40px;
            font-weight: bold;
        """)

        self.sub = QLabel("Aguardando reconexão...")
        self.sub.setAlignment(Qt.AlignCenter)
        self.sub.setStyleSheet("color: #aaa; font-size: 18px;")

        layout.addWidget(self.label)
        layout.addWidget(self.sub)

    def showEvent(self, event):
        if self.parent():
            self.resize(self.parent().size())
        super().showEvent(event)