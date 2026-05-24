import sys

from PyQt5.QtWidgets import QApplication, QStackedWidget

from service.SyncService import SyncService
from telas.bemvindo import TelaBemVindos
from telas.login_screen import LoginScreen
from telas.terminal_screen import TerminalScreen
from telas.pagamento import PagamentoScreen
from telas.teclado import TecladoScreen
from telas.pix import PixScreen


class MainWindow(QStackedWidget):

    def __init__(self):
        super().__init__()

        SyncService().sincronizar_produtos()

        self.resize(1600, 900)

        self.setWindowTitle(
            "Terminal Inteligente"
        )

        self.welcome = TelaBemVindos(self)

        self.login = LoginScreen(self)

        self.terminal = TerminalScreen(self)

        self.pagamento = PagamentoScreen(self)

        self.teclado = TecladoScreen(self)

        # NOVA TELA PIX
        self.pix = PixScreen(self)

        self.addWidget(self.welcome)

        self.addWidget(self.login)

        self.addWidget(self.teclado)

        self.addWidget(self.terminal)

        self.addWidget(self.pagamento)

        # ADICIONA PIX
        self.addWidget(self.pix)

        self.setCurrentWidget(
            self.welcome
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

    window.showMaximized()

    sys.exit(app.exec_())
