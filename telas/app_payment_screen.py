import threading
from io import BytesIO

import requests
from PIL import Image

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QPushButton
)


class AppPaymentScreen(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        try:

            with open(
                "css/terminal_screen.css",
                "r",
                encoding="utf-8"
            ) as file:

                self.setStyleSheet(
                    file.read()
                )

        except:
            pass

        main_layout = QHBoxLayout(self)

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(0)

        # SIDEBAR
        self.sidebar = QFrame()

        self.sidebar.setObjectName(
            "sidebar"
        )

        self.sidebar.setFixedWidth(400)

        layout_lateral = QVBoxLayout(
            self.sidebar
        )

        self.logo = QLabel()

        pixmap = QPixmap(
            "css/ima.png"
        )

        if not pixmap.isNull():

            self.logo.setPixmap(
                pixmap.scaled(
                    200,
                    200,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        layout_lateral.addWidget(
            self.logo,
            alignment=Qt.AlignCenter
        )

        layout_lateral.addSpacing(30)

        titulo_total = QLabel(
            "TOTAL"
        )

        titulo_total.setStyleSheet(
            "color:#8dd4ff;font-size:18px;"
        )

        self.total_label = QLabel(
            "R$ 0,00"
        )

        self.total_label.setObjectName(
            "totalBox"
        )

        layout_lateral.addWidget(
            titulo_total,
            alignment=Qt.AlignCenter
        )

        layout_lateral.addWidget(
            self.total_label
        )

        layout_lateral.addStretch()

        self.status = QLabel(
            "Aguardando..."
        )

        self.status.setObjectName(
            "api"
        )

        layout_lateral.addWidget(
            self.status
        )

        # CONTENT
        self.content = QFrame()

        self.content.setObjectName(
            "content"
        )

        layout_content = QVBoxLayout(
            self.content
        )

        layout_content.setContentsMargins(
            40,
            40,
            40,
            40
        )

        self.titulo = QLabel(
            "CONTINUE O PAGAMENTO NO APP"
        )

        self.titulo.setObjectName(
            "header"
        )

        self.titulo.setAlignment(
            Qt.AlignCenter
        )

        self.loading = QLabel(
            "Gerando QR Code..."
        )

        self.loading.setAlignment(
            Qt.AlignCenter
        )

        self.loading.setStyleSheet(
            "font-size:20px;color:white;"
        )

        self.qr_label = QLabel()

        self.qr_label.setAlignment(
            Qt.AlignCenter
        )

        self.btn_cancelar = QPushButton(
            "CANCELAR"
        )

        self.btn_cancelar.setStyleSheet(
            """
            background:#e74c3c;
            color:white;
            border-radius:12px;
            padding:15px;
            font-size:18px;
            """
        )

        self.btn_cancelar.clicked.connect(
            lambda: self.parent.setCurrentWidget(
                self.parent.pagamento
            )
        )

        layout_content.addWidget(
            self.titulo
        )

        layout_content.addSpacing(30)

        layout_content.addWidget(
            self.loading
        )

        layout_content.addWidget(
            self.qr_label,
            1
        )

        layout_content.addStretch()

        layout_content.addWidget(
            self.btn_cancelar
        )

        main_layout.addWidget(
            self.sidebar
        )

        main_layout.addWidget(
            self.content
        )

    def iniciar_pagamento(self, valor):

        self.total_label.setText(
            valor
        )

        self.loading.show()

        self.loading.setText(
            "Gerando pagamento no aplicativo..."
        )

        self.qr_label.clear()

        self.status.setText(
            "Gerando checkout..."
        )

        self.status.setStyleSheet(
            "color:#62c8ff;"
        )

        threading.Thread(
            target=self.gerar_checkout,
            daemon=True
        ).start()

    def gerar_checkout(self):

        try:

            carrinho = self.parent.terminal.carrinho

            # cria carrinho
            response = requests.post(

                "http://localhost:8080/carrinho",

                json=carrinho.to_dict()

            )

            dados = response.json()

            carrinho_id = dados["carrinhoId"]

            # cria sessão checkout
            response = requests.get(

                "http://localhost:8080/checkout/carrinho?idCarrinho="
                + carrinho_id

            )

            dados = response.json()

            session_id = dados["sessionId"]

            # pega qrcode
            response = requests.get(

                "http://localhost:8080/checkout/qrcode?id="
                + session_id

            )

            imagem_bytes = response.content

            imagem = Image.open(
                BytesIO(imagem_bytes)
            )

            imagem.save(
                "temp_checkout.png"
            )

            pixmap = QPixmap(
                "temp_checkout.png"
            )

            pixmap = pixmap.scaled(
                320,
                320,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.loading.hide()

            self.qr_label.setPixmap(
                pixmap
            )

            self.status.setText(
                "✓ Escaneie no aplicativo"
            )

            self.status.setStyleSheet(
                "color:#62c8ff;"
            )

        except Exception as e:

            print(e)

            self.loading.setText(
                "Erro ao gerar checkout"
            )

            self.status.setText(
                "✗ Falha no pagamento"
            )

            self.status.setStyleSheet(
                "color:#ff4d4d;"
            )