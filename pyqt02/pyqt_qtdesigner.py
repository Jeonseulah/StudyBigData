
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#class oop 
class qTemplate(QWidget):
    # 생성자 
    def __init__(self)->None:
        super().__init__()
        uic.loadUi('./pyqt02/basic01.ui', self)
        self.initUI()

    def initUI(self)-> None:
        self.addControls()
        self.show()
    
    def addControls(self) -> None:
        self.btn1.clicked.connect(self.btn1_clicked)

    # event = signal (python)
    def btn1_clicked(self):
        # QMessageBox.information(self, 'signal', 'self.btn1_clicked') # 일반정보창
        # QMessageBox.warning(self, 'signal', 'self.btn1_clicked') # 경고창
        self.label.setText('메시지: btn1 버튼 클릭!!!')
        QMessageBox.critical(self, 'signal', 'self.btn1_clicked') # 에러창 


if __name__ == '__main__':
    app=QApplication(sys.argv)
    ins=qTemplate()
    app.exec_()
