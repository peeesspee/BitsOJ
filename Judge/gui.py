import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
# from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
# from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
# from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
# from interface_packages.ui_classes import *
# from init_server import initialize_server

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'BitsOJ Judge'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
    
        # Create widget for background
        label = QLabel(self)
        pixmap = QPixmap('./Assets/background.png')
        label.setPixmap(pixmap)
        self.resize(700,600)
        # self.setFixedSize(pixmap.width(),pixmap.height())

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)     
        self.move(qtRectangle.topLeft())


        # Title of login window
        self.title = QLabel("<<BitsOJ>>")

        # Creating input fields
        self.judge_id = QLineEdit(self)
        self.judge_id.setFixedWidth(400)
        self.judge_id.setFixedHeight(50)
        self.judge_id.setPlaceholderText('Judge ID')
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())