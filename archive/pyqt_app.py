from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import QTimer, Qt
from archive.youtube_control import open_youtube, play_pause_video, check_window
from archive.surfshark_control import open_surfshark, connect_surfshark, disconnect_surfshark
from archive.openvpn_control import start_openvpn, stop_openvpn
from volume_control import *

class YouTubeControllerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Controller")
        self.setGeometry(100, 100, 300, 200)

        self.open_button = QPushButton("Open YouTube")
        self.open_button.clicked.connect(open_youtube)

        self.play_pause_button = QPushButton("Play/Pause Video")
        self.play_pause_button.clicked.connect(play_pause_video)

        self.open_surfshark_button = QPushButton("Open Surfshark")
        self.open_surfshark_button.clicked.connect(open_surfshark)

        self.connect_surfshark_button = QPushButton("Connect Surfshark")
        self.connect_surfshark_button.clicked.connect(connect_surfshark)

        self.disconnect_surfshark_button = QPushButton("Disconnect Surfshark")
        self.disconnect_surfshark_button.clicked.connect(disconnect_surfshark)

        self.openvpn_start_button = QPushButton("Start OpenVPN")
        self.openvpn_start_button.clicked.connect(start_openvpn)

        self.openvpn_stop_button = QPushButton("Stop OpenVPN")
        self.openvpn_stop_button.clicked.connect(stop_openvpn)

        self.volume_slider = QSlider(self)
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)  # Set range from 0 to 100
        self.volume_slider.setValue(50)  # Set default value
        self.volume_slider.valueChanged.connect(lambda value: set_sys_volume(value))

        self.volume_label = QLabel("Volume", self)

        self.mute_button = QPushButton("Mute", self)
        self.mute_button.clicked.connect(mute_volume)

        self.unmute_button = QPushButton("Unmute", self)
        self.unmute_button.clicked.connect(unmute_volume)

        layout = QVBoxLayout(self)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.open_button)
        layout.addWidget(self.play_pause_button)
        layout.addWidget(self.open_surfshark_button)
        layout.addWidget(self.connect_surfshark_button)
        layout.addWidget(self.disconnect_surfshark_button)
        layout.addWidget(self.openvpn_start_button)
        layout.addWidget(self.openvpn_stop_button)
        layout.addWidget(self.mute_button)
        layout.addWidget(self.unmute_button)


if __name__ == "__main__":
    app = QApplication([])
    window = YouTubeControllerApp()
    window.show()
    app.exec_()
