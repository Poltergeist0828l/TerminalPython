import redis
import json
from PyQt5.QtCore import QThread, pyqtSignal


class PaymentListener(QThread):
    # O sinal agora é parte estrita da classe QThread
    pagamento_aprovado_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        # É boa prática passar o parent para o QThread
        super().__init__(parent)
        self.redis = redis.Redis(
            host='bore.pub',
            port=64552,
            decode_responses=True
        )
        print(self.redis.ping())
        self.is_running = True

    def run(self):
        """Este método roda na thread secundária."""
        pubsub = self.redis.pubsub()
        pubsub.subscribe("payment_channel")

        # Usamos listen() com um timeout sutil ou checamos get_message
        # para permitir que a thread possa ser encerrada de forma limpa depois, se necessário.
        for message in pubsub.listen():
            if not self.is_running:
                break

            if message["type"] == "message":
                try:
                    data = json.loads(message["data"])
                    # Emite o sinal para a thread principal do PyQt
                    self.pagamento_aprovado_signal.emit(data)
                except json.JSONDecodeError:
                    print("Erro ao decodificar JSON do Redis")

    def stop(self):
        """Método útil para parar a thread quando fechar o app"""
        self.is_running = False
        self.quit()
        self.wait()