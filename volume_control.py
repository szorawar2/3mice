import ctypes
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_volume_controller():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

volume = get_volume_controller()

def set_sys_volume(level):
    try:
        level_int = int(level)
        volume.SetMasterVolumeLevelScalar(level_int / 100, None)  # Level is a percentage (0-100)
        print(f"Volume set to {level}%")
    except Exception as e:
        print(f"Error setting volume: {e}")

def increase_volume():
    current_volume = 100*volume.GetMasterVolumeLevelScalar()
    if current_volume <= 95:
        set_sys_volume(current_volume + 5)
    else: 
        set_sys_volume(100)

def decrease_volume():
    current_volume = 100*volume.GetMasterVolumeLevelScalar()
    if current_volume >= 5:
        set_sys_volume(current_volume - 5)
    else:
        set_sys_volume(0)

def mute_volume():
    try:
        volume.SetMute(1, None)
        print("Volume muted.")
    except Exception as e:
        print(f"Error muting volume: {e}")

def unmute_volume():
    try:
        volume.SetMute(0, None)
        print("Volume unmuted.")
    except Exception as e:
        print(f"Error unmuting volume: {e}")
