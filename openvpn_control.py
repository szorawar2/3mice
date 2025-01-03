import subprocess
import os

def start_openvpn():
    try:  
        process = subprocess.Popen([r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe", "--command", "connect", "config"], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("OpenVPN process started.")
        return process
    except Exception as e:
        print(f"{e}")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Failed to start OpenVPN: {e}")
        return None

def stop_openvpn():
    try:
        # Disconnect command for OpenVPN GUI
        subprocess.run([r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe", "--command", "disconnect", "config"])
        # process.terminate()  # Terminate the OpenVPN process
        # process.wait()  # Wait for it to terminate
        print("OpenVPN process stopped.")
    except Exception as e:
        print(f"Failed to stop OpenVPN: {e}")

# openvpn_process = start_openvpn()
# if openvpn_process:
#     print("OpenVPN started successfully.")

# if openvpn_process:
#     stop_openvpn(openvpn_process)
#     print("OpenVPN stopped successfully.")
