<<<<<<< HEAD
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)

=======
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
>>>>>>> 7ef3cd1cbce0b7da6837dd421a215aa1b3a4bf13
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class PagamentoScreen(QWidget):
<<<<<<< HEAD

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

=======
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        try:
            with open("css/terminal_screen.css", "r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())
>>>>>>> 7ef3cd1cbce0b7da6837dd421a215aa1b3a4bf13
        except:
            pass

        main_layout = QHBoxLayout(self)
<<<<<<< HEAD

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(0)

        self.sidebar = QFrame()

        self.sidebar.setObjectName(
            "sidebar"
        )

        self.sidebar.setFixedWidth(400)

        layout_lateral = QVBoxLayout(
            self.sidebar
        )

        self.logo = QLabel()

        pixmap = QPixmap("css/ima.png")

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

        layout_lateral.addSpacing(40)

        lbl_total = QLabel(
            "TOTAL A PAGAR"
        )

        lbl_total.setStyleSheet(
            "color: #8dd4ff; font-size: 18px;"
        )

        self.total_final = QLabel(
            "R$ 0,00"
        )

        self.total_final.setObjectName(
            "totalBox"
        )

        layout_lateral.addWidget(
            lbl_total,
            alignment=Qt.AlignCenter
        )

        layout_lateral.addWidget(
            self.total_final
        )

        layout_lateral.addStretch()

        self.content = QFrame()

        self.content.setObjectName(
            "content"
        )

        layout_opcoes = QVBoxLayout(
            self.content
        )

        layout_opcoes.setContentsMargins(
            50,
            50,
            50,
            50
        )

        titulo = QLabel(
            "SELECIONE A FORMA DE PAGAMENTO"
        )

        titulo.setObjectName(
            "header"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        grid_pagamento = QVBoxLayout()

        grid_pagamento.setSpacing(20)

        self.btn_pix = QPushButton(
            "💠 PIX (QR CODE)"
        )

        self.btn_pix.setObjectName(
            "app"
        )

        self.btn_pix.setMinimumHeight(100)

        self.btn_credito = QPushButton(
            "💳 CARTÃO DE CRÉDITO"
        )

        self.btn_credito.setObjectName(
            "pay"
        )

        self.btn_credito.setMinimumHeight(100)

        self.btn_debito = QPushButton(
            "💳 CARTÃO DE DÉBITO"
        )

        self.btn_debito.setObjectName(
            "app"
        )

        self.btn_debito.setMinimumHeight(100)

        self.btn_voltar = QPushButton(
            "CANCELAR / VOLTAR"
        )

        self.btn_voltar.setStyleSheet(
            """
            background: #e74c3c;
            margin-top: 40px;
            color: white;
            border-radius: 12px;
            padding: 15px;
            """
        )

        self.btn_voltar.clicked.connect(
            lambda: self.parent.setCurrentWidget(
                self.parent.terminal
            )
        )

        # PIX ABRE TELA PIX
        self.btn_pix.clicked.connect(
            self.ir_para_pix
        )

        self.btn_credito.clicked.connect(
            self.finalizar_venda
        )

        self.btn_debito.clicked.connect(
            self.finalizar_venda
        )

        grid_pagamento.addWidget(
            self.btn_pix
        )

        grid_pagamento.addWidget(
            self.btn_credito
        )

        grid_pagamento.addWidget(
            self.btn_debito
        )

        layout_opcoes.addWidget(
            titulo
        )

        layout_opcoes.addSpacing(40)

        layout_opcoes.addLayout(
            grid_pagamento
        )

        layout_opcoes.addStretch()

        layout_opcoes.addWidget(
            self.btn_voltar
        )

        main_layout.addWidget(
            self.sidebar
        )

        main_layout.addWidget(
            self.content
        )

    def ir_para_pix(self):

        valor = self.total_final.text()

        self.parent.pix.iniciar_pagamento(
            valor
        )

        self.parent.setCurrentWidget(
            self.parent.pix
        )

    def finalizar_venda(self):

        self.parent.terminal.total = 0

        self.parent.terminal.id_contador = 1

        self.parent.terminal.peso_total_venda = 0.0

        self.parent.terminal.totalBox.setText(
            "R$ 0,00"
        )

        self.parent.terminal.peso_display.setText(
            "0.000 KG"
        )

        for i in reversed(
            range(
                self.parent.terminal.productsLayout.count()
            )
        ):

            widget = self.parent.terminal.productsLayout.itemAt(i).widget()

            if widget:
                widget.setParent(None)

        self.parent.setCurrentWidget(
            self.parent.welcome
        )
=======
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(400)
        layout_lateral = QVBoxLayout(self.sidebar)

        self.logo = QLabel()
        pixmap = QPixmap("css/ima.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        layout_lateral.addWidget(self.logo, alignment=Qt.AlignCenter)
        layout_lateral.addSpacing(40)

        lbl_total = QLabel("TOTAL A PAGAR")
        lbl_total.setStyleSheet("color: #8dd4ff; font-size: 18px;")

        self.total_final = QLabel("R$ 0,00")
        self.total_final.setObjectName("totalBox")

        layout_lateral.addWidget(lbl_total, alignment=Qt.AlignCenter)
        layout_lateral.addWidget(self.total_final)
        layout_lateral.addStretch()

        self.content = QFrame()
        self.content.setObjectName("content")
        layout_opcoes = QVBoxLayout(self.content)
        layout_opcoes.setContentsMargins(50, 50, 50, 50)

        titulo = QLabel("SELECIONE A FORMA DE PAGAMENTO")
        titulo.setObjectName("header")
        titulo.setAlignment(Qt.AlignCenter)

        grid_pagamento = QVBoxLayout()
        grid_pagamento.setSpacing(20)

        self.btn_pix = QPushButton("💠 PIX (QR CODE)")
        self.btn_pix.setObjectName("app")
        self.btn_pix.setMinimumHeight(100)

        self.btn_credito = QPushButton("💳 CARTÃO DE CRÉDITO")
        self.btn_credito.setObjectName("pay")
        self.btn_credito.setMinimumHeight(100)

        self.btn_debito = QPushButton("💳 CARTÃO DE DÉBITO")
        self.btn_debito.setObjectName("app")
        self.btn_debito.setMinimumHeight(100)

        self.btn_voltar = QPushButton("CANCELAR / VOLTAR")
        self.btn_voltar.setStyleSheet(
            "background: #e74c3c; margin-top: 40px; color: white; border-radius: 12px; padding: 15px;")
        self.btn_voltar.clicked.connect(lambda: self.parent.setCurrentWidget(self.parent.terminal))

        self.btn_pix.clicked.connect(self.finalizar_venda)
        self.btn_credito.clicked.connect(self.finalizar_venda)
        self.btn_debito.clicked.connect(self.finalizar_venda)

        grid_pagamento.addWidget(self.btn_pix)
        grid_pagamento.addWidget(self.btn_credito)
        grid_pagamento.addWidget(self.btn_debito)

        layout_opcoes.addWidget(titulo)
        layout_opcoes.addSpacing(40)
        layout_opcoes.addLayout(grid_pagamento)
        layout_opcoes.addStretch()
        layout_opcoes.addWidget(self.btn_voltar)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content)

    def finalizar_venda(self):
        self.parent.terminal.total = 0
        self.parent.terminal.id = 1
        self.parent.terminal.peso_acumulado = 0.0
        self.parent.terminal.totalBox.setText("R$ 0,00")
        self.parent.terminal.peso.setText("0.000 KG")

        for i in reversed(range(self.parent.terminal.productsLayout.count())):
            widget = self.parent.terminal.productsLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.parent.setCurrentWidget(self.parent.welcome)
>>>>>>> 7ef3cd1cbce0b7da6837dd421a215aa1b3a4bf13
