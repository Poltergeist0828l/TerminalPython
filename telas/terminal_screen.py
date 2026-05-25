from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame,
    QLineEdit, QScrollArea
)

from database.DatabaseProdutos import DatabaseProdutos
from database.PaymentListener import PaymentListener
from model.Carrinho import Carrinho
from model.Item import Item
from model.Produtos import Produtos


class TerminalScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)  # Chame o super() ANTES de criar os filhos!
        self.parent_app = parent  # Mudei o nome para evitar confusão com o parent do QWidget

        self.db = DatabaseProdutos()
        self.carrinho = Carrinho("T01")

        # 1. Instancia a nova classe QThread (passando self como parent)
        self.listener = PaymentListener(self)

        # 2. Conecta o sinal à função de limpar a tela
        # Usamos Qt.QueuedConnection para forçar que execute na thread principal
        self.listener.pagamento_aprovado_signal.connect(self.pagamento_aprovado, Qt.QueuedConnection)

        # 3. Inicia a thread
        self.listener.start()

        super().__init__()

        try:
            with open(
                    "css/terminal_screen.css",
                    "r",
                    encoding="utf-8"
            ) as file:

                self.setStyleSheet(
                    file.read()
                )

        except FileNotFoundError:

            print(
                "Erro: Arquivo css/terminal_screen.css não encontrado!"
            )

        self.parent = parent

        self.total = 0.0
        self.id_contador = 1
        self.peso_total_venda = 0.0

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(400)

        layout_lateral = QVBoxLayout(self.sidebar)

        self.logo = QLabel()
        pixmap = QPixmap("css/ima.png")

        if not pixmap.isNull():
            self.logo.setPixmap(
                pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

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

        # CONTENT
        self.content = QFrame()
        self.content.setObjectName("content")

        layout_conteudo = QVBoxLayout(self.content)

        self.cabecalho = QLabel(
            "ID        CÓDIGO        PRODUTO        QTD        VALOR"
        )
        self.cabecalho.setObjectName("header")

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border:none; background:transparent;")

        self.productsContainer = QWidget()
        self.productsLayout = QVBoxLayout(self.productsContainer)
        self.productsLayout.setAlignment(Qt.AlignTop)
        self.productsLayout.setSpacing(5)

        self.scroll.setWidget(self.productsContainer)

        # INPUTS
        layout_inputs = QHBoxLayout()

        self.codigo_barras = QLineEdit()
        self.codigo_barras.setPlaceholderText("Aguardando leitura do produto...")
        self.codigo_barras.returnPressed.connect(self.readProduct)

        self.peso_display = QLineEdit("0.000 KG")
        self.peso_display.setFixedWidth(180)
        self.peso_display.setReadOnly(True)

        layout_inputs.addWidget(self.codigo_barras)
        layout_inputs.addWidget(self.peso_display)

        # BOTÕES
        layout_botoes = QHBoxLayout()

        self.btn_pagar = QPushButton("PAGAR AGORA")
        self.btn_pagar.setObjectName("pay")
        self.btn_pagar.clicked.connect(self.ir_para_pagamento)

        self.btn_app = QPushButton("PAGAR NO APP")
        self.btn_app.setObjectName("app")
        self.btn_app.clicked.connect(self.ir_para_app)

        layout_botoes.addWidget(self.btn_pagar)
        layout_botoes.addWidget(self.btn_app)

        layout_conteudo.addWidget(self.cabecalho)
        layout_conteudo.addWidget(self.scroll, 1)
        layout_conteudo.addLayout(layout_inputs)
        layout_conteudo.addSpacing(10)
        layout_conteudo.addLayout(layout_botoes)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content)

        # FOCO
        self.timer_foco = QTimer()
        self.timer_foco.timeout.connect(self.garantir_foco)
        self.timer_foco.start(1000)

    # ================= UI =================

    def atualizar_interface(self):
        self.totalBox.setText(self.carrinho.total_formatado())
        self.peso_display.setText(f"{self.peso_total_venda:.3f} KG")

    def atualizar_linha(self, codigo, label):
        item = self.carrinho.buscar_item(codigo)
        if not item:
            return

        label.setText(
            f"{self.id_contador:<8} "
            f"{codigo:<18} "
            f"{item.produto.nome:<25} "
            f"{item.quantidade:>3}x   "
            f"R$ {item.subtotal():>7.2f}"
        )

    # ================= QUANTIDADE =================

    def aumentar_quantidade(self, codigo, label):
        item = self.carrinho.buscar_item(codigo)
        if not item:
            return

        item.quantidade += 1
        self.atualizar_interface()
        self.atualizar_linha(codigo, label)

    def diminuir_quantidade(self, codigo, widget, label):
        item = self.carrinho.buscar_item(codigo)
        if not item:
            return

        item.quantidade -= 1

        if item.quantidade <= 0:
            self.remover_produto(codigo, widget)
        else:
            self.atualizar_interface()
            self.atualizar_linha(codigo, label)

    # ================= NAVEGAÇÃO =================

    def pagamento_aprovado(self, data):
        print("✅ Pagamento confirmado via Redis!")

        if self.parent_app:
            self.parent_app.setCurrentWidget(self.parent_app.confirmacao)
            self.parent_app.confirmacao.mostrar_tela()

    def liberar_tela(self):
        print("🧹 Limpando a tela...")
        self.carrinho = Carrinho("T01")

        # Limpa layout da lista de forma segura
        while self.productsLayout.count():
            item = self.productsLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        # Reseta variáveis
        self.total = 0.0
        self.id_contador = 1
        self.peso_total_venda = 0.0

        # Atualiza UI
        self.totalBox.setText("R$ 0,00")
        self.peso_display.setText("0.000 KG")

        print("✨ Terminal resetado em background!")

    def garantir_foco(self):
        # Modificado para acessar o stacked_widget de dentro da MainWindow
        if self.parent and self.parent.stacked_widget.currentWidget() == self:
            # seu código de foco atual...

            if not self.codigo_barras.hasFocus():
                self.codigo_barras.setFocus()

    def ir_para_pagamento(self):
        if self.parent_app:
            self.parent_app.pagamento.total_final.setText(self.totalBox.text())
            self.parent_app.setCurrentWidget(self.parent_app.pagamento)

    def ir_para_app(self):
        if self.parent_app:
            self.parent_app.app_payment.iniciar_pagamento(self.totalBox.text())
            self.parent_app.setCurrentWidget(self.parent_app.app_payment)

    # ================= REMOVER =================

    def remover_produto(self, codigo_produto, widget_linha):
        item = self.carrinho.buscar_item(codigo_produto)
        if not item:
            return

        self.carrinho.remover_item(codigo_produto)

        self.totalBox.setText(self.carrinho.total_formatado())

        widget_linha.deleteLater()

    # ================= LEITURA =================

    def readProduct(self):

        barcode = self.codigo_barras.text().strip()
        if not barcode:
            return

        try:
            tupla = self.db.buscar_por_codigo(barcode)

            if not tupla:
                self.status_api.setText("Produto não cadastrado")
                self.status_api.setStyleSheet("color:#ff4d4d;")
                return

            produto = Produtos.from_tuple(tupla)

            item = self.carrinho.buscar_item(produto.codigo)

            if item:
                item.quantidade += 1
            else:
                item = Item(produto=produto, quantidade=1, received_weight=1.0)
                self.carrinho.adicionar_item(item)

            self.peso_total_venda += 1.0

            linha_widget = QFrame()
            layout_linha = QHBoxLayout(linha_widget)
            layout_linha.setContentsMargins(10, 5, 10, 5)

            item = self.carrinho.buscar_item(produto.codigo)

            lbl_texto = QLabel(
                f"{self.id_contador:<8} "
                f"{produto.codigo:<18} "
                f"{produto.nome:<25} "
                f"{item.quantidade:>3}x   "
                f"R$ {item.subtotal():>7.2f}"
            )

            btn_menos = QPushButton("-")
            btn_mais = QPushButton("+")
            btn_remover = QPushButton("?")

            btn_menos.setFixedWidth(40)
            btn_mais.setFixedWidth(40)
            btn_remover.setFixedWidth(40)

            btn_menos.clicked.connect(
                lambda _, c=produto.codigo, w=linha_widget, l=lbl_texto:
                self.diminuir_quantidade(c, w, l)
            )

            btn_mais.clicked.connect(
                lambda _, c=produto.codigo, l=lbl_texto:
                self.aumentar_quantidade(c, l)
            )

            btn_remover.clicked.connect(
                lambda _, c=produto.codigo, w=linha_widget:
                self.remover_produto(c, w)
            )
            btn_mais.setProperty("class", "action")
            btn_menos.setProperty("class", "action")
            btn_remover.setProperty("class", "danger")

            layout_linha.addWidget(lbl_texto, 1)
            layout_linha.addWidget(btn_menos)
            layout_linha.addWidget(btn_mais)
            layout_linha.addWidget(btn_remover)

            self.productsLayout.addWidget(linha_widget)

            self.totalBox.setText(self.carrinho.total_formatado())

            self.id_contador += 1

            self.codigo_barras.clear()
            self.codigo_barras.setFocus()

        except Exception as e:
            print("Erro:", e)
