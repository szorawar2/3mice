import sys
from pystray import MenuItem as item, Icon
from threading import Thread
from PyQt5.QtWidgets import QApplication
from PIL import Image

from pyqt_app import AnymiceLogger, LogEmitter  # Logs for debugging
from web_api import run_api # Flask API functionality

def on_quit(icon, item):
    # Stops the system tray icon and exits the app
    icon.stop()
    sys.exit()
    sys.exit(app.exec_())
    
    
def check_logs(item):
    # Opens logs window
    window.show()
    

def create_tray_icon():
    # Creates a system tray icon with a Quit option
    image = Image.open("mouse_icon.ico")  
    menu = (item('Quit', on_quit), item('Logs', check_logs))
    tray_icon = Icon("Anymice", image, menu=menu)
    tray_icon.run()

if __name__ == "__main__":
    
    # Create signal emitter
    emitter = LogEmitter()

     # Start Flask API in a separate thread
    api_thread = Thread(target=run_api, args=(emitter,), daemon=True)
    api_thread.start()

    # Initialize PyQt app
    app = QApplication(sys.argv)
    window = AnymiceLogger(emitter)  # Pass emitter to UI
    
    def closeEvent(event):
        event.ignore()  # Prevent the window from closing
        window.hide()   # Hide the window instead

    window.closeEvent = closeEvent
    
    # Start System Tray Icon
    create_tray_icon()