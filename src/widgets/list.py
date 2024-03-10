from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QCheckBox, QProgressBar
from .card import *
from PyQt5.QtGui import QPixmap


class CustomList(QWidget):
    def __init__(self,filter,items,videoCards):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.cardCheckState = []
        self.cards = []
        def handleClick(state):
            for card in videoCards:
                checkbox = card["checkbox"]
                if checkbox:
                    checkbox.setChecked(state)
        selectAllBox = filter.widgets[0]
        # attach the click event to the selectAll checkbox
        if selectAllBox and isinstance(selectAllBox,(QCheckBox)):
            selectAllBox.clicked.connect(handleClick)

        # create the cards for each video item
        for i,(imageUrl, title) in enumerate(items):
            self.cardCheckState.append(True) # by default the state is true for each card
            card = VideoInfoCard(imageUrl,title,filter,self,i,videoCards)
            # self.cards.append(card)
            self.layout.addWidget(card)



def handleReply(reply:QNetworkReply,videoThumbnail):
    if reply.error() == QNetworkReply.NoError:
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        scaledPixmap = pixmap.scaled(QSize(100,100))
        videoThumbnail.setPixmap(scaledPixmap)
    else:
        print(f"Error fetching image:",reply.errorString())

def fetchImage(imageUrl,networkManager,videoThumbnail):
    request = QNetworkRequest(QUrl(imageUrl))
    reply = networkManager.get(request)
    if reply:
        reply.finished.connect(lambda:handleReply(reply,videoThumbnail))

class VideoInfoCard(QWidget):
    def __init__(self,imageUrl,title,filter,cList,index,videoCards):
        super().__init__()
        self.index = index
        self.filter = filter
        self.cList = cList
        self.networkManager = QNetworkAccessManager()

        card = QHBoxLayout()
        self.setLayout(card)
        card.setAlignment(Qt.AlignLeft)
        card.setContentsMargins(0,5,0,0)
        self.videoCards = videoCards
        checkbox = QCheckBox()
        checkbox.setObjectName(f"ch_check{index}")
        checkbox.setChecked(True)
        checkbox.clicked.connect(self.__handleCheckBoxClick)
        # id,yt keys are already set
        videoCards[index]["checkState"] = True
        videoCards[index]["checkbox"]=checkbox


        videoTitle = QLabel(title)
        videoThumbnail = QLabel()
        fetchImage(imageUrl,self.networkManager,videoThumbnail)

        card.addWidget(checkbox)
        card.addWidget(videoThumbnail)
        div2 = QVBoxLayout()
        div2.setAlignment(Qt.AlignLeft)
        div2.addWidget(videoTitle)
        # download progress and complete
        progressBar = QProgressBar(self)
        progressBar.setFixedWidth(300)
        progressBar.setFixedHeight(14)
        progressBar.setMinimum(0)
        progressBar.setMaximum(100)
        div2.addWidget(progressBar)
        
        videoCards[index]["progress_bar"]=progressBar
        card.addLayout(div2)
    
    def __isAllBoxChecked(self,box):
        prev = True
        for i in box:
            prev = prev & i
        return prev
    def __handleCheckBoxClick(self,state):
        self.videoCards[self.index]["checkState"]=state
        checkState = [item["checkState"] for item in self.videoCards]
        isAllBoxChecked = self.__isAllBoxChecked(checkState)
        self.filter.selectAll = isAllBoxChecked
        selectAllBox = self.filter.widgets[0]
        selectAllBox.setChecked(isAllBoxChecked)

