from web_api import run_api # Flask API functionality
from pyqt_app import YouTubeControllerApp  # PyQt GUI functionality
import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    # Start Flask API in a separate thread
    api_thread = Thread(target=run_api, daemon=True)
    api_thread.start()

    # Start PyQt app
    app = QApplication(sys.argv)
    window = YouTubeControllerApp()
    window.show()
    sys.exit(app.exec_())
    

    
