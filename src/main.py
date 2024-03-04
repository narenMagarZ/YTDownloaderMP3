from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from widgets.search_box import *
from widgets.download_btn import *
app = QApplication([])
window = QWidget()
window.setWindowTitle("YTdownloaderMP3")

# set window size
windowWidth, windowHeight = 800,800
window.setFixedSize(windowWidth,windowHeight)

screen = app.desktop().screenGeometry()
screenWidth, screenHeight = screen.width(), screen.height()
centerX=(screenWidth - windowWidth) // 2
centerY=(screenHeight - windowHeight) // 2
window.setGeometry(centerX,centerY,windowWidth,windowHeight)
# create a vertical layout
mainLayout = QVBoxLayout()

# create inputbox 



inputBox = InputBox()
searchBox = inputBox.createInputBox()


btn = SearchBtn()
searchBtn = btn.createSearchBtn(searchBox)

hLayout1 = QHBoxLayout()
hLayout1.addWidget(searchBox)
hLayout1.addWidget(searchBtn)
mainLayout.addLayout(hLayout1)


window.setLayout(mainLayout)
window.show()
app.exec_()