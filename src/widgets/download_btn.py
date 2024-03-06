from PyQt5.QtWidgets import QPushButton



class DownloadBtn(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Download")