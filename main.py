import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from service.SyncService import SyncService
from telas.ConfirmacaoScreen import ConfirmacaoScreen
from telas.app_payment_screen import AppPaymentScreen
from telas.bemvindo import TelaBemVindos
from telas.login_screen import LoginScreen
from telas.terminal_screen import TerminalScreen
from telas.pagamento import PagamentoScreen
from telas.teclado import TecladoScreen
from telas.pix import PixScreen


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Terminal Inteligente")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # O gerenciador continua aqui para resolver o problema do tamanho da tela
        self.stacked_widget = QStackedWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.stacked_widget)

        self.welcome = TelaBemVindos(self)
        self.login = LoginScreen(self)
        self.terminal = TerminalScreen(self)
        self.pagamento = PagamentoScreen(self)
        self.teclado = TecladoScreen(self)
        self.app_payment = AppPaymentScreen(self)
        self.pix = PixScreen(self)
        self.confirmacao = ConfirmacaoScreen(self)

        self.stacked_widget.addWidget(self.confirmacao)
        self.stacked_widget.addWidget(self.app_payment)
        self.stacked_widget.addWidget(self.welcome)
        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.teclado)
        self.stacked_widget.addWidget(self.terminal)
        self.stacked_widget.addWidget(self.pagamento)
        self.stacked_widget.addWidget(self.pix)

        self.stacked_widget.setCurrentWidget(self.welcome)

        QTimer.singleShot(100, self.executar_sincronizacao)

    # ====================================================================
    # FUNÇÕES "PONTE" PARA VOCÊ NÃO PRECISAR ALTERAR NENHUMA OUTRA TELA!
    # ====================================================================
    def setCurrentWidget(self, widget):
        """ Recebe o comando antigo das telas e repassa para o stacked_widget """
        self.stacked_widget.setCurrentWidget(widget)

    def currentWidget(self):
        """ Atende a tela do terminal que verifica o widget atual """
        return self.stacked_widget.currentWidget()

    # ====================================================================

    def executar_sincronizacao(self):
        print("Iniciando sincronização de produtos...")
        try:
            SyncService().sincronizar_produtos()
        except Exception as e:
            print(f"Erro na sincronização: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    # Se quiser o cursor do mouse de volta para testar no PC, comente a linha abaixo
    app.setOverrideCursor(Qt.BlankCursor)

    window.showFullScreen()

    sys.exit(app.exec_())
