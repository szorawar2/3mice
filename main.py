import sys
import os
from pystray import MenuItem as item, Icon
from threading import Thread
from PyQt5.QtWidgets import QApplication
from PIL import Image

from pyqt_app import AnymiceLogger, LogEmitter  # Logs for debugging
from web_api import run_api # Flask API functionality

def on_quit(icon, item):
    # Stops the system tray icon and exits the app
    icon.stop()
    os._exit(0)  # Force exit
    
def check_logs(item):
    # Opens logs window
    window.show()

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_tray_icon():
    # Load tray icon with proper path handling
    icon_path = get_resource_path('mouse_icon.ico')
    
    try:
        image = Image.open(icon_path)
    except Exception as e:
        print(f"Error loading icon: {e}")
        # Create blank fallback image
        image = Image.new('RGB', (64, 64), (255, 255, 255))
    
    menu = (item('Quit', on_quit), item('Logs', check_logs))
    tray_icon = Icon("Anymice", image, menu=menu)
    tray_icon.run()
    

if __name__ == "__main__":
    
    # Create signal emitter
    emitter = LogEmitter()
    
    # Initialize PyQt app
    app = QApplication(sys.argv)
    window = AnymiceLogger(emitter)  # Pass emitter to UI

     # Start Flask API in a separate thread
    api_thread = Thread(target=run_api, args=(emitter,), daemon=True)
    api_thread.start()

    def closeEvent(event):
        event.ignore()  # Prevent the window from closing
        window.hide()   # Hide the window instead

    window.closeEvent = closeEvent
    
    window.show()
    
    # Start System Tray Icon
    create_tray_icon()