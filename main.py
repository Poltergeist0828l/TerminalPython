import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

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

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.stacked_widget = QStackedWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)

        self.welcome = TelaBemVindos(self)
        self.login = LoginScreen(self)
        self.cadastro_terminal = CadastroTerminalScreen(self)

        self.stacked_widget.addWidget(self.welcome)
        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.cadastro_terminal)

        # Inicializa como None
        self.terminal = None
        self.pagamento = None
        self.teclado = None
        self.app_payment = None
        self.pix = None
        self.confirmacao = None

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

        # QTimer.singleShot(100, self.executar_sincronizacao)

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

    def setCurrentWidget(self, widget):
        self.stacked_widget.setCurrentWidget(widget)

    def currentWidget(self):
        return self.stacked_widget.currentWidget()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    # Se quiser o cursor do mouse de volta para testar no PC, comente a linha abaixo
    # app.setOverrideCursor(Qt.BlankCursor)

    window.showFullScreen()

    sys.exit(app.exec_())
