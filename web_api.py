from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
# from engineio.async_drivers import gevent
# import gevent
# import eventlet

from volume_control import *
from youtube_control import open_youtube, play_pause_video
from surfshark_control import open_surfshark, connect_surfshark, disconnect_surfshark
from openvpn_control import start_openvpn, stop_openvpn
import threading 
import pyautogui
import socket

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Mobile app
touch_x = None
touch_y = None

# Screen mouse
pointer_x = None
pointer_y = None

@app.route('/3mice_discovery')
def discovery():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname) #Get local IP address
        return jsonify({
            'name': hostname,
            'ip': ip_address
            # Add other device information as needed
        }), 200 #Explicitly send 200 OK status
    except Exception as e:
        print(f"Error during discovery: {e}")
        return jsonify({'error': 'Discovery failed'}), 500 # Return error status

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
        # emit ("response",{"status": "success", "x": new_x, "y": new_y})
    except Exception as e:
        emit ("response",{"error": str(e)}), 500

@socketio.on("mouse_start")
def mouse_start(data):
    global touch_x, touch_y, pointer_x, pointer_y
    try:
        touch_x = data.get("x")
        touch_y = data.get("y")

        pointer_x, pointer_y = pyautogui.position()
        # emit ("response",{"status": "initialized", "touch_x": touch_x, "touch_y": touch_y, 
        #                 "pointer_x": pointer_x, "pointer_y": pointer_y})
    except Exception as e:
        emit ("response",{"error": str(e)}), 500
        

@app.route("/mouse_click", methods=["POST"])
def mouse_click():
    data = request.json
    click = data.get("action")
    
    try :
        if click == "left":
            pyautogui.click(button='left')
        if click == "right":
            pyautogui.click(button='right')
        return jsonify({"message": f"{click} click executed successfully"}), 200
    except Exception as e:
        return jsonify({f"error clicking {click}": str(e)}), 500
    
@app.route("/send_text", methods=["POST"])
def send_text():
    try:
        data = request.json
        text = data.get("key", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        pyautogui.press(text)
        return jsonify({"status": "success", "message": f"Sent text: {text}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/volume", methods=["POST"])
def set_volume():

    action = request.json.get("action")

    import pythoncom
    pythoncom.CoInitialize()

    try:
        if action == "increase":
            increase_volume()
        elif action == "decrease":
            decrease_volume()
        return jsonify({"status": f"Completed Volume {action} action"})
    except Exception as e:
        return jsonify({"error": f"Failed Volume {action} action: {str(e)}"}), 500
    finally:
        pythoncom.CoUninitialize()

@app.route("/youtube", methods=["POST"])
def youtube_control():
    action = request.json.get("action")
    try:
        if action == "open":
            open_youtube()
        elif action == "play_pause":
            play_pause_video()
        return jsonify({"status": f"Completed Youtube {action} action"})
    except Exception as e:
        return jsonify({"error": f"Failed Youtube {action} action: {str(e)}"}), 500

@app.route("/openvpn", methods=["POST"])
def openvpn_control():
    action = request.json.get("action")
    try:    
        if action == "start":
            start_openvpn()
        elif action == "stop":
            stop_openvpn()
        return jsonify({"status": f"Completed OpenVPN {action} action"})
    except Exception as e:
        return jsonify({"error": f"Failed OpenVPN {action} action: {str(e)}"}), 500

@app.route("/surfshark", methods=["POST"])
def control_surfshark():
    action = request.json.get("action")
    try:
        if action == "open":
            open_surfshark()
        elif action == "connect":
            connect_surfshark()
        elif action == "disconnect":
            disconnect_surfshark()
        return jsonify({"status": f"Completed Surfshark {action} action"})   
    except Exception as e:
            return jsonify({"error": f"Failed Surfshark {action} action: {str(e)}"}), 500


def run_api():
    print("Starting Flask server...")
    try:
        socketio.run(app, host="0.0.0.0", port=5125, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error running server: {e}")