from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
from PyQt5.QtGui import QPixmap

class TelaBemVindos(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        try:
            with open("css/bemvindo.css", "r", encoding="utf-8") as arquivo_css:
                self.setStyleSheet(arquivo_css.read())
        except:
            self.setStyleSheet("background-color: black;")

        layout_principal = QVBoxLayout()

        self.card = QFrame()
        self.card.setObjectName("centralCard")
        layout_cartao = QVBoxLayout(self.card)

        logo = QLabel()
        logo_pixmap = QPixmap("css/ima.png")
        if not logo_pixmap.isNull():
            logo.setPixmap(logo_pixmap.scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        titulo = QLabel("BEM VINDO")
        titulo.setObjectName("title")
        titulo.setAlignment(Qt.AlignCenter)

        subtitulo = QLabel("SEMPRE AQUI")
        subtitulo.setObjectName("subtitle")
        subtitulo.setAlignment(Qt.AlignCenter)


        self.relogio = QLabel()
        self.relogio.setObjectName("relogio")
        self.relogio.setAlignment(Qt.AlignCenter)

        botao_entrar = QPushButton("TOQUE PARA CONTINUAR")
        botao_entrar.setCursor(Qt.PointingHandCursor)
        botao_entrar.setFixedWidth(400)
        botao_entrar.clicked.connect(lambda: self.parent.setCurrentWidget(self.parent.login))

        layout_cartao.addStretch()
        layout_cartao.addWidget(logo)
        layout_cartao.addSpacing(10)
        layout_cartao.addWidget(subtitulo)
        layout_cartao.addWidget(titulo)
        layout_cartao.addSpacing(20)
        layout_cartao.addWidget(self.relogio)
        layout_cartao.addSpacing(40)
        layout_cartao.addWidget(botao_entrar, alignment=Qt.AlignCenter)
        layout_cartao.addStretch()

        layout_principal.addWidget(self.card)
        self.setLayout(layout_principal)

        timer = QTimer(self)
        timer.timeout.connect(self.atualizarRelogio)
        timer.start(1000)
        self.atualizarRelogio()

    def atualizarRelogio(self):
        now = datetime.now()
        self.relogio.setText(now.strftime("%H:%M:%S"))
