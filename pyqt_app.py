from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt5.QtCore import QObject, pyqtSignal

# Signal emitter for logs
class LogEmitter(QObject):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

# PyQt UI with log display
class AnymiceLogger(QWidget):
    def __init__(self, emitter):
        super().__init__()
        self.emitter = emitter
        self.setup_ui()
        # Connect signal to log display
        self.emitter.log_signal.connect(self.append_log)

    def setup_ui(self):
        self.setWindowTitle("Anymice logs")
        self.setGeometry(100, 100, 1000, 400)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

    def append_log(self, message):
        self.text_edit.append(message)  # Update logs in UI