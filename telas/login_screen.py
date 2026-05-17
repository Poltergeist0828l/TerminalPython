from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt
import requests


class LoginScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        try:
            with open("css/login_screen.css", "r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())
        except:
            pass

        root = QVBoxLayout(self)
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)

        title = QLabel("Como deseja continuar?")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        btn_identificar = QPushButton("IDENTIFICAR-SE (CPF)")
        btn_identificar.setObjectName("continue")
        btn_identificar.setMinimumHeight(80)
        btn_identificar.clicked.connect(lambda: self.parent.setCurrentWidget(self.parent.teclado))

        btn_anonimo = QPushButton("CONTINUAR ANÔNIMO")
        btn_anonimo.setObjectName("anonymous")
        btn_anonimo.setMinimumHeight(60)
        btn_anonimo.clicked.connect(self.continuar_anonimo)

        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(btn_identificar)
        layout.addSpacing(15)
        layout.addWidget(btn_anonimo)

        root.addStretch()
        root.addWidget(card, alignment=Qt.AlignCenter)
        root.addStretch()

    def continuar_anonimo(self):
        # Envia para o Spring Boot para registrar
        url = "http://localhost:8080/usuarios/anonimo"
        try:
            requests.post(url, json={"nome": "Visitante"}, timeout=2)
        except:
            print("Aviso: Back-end offline, continuando local...")

        self.ir_terminal()

    def ir_terminal(self):
        self.parent.setCurrentWidget(self.parent.terminal)
