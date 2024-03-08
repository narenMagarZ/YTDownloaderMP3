from PyQt5.QtWidgets import QHBoxLayout
from PyQt5 import QtCore
from .download_btn import *
from .select_all import *


class Filter(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.selectAll = True
        self.setObjectName("filter")
        self.setAlignment(QtCore.Qt.AlignLeft)
        selectAll = SelectAll(self)
        downloadBtn = DownloadBtn()
        self.widgets = [selectAll,downloadBtn]
        self.addWidget(selectAll)
        self.addWidget(downloadBtn)
