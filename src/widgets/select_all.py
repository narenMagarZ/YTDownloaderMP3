from PyQt5.QtWidgets import QCheckBox



class SelectAll(QCheckBox):
    def __init__(self,filter):
        super().__init__()
        self.setText("Select All")
        self.setObjectName("select-all")
        self.setChecked(filter.selectAll)


