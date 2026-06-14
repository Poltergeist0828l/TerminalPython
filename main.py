import os

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget,
    QVBoxLayout, QWidget, QSizePolicy
)

from model.Terminal import Terminal
from service.SyncService import SyncService
from service.TerminalSocket import TerminalSocket

from telas.CadastroTerminalScreen import CadastroTerminalScreen
from telas.ConfirmacaoScreen import ConfirmacaoScreen
from telas.app_payment_screen import AppPaymentScreen
from telas.bemvindo import TelaBemVindos
from telas.login_screen import LoginScreen
from telas.pagamento import PagamentoScreen
from telas.pix import PixScreen
from telas.teclado import TecladoScreen
from telas.terminal_screen import TerminalScreen


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Terminal Inteligente")

        # -----------------------------
        # CENTRAL WIDGET
        # -----------------------------
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # -----------------------------
        # STACKED RESPONSIVO
        # -----------------------------
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        # -----------------------------
        # LAYOUT CORRETO (FULL SCREEN)
        # -----------------------------
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.stacked_widget)

        # -----------------------------
        # TELAS
        # -----------------------------
        self.welcome = TelaBemVindos(self)
        self.login = LoginScreen(self)
        self.cadastro_terminal = CadastroTerminalScreen(self)

        self.stacked_widget.addWidget(self.welcome)
        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.cadastro_terminal)

        # -----------------------------
        # OUTRAS TELAS (lazy init)
        # -----------------------------
        self.terminal = None
        self.pagamento = None
        self.teclado = None
        self.app_payment = None
        self.pix = None
        self.confirmacao = None

        # -----------------------------
        # START LOGIC
        # -----------------------------
        if Terminal.is_activated():
            sync = SyncService()
            sync.iniciar_sync_em_thread()

            print("Aplicação continua executando...")

            self.inicializar_terminal()

            self.socket = TerminalSocket()
            self.socket.start()

            self.stacked_widget.setCurrentWidget(self.welcome)

        else:
            self.stacked_widget.setCurrentWidget(self.cadastro_terminal)

    # -----------------------------
    # INICIALIZA TELAS PESADAS
    # -----------------------------
    def inicializar_terminal(self):

        if self.terminal is not None:
            return

        self.terminal = TerminalScreen(self)
        self.pagamento = PagamentoScreen(self)
        self.teclado = TecladoScreen(self)
        self.app_payment = AppPaymentScreen(self)
        self.pix = PixScreen(self)
        self.confirmacao = ConfirmacaoScreen(self)

        self.stacked_widget.addWidget(self.confirmacao)
        self.stacked_widget.addWidget(self.app_payment)
        self.stacked_widget.addWidget(self.teclado)
        self.stacked_widget.addWidget(self.terminal)
        self.stacked_widget.addWidget(self.pagamento)
        self.stacked_widget.addWidget(self.pix)

    # -----------------------------
    # HELPERS
    # -----------------------------
    def setCurrentWidget(self, widget):
        self.stacked_widget.setCurrentWidget(widget)

    def currentWidget(self):
        return self.stacked_widget.currentWidget()


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    print("Screen size:", screen.size())
    print("Available geometry:", screen.availableGeometry())
    window = MainWindow()

    # cursor oculto (modo terminal)
    app.setOverrideCursor(Qt.BlankCursor)


#    window.setFixedSize(1024, 600)

    window.showFullScreen()
    #  window.show()
    # window.resize(800, 480)





    window.show()

    sys.exit(app.exec_())