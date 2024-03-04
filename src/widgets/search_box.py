from PyQt5.QtWidgets import QLineEdit


class InputBox():
    def __init__(self):
        pass
    
    def __handleTextChange(self,text):
        self.url = text

    def createInputBox(self):
        inputBox = QLineEdit()
        padding = 5
        inputBox.setStyleSheet(f"padding:{padding}px;")
        inputBox.setPlaceholderText("Paste video link here")
        inputBox.textChanged.connect(self.__handleTextChange)
        return inputBox    