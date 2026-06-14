import requests
import time
from PyQt5.QtCore import QThread, pyqtSignal


class InternetMonitor(QThread):
    status_changed = pyqtSignal(bool)

    def __init__(self, interval=3):
        super().__init__()
        self.interval = interval
        self.running = True
        self.status = None

    def check_internet(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except:
            return False

    def run(self):
        while self.running:
            new_status = self.check_internet()

            if new_status != self.status:
                self.status = new_status
                self.status_changed.emit(self.status)

            time.sleep(self.interval)

    def stop(self):
        self.running = False