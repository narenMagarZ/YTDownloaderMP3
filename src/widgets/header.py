from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5 import QtCore

class Header(QVBoxLayout):
    def __init__(self):
        super().__init__()
        h1 = QLabel("Youtube Video Downloader")
        h5 = QLabel("Download youtube videos, convert video to mp3")
        h1.setStyleSheet(f"font-weight:bold;font-size:16px;")
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setContentsMargins(0,5,0,10)
        self.addWidget(h1,alignment=QtCore.Qt.AlignCenter)
        self.addWidget(h5,alignment=QtCore.Qt.AlignCenter)



