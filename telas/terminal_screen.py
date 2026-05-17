from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QLineEdit, QScrollArea
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import requests
import serial
import re


class TerminalScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        try:
            with open("css/terminal_screen.css", "r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Erro: Arquivo css/terminal_screen.css não encontrado!")

        self.total = 0.0
        self.id_contador = 1
        self.peso_total_venda = 0.0

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(400)
        layout_lateral = QVBoxLayout(self.sidebar)

        self.logo = QLabel()
        pixmap = QPixmap("css/ima.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)

        self.totalBox = QLabel("R$ 0,00")
        self.totalBox.setObjectName("totalBox")
        self.totalBox.setAlignment(Qt.AlignCenter)

        self.status_api = QLabel("Conectando Local...")
        self.status_api.setObjectName("api")

        layout_lateral.addWidget(self.logo)
        layout_lateral.addSpacing(40)
        layout_lateral.addWidget(QLabel("VALOR TOTAL"))
        layout_lateral.addWidget(self.totalBox)
        layout_lateral.addStretch()
        layout_lateral.addWidget(self.status_api)

        self.content = QFrame()
        self.content.setObjectName("content")
        layout_conteudo = QVBoxLayout(self.content)

        self.cabecalho = QLabel("ID        CÓDIGO        PRODUTO        PESO(KG)        VALOR")
        self.cabecalho.setObjectName("header")

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")

        self.productsContainer = QWidget()
        self.productsLayout = QVBoxLayout(self.productsContainer)
        self.productsLayout.setAlignment(Qt.AlignTop)
        self.productsLayout.setSpacing(5)

        self.scroll.setWidget(self.productsContainer)

        layout_inputs = QHBoxLayout()
        self.codigo_barras = QLineEdit()
        self.codigo_barras.setPlaceholderText("Aguardando leitura do produto...")
        self.codigo_barras.returnPressed.connect(self.readProduct)

        self.peso_display = QLineEdit()
        self.peso_display.setText("0.000 KG")
        self.peso_display.setFixedWidth(180)
        self.peso_display.setReadOnly(True)

        layout_inputs.addWidget(self.codigo_barras)
        layout_inputs.addWidget(self.peso_display)

        layout_botoes = QHBoxLayout()
        self.btn_pagar = QPushButton("PAGAR AGORA")
        self.btn_pagar.setObjectName("pay")
        self.btn_pagar.clicked.connect(self.ir_para_pagamento)

        self.btn_app = QPushButton("PAGAR NO APP")
        self.btn_app.setObjectName("app")

        layout_botoes.addWidget(self.btn_pagar)
        layout_botoes.addWidget(self.btn_app)

        layout_conteudo.addWidget(self.cabecalho)
        layout_conteudo.addWidget(self.scroll, 1)
        layout_conteudo.addLayout(layout_inputs)
        layout_conteudo.addSpacing(10)
        layout_conteudo.addLayout(layout_botoes)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content)

        self.timer_foco = QTimer()
        self.timer_foco.timeout.connect(self.garantir_foco)
        self.timer_foco.start(1000)

    def garantir_foco(self):
        if self.parent and self.parent.currentWidget() == self:
            if not self.codigo_barras.hasFocus():
                self.codigo_barras.setFocus()

    def ir_para_pagamento(self):
        valor_final = self.totalBox.text()
        self.parent.pagamento.total_final.setText(valor_final)
        self.parent.setCurrentWidget(self.parent.pagamento)

    def ler_balanca(self):
        try:
            ser = serial.Serial('COM3', 9600, timeout=0.5)
            leitura = ser.readline().decode('utf-8').strip()
            ser.close()
            resultado = re.findall(r"[-+]?\d*\.\d+|\d+", leitura)
            return float(resultado[0]) if resultado else 0.0
        except Exception as e:
            print(f"Erro balança: {e}")
            return 0.0

    def remover_produto(self, widget_linha, valor, peso):

        self.total -= valor
        self.peso_total_venda -= peso

        self.totalBox.setText(f"R$ {max(0, self.total):.2f}")
        self.peso_display.setText(f"{max(0, self.peso_total_venda):.3f} KG")

        widget_linha.deleteLater()

    def readProduct(self):
        barcode = self.codigo_barras.text().strip()
        if not barcode: return

        peso_venda = self.ler_balanca()

        if peso_venda <= 0:
            self.status_api.setText("⚠️ Coloque na balança")
            self.status_api.setStyleSheet("color: #ffcc00;")
            self.codigo_barras.clear()
            return

        url_local = f"http://localhost:8080/produtos/{barcode}"

        try:
            resp_produto = requests.get(url_local, timeout=2)

            if resp_produto.status_code == 200:
                data = resp_produto.json()
                nome_prod = data.get("nome", "Desconhecido")
                preco_prod = float(data.get("preco", 0))

                valor_item = (preco_prod * peso_venda)

                self.total += valor_item
                self.peso_total_venda += peso_venda

                linha_widget = QFrame()
                linha_widget.setObjectName("linha_produto")
                layout_linha = QHBoxLayout(linha_widget)
                layout_linha.setContentsMargins(10, 5, 10, 5)

                texto_formatado = f"{self.id_contador:<8} {barcode:<18} {nome_prod:<25} {peso_venda:>6.3f}kg  R$ {valor_item:>7.2f}"
                lbl_texto = QLabel(texto_formatado)
                lbl_texto.setObjectName("item")

                btn_remover = QPushButton("🗑️")
                btn_remover.setFixedWidth(40)
                btn_remover.setCursor(Qt.PointingHandCursor)
                btn_remover.setStyleSheet("background: transparent; font-size: 20px; color: #ff4d4d; border: none;")

                btn_remover.clicked.connect(lambda: self.remover_produto(linha_widget, valor_item, peso_venda))

                layout_linha.addWidget(lbl_texto, 1)
                layout_linha.addWidget(btn_remover)

                self.productsLayout.addWidget(linha_widget)

                self.totalBox.setText(f"R$ {self.total:.2f}")
                self.peso_display.setText(f"{self.peso_total_venda:.3f} KG")

                self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())
                self.id_contador += 1
                self.status_api.setText("✅ Local Conectado")
                self.status_api.setStyleSheet("color: #62c8ff;")
            else:
                self.status_api.setText(f"❌ Produto não cadastrado")
                self.status_api.setStyleSheet("color: #ff4d4d;")

        except requests.exceptions.ConnectionError:
            self.status_api.setText("⚠️ Java Desligado")
            self.status_api.setStyleSheet("color: #ff4d4d;")
        except Exception as e:
            self.status_api.setText("⚠️ Erro no Link")
            print(f"Erro: {e}")

        self.codigo_barras.clear()
        self.codigo_barras.setFocus()
