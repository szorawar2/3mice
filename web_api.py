import sys
import os
from pathlib import Path 
from flask import Flask, request, jsonify, Response, send_from_directory, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pythoncom
import threading 
import pyautogui
import socket
import engineio.async_drivers.threading
import logging
from gevent.pywsgi import WSGIServer

from volume_control import *

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    print(f"base path: {base_path}")
    return os.path.join(base_path, relative_path)

app = Flask(
    __name__,
    static_folder=resource_path('react/static'),
    template_folder=resource_path('react')
)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


"""
  - Serve React files
  
"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and (app.static_folder and 
                 (Path(app.static_folder) / path).exists()):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.template_folder, 'index.html')



"""
  - Log Handling
  
"""

# Configure logging to use PyQt signals
def configure_logging(emitter):
    class QtLogHandler(logging.Handler):
        def __init__(self, emitter):
            super().__init__()
            self.emitter = emitter

        def emit(self, record):
            msg = self.format(record)
            self.emitter.log_signal.emit(msg)  # Emit to PyQt

    handler = QtLogHandler(emitter)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    
    # Attach handler to Flask and Werkzeug loggers
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.addHandler(handler)
    werkzeug_logger.setLevel(logging.INFO)
  
# Logs on both pyqt app and terminal for debugging    
main_log = app.logger.info



"""
  - Mouse Actions

"""

# Mobile screen
touch_x = None
touch_y = None

# Screen mouse
pointer_x = None
pointer_y = None

@socketio.on("mouse_move")
def control_mouse(data):
    global pointer_x, pointer_y, touch_x, touch_y
    try:
        x = data.get("x")
        y = data.get("y")
        new_x = pointer_x + 1.8*(x - touch_x)
        new_y = pointer_y + 1.8*(y - touch_y)
        pyautogui.moveTo(new_x, new_y)
        pointer_x, pointer_y = new_x, new_y 
        touch_x, touch_y = x, y
        
    except Exception as e:
        main_log(f"failed to move to position {new_x} | {new_y} , error: {e}")
        emit ("response",{"error": str(e)}), 500

@socketio.on("mouse_start")
def mouse_start(data):
    global touch_x, touch_y, pointer_x, pointer_y
    try:
        touch_x = data.get("x")
        touch_y = data.get("y")

        pointer_x, pointer_y = pyautogui.position()
        main_log("mouse touch initiated")

    except Exception as e:
        main_log(f"failed to initiate mouse touch, error: {e}")
        emit ("response",{"error": str(e)}), 500
        

@app.route("/api/mouse_click", methods=["POST"])
def mouse_click():
    data = request.json
    click = data.get("action")
    
    try :
        if click == "left":
            pyautogui.click(button='left')
        if click == "right":
            pyautogui.click(button='right')
            
        main_log(f"{click} click executed")
        return Response(status=200)
    
    except Exception as e:
        main_log(f"{click} click failed to execute, error: {e}")
        return jsonify({f"error clicking {click}": str(e)}), 500



"""
 -  Send Text 

"""

@app.route("/api/send_text", methods=["POST"])
def send_text():
    try:
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        if text == "backspace":
            pyautogui.press(text)
        else:
            pyautogui.write(text)
            
        main_log("text added or removed")
        return Response(status=200)
    
    except Exception as e:
        main_log(f"failed to send text, error: {e}")
        return jsonify({"error": str(e)}), 500
    
    
"""
 -  Volume Control

"""

@app.route("/api/volume", methods=["POST"])
def set_volume():

    action = request.json.get("action")
    pythoncom.CoInitialize()

    try:
        if action == "increase":
            increase_volume(main_log)
        elif action == "decrease":
            decrease_volume(main_log)            
                
        return Response(status=200)
    
    except Exception as e:
        main_log(f"volume {action} action failed, error: {e}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        pythoncom.CoUninitialize()


def run_api(emitter):
    configure_logging(emitter)
    try:
        socketio.run(app, host="0.0.0.0", port=5125, debug=False, use_reloader=False, allow_unsafe_werkzeug=True) 
        #allow_unsafe_werkzeug for production server
        
        main_log("Successfully started Flask server...")
    except Exception as e:
        main_log(f"Error running server: {e}")

