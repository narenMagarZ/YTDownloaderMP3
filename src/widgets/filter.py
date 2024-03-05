from PyQt5.QtWidgets import QHBoxLayout
from PyQt5 import QtCore
from .download_btn import *
from .select_all import *


class Filter(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.addWidget(SelectAll())
        self.addWidget(DownloadBtn())

