from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class ConfirmacaoScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent

        # Layout Principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Estilização interna caso não queira usar CSS externo para esta tela
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
            }
            QLabel#lbl_check {
                color: #2ec4b6;
                font-size: 80px;
            }
            QLabel#lbl_sucesso {
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
            }
            QLabel#lbl_sub {
                color: #a0a0a0;
                font-size: 16px;
            }
            QPushButton#btn_voltar {
                background-color: #2ec4b6;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px 24px;
                margin-top: 20px;
            }
            QPushButton#btn_voltar:hover {
                background-color: #209f93;
            }
        """)

        # Elementos da Interface
        self.lbl_check = QLabel("✔")
        self.lbl_check.setObjectName("lbl_check")
        self.lbl_check.setAlignment(Qt.AlignCenter)

        self.lbl_sucesso = QLabel("PAGAMENTO APROVADO!")
        self.lbl_sucesso.setObjectName("lbl_sucesso")
        self.lbl_sucesso.setAlignment(Qt.AlignCenter)

        self.lbl_subtext = QLabel("Imprimindo cupom... A tela resetará em instantes.")
        self.lbl_subtext.setObjectName("lbl_sub")
        self.lbl_subtext.setAlignment(Qt.AlignCenter)

        self.btn_voltar = QPushButton("AVANÇAR AGORA (Enter)")
        self.btn_voltar.setObjectName("btn_voltar")
        self.btn_voltar.clicked.connect(self.finalizar_e_voltar)

        # Adiciona ao layout
        layout.addWidget(self.lbl_check)
        layout.addWidget(self.lbl_sucesso)
        layout.addWidget(self.lbl_subtext)
        layout.addWidget(self.btn_voltar)

        # Timer para fechar automaticamente
        self.timer_auto_fechar = QTimer(self)
        self.timer_auto_fechar.timeout.connect(self.finalizar_e_voltar)

    def mostrar_tela(self):
        """Chame esta função quando a tela for exibida para iniciar o cronômetro."""
        self.btn_voltar.setFocus()
        self.timer_auto_fechar.start(20000)  # 4000 milissegundos = 4 segundos

    def finalizar_e_voltar(self):
        self.timer_auto_fechar.stop()

        if self.parent_app:
            # 1. Executa a limpeza do carrinho no terminal (em background)
            self.parent_app.terminal.liberar_tela()

            # 2. Em vez de voltar para o terminal, joga o app para a tela Welcome
            # Certifique-se de usar o nome exato da sua variável da tela welcome aqui
            self.parent_app.setCurrentWidget(self.parent_app.welcome)
            
    def keyPressEvent(self, event):
        """Permite que o operador aperte Enter ou Espaço para ir mais rápido"""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self.finalizar_e_voltar()
        else:
            super().keyPressEvent(event)