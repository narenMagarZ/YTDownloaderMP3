from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from pytube import YouTube
from .list import *
from .helper.generate_folderpath import generateFolderPath
import threading


class SearchBtn():
    inputBox = None
    mainLayout = None
    filter = None
    yts = []
    videoCards = []
    def __init__(self,inputbox,mainLayout:QVBoxLayout):
        self.inputBox = inputbox
        self.mainLayout = mainLayout
    def __downloadProgress(self,stream,chunk,bytesRemaining):
        totalSize = stream.filesize
        bytesDownloaded = totalSize - bytesRemaining
        percentageCompleted = (bytesDownloaded / totalSize ) * 100
        print(f"download progress: {round(percentageCompleted,2)}%")
    def getVideoInfo(self,url):
        try:
            yt = YouTube(url)
            title = yt.title
            thumbnail = yt.thumbnail_url
            return(thumbnail,title)
        except :
            pass

# https://www.youtube.com/watch?v=NoltgGRat2Y, https://www.youtube.com/watch?v=u_zeA_UFRnA
    def handleSearch(self):
        self.videoCards = [] # reset value to empty list
        value = self.inputBox.text().strip()
        urls = value.split(",")
        videoInfo = []
        for i,url in enumerate(urls):
            url = url.strip()
            if len(url) > 0:
                (thumbnail,title) = self.getVideoInfo(url)
                if thumbnail and title:
                    self.videoCards.append({"id":i,"url":url})
                    videoInfo.append((thumbnail,title))
        videoCatalog = CustomList(self.filter,videoInfo,self.videoCards)
        self.mainLayout.addWidget(videoCatalog)
                
    def createSearchBtn(self,inputBox,filter):
        self.filter = filter
        downloadBtn = self.filter.widgets[1]
        def handleDownload():
            print("video cards")
            print(self.videoCards)
            # before starting download check the list of selected file to be downloaded 
            # only selected file are allowed to be download
            # if self.filter.selectAll == True then no need to check for each file to be downloaded
            # just download every file
            # elif self.filter.selectAll == False then only download those file that are checked
            for i,card in enumerate(self.videoCards):
                url = card["url"]
                isChecked = card["checkState"]
                print(url,isChecked)
                if url and isChecked:
                    yt = YouTube(url)
                    createThread(yt)
        if downloadBtn:
            downloadBtn.clicked.connect(handleDownload)
        self.inputBox = inputBox
        btn = QPushButton("Search")
        padding = 5
        btn.setStyleSheet(f"padding:{padding}px;")
        btn.clicked.connect(self.handleSearch)
        return btn


def createThread(yt):
    thread = threading.Thread(target=download,args=[yt])
    thread.start()
    

def download(yt:YouTube):
    stream = yt.streams.filter(progressive=True,resolution="720p").first()
    folderPath = generateFolderPath()
    downloadPath = stream.download(folderPath)
    print("download path",downloadPath)