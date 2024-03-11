from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from pytube import YouTube
from .list import *
from .helper.generate_folderpath import generateFolderPath
import threading
import os

class Helper():
    def __init__(self,url,index,p):
        self.url = url
        self.index = index
        self.p = p
    def downloadProgress(self,stream,chunk,bytesRemaining):
        totalSize = stream.filesize
        bytesDownloaded = totalSize - bytesRemaining
        percentageCompleted = (bytesDownloaded / totalSize ) * 100
        approximatePercentage = round(percentageCompleted)
        progressBar = self.p.videoCards[self.index]["progress_bar"]
        progressBar.setValue(approximatePercentage)
        progressBar.update()
    def downloadComplete(self,x,y):
        progressBar = self.p.videoCards[self.index]["progress_bar"]
        progressBar.setValue(100)
        progressBar.update()
        pass
class SearchBtn():
    inputBox = None
    mainLayout = None
    filter = None
    yts = []
    videoCards = []
    catalog = None
    def __init__(self,inputbox,mainLayout:QVBoxLayout):
        self.inputBox = inputbox
        self.mainLayout = mainLayout

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
        # remove the list items
        if self.catalog:
            self.mainLayout.removeWidget(self.catalog)
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
        self.catalog = CustomList(self.filter,videoInfo,self.videoCards)
        self.mainLayout.addWidget(self.catalog)
                
    def createSearchBtn(self,inputBox,filter):
        self.filter = filter
        downloadBtn = self.filter.widgets[1]
        def handleDownload():
            # todo :
            # if downloaded files are already existed no need to download

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
                    helper = Helper(url,i,self)
                    yt = YouTube(helper.url,on_progress_callback=helper.downloadProgress,on_complete_callback=helper.downloadComplete)
                    createThread(yt,self.videoCards[i])
        if downloadBtn:
            downloadBtn.clicked.connect(handleDownload)
        self.inputBox = inputBox
        btn = QPushButton("Search")
        padding = 5
        btn.setStyleSheet(f"padding:{padding}px;")
        btn.clicked.connect(self.handleSearch)
        return btn


def createThread(yt,videoCard):
    thread = threading.Thread(target=download,args=[yt,videoCard])
    thread.start()
    

def download(yt:YouTube,videCard):
    folderPath = generateFolderPath()
    stream = yt.streams.filter(progressive=True,resolution="720p").first()
    path = stream.download(folderPath)
    videCard["path"]=path




# https://www.youtube.com/watch?v=sDp_ulTyDTY, https://www.youtube.com/watch?v=vnHTrxV7TMc, https://www.youtube.com/watch?v=OSYFhv3q6xo, https://www.youtube.com/watch?v=WmLXSosljUk