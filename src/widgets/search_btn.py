from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from pytube import YouTube
from .list import *


def downloadProgress(stream,chunk,bytes):
    pass


class SearchBtn():
    inputBox = None
    mainLayout = None
    filter = None
    youtube = []
    def __init__(self,inputbox,mainLayout:QVBoxLayout):
        self.inputBox = inputbox
        self.mainLayout = mainLayout
    def getVideoInfo(self,url):
        try:
            yt = YouTube(url)
            self.youtube.append(yt)
            title = yt.title
            thumbnail = yt.thumbnail_url
            print(title,thumbnail)
            return(thumbnail,title)
        except :
            pass

# https://www.youtube.com/watch?v=NoltgGRat2Y, https://www.youtube.com/watch?v=u_zeA_UFRnA
    def handleSearch(self):
        value = self.inputBox.text().strip()
        urls = value.split(",")
        videoInfo = []
        for url in urls:
            url = url.strip()
            if len(url) > 0:
                videoInfo.append(self.getVideoInfo(url))
        videoCatalog = CustomList(self.filter,videoInfo)
        self.mainLayout.addWidget(videoCatalog)
                
    def createSearchBtn(self,inputBox,filter):
        self.filter = filter
        downloadBtn = self.filter.widgets[1]
        def handleDownload():
            for yt in self.youtube:
                stream = yt.streams.filter(progressive=True,resolution="720p").first()
                a = stream.download("/home/naren/Downloads")
                print("stream",stream)
                # stream = yt.streams.filter(progressive=True,resolution="720p").first()
                # downloadedVideo = stream.download(output_path="/home/naren/Downloads")
                # print(f"video downloaded:", downloadedVideo)
            pass
        if downloadBtn:
            downloadBtn.clicked.connect(handleDownload)
        self.inputBox = inputBox
        btn = QPushButton("Search")
        padding = 5
        btn.setStyleSheet(f"padding:{padding}px;")
        btn.clicked.connect(self.handleSearch)
        return btn