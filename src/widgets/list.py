from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QCheckBox
from .card import *
from PyQt5.QtGui import QPixmap



def handleResponse(response:QNetworkReply,thumbnail:QLabel):
    if response.error() == QNetworkReply.NoError:
        data = response.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        scaledPixmap = pixmap.scaled(QSize(100,100),Qt.KeepAspectRatio)
        thumbnail.setPixmap(scaledPixmap)
    else:
        # handle network errors
        print(f"Error fetching image:",response.errorString())

class CustomList(QWidget):
    def __init__(self,items):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.networkManager = QNetworkAccessManager()
        for imageUrl, title in items:
            card = QHBoxLayout()
            card.setAlignment(Qt.AlignLeft)
            card.setContentsMargins(0,5,0,0)
            videoTitle = QLabel(title)
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            thumbnail = QLabel()
            request = QNetworkRequest(QUrl(imageUrl))
            response = self.networkManager.get(request)
            response.finished.connect(lambda:handleResponse(response,thumbnail))
            card.addWidget(checkbox)
            card.addWidget(thumbnail)
            card.addWidget(videoTitle)
            self.layout.addLayout(card)



def handleReply(reply:QNetworkReply):
    try:
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        scaledPixmap = pixmap.scaled(QSize(100,100,Qt.keepAspectRatio))
        
        return data
    except Exception as e:
        print(f"Error fetching image:",e)

def fetchImage(imageUrl,networkManager):
    request = QNetworkRequest(QUrl(imageUrl))
    reply = networkManager.get(request)
    reply.finished.connect(lambda:handleResponse(reply))

class VideoInfoCard(QVBoxLayout):
    def __init__(self,imageUrl,title):
        self.networkManager = QNetworkAccessManager()
        card = QVBoxLayout()
        card.setAlignment(Qt.AlignLeft)
        card.setContentsMargins(0,5,0,0)

        div1 = QHBoxLayout()
        checkbox = QCheckBox()
        checkbox.setChecked(True)
        title = QLabel(title)
        thumbnail = QLabel()
        fetchImage(imageUrl,self.networkManager)

        div2 = QHBoxLayout()
        


        card.addLayout(div1)
        card.addLayout(div2)
        pass

