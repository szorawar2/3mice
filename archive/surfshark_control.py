import subprocess
import pyautogui

screen_width, screen_height = pyautogui.size()

def open_surfshark():
    try:
        subprocess.Popen(r"C:\Program Files\Surfshark\Surfshark.exe")
    except Exception as e:
        print(f"Error opening Surfshark: {e}")

def connect_surfshark():
    try:
        pyautogui.click((0.9010 * screen_width), (0.8981 * screen_height))
    except Exception as e:
        print(f"Error connecting to Surfshark: {e}")

def disconnect_surfshark():
    try:
        pyautogui.click((0.8645 * screen_width), (0.8981 * screen_height))
    except Exception as e:
        print(f"Error disconnecting from Surfshark: {e}")
