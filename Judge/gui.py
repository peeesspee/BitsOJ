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
        try:
            self.title = 'BitsOJ Judge'
            self.setWindowTitle(self.title)
            self.resize(700,600)
            self.setWindowIcon(QIcon('./Assets/logo.png'))

            # Frame Geometry
            qtRectangle = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            qtRectangle.moveCenter(centerPoint)     
            self.move(qtRectangle.topLeft())


            # Title of login window
            self.title = QLabel("<<BitsOJ>>")
            self.title.setObjectName('header')
            self.title.setFixedWidth(400)
            self.title.setFixedHeight(150)


            # Creating input fields

            # Username field
            self.judge_id = QLineEdit(self)
            self.judge_id.setFixedWidth(400)
            self.judge_id.setFixedHeight(50)
            self.judge_id.setPlaceholderText('Judge ID')

            # Password field
            self.password = QLineEdit(self)
            self.password.setFixedWidth(400)
            self.password.setFixedHeight(50)
            self.password.setPlaceholderText('Password')
            self.password.setEchoMode(QLineEdit.Password)

            # Button to login
            self.login_button = QPushButton('Login', self)
            self.login_button.setFixedWidth(300)
            self.login_button.setFixedHeight(80)
            self.login_button.clicked.connect(lambda : self.onClick)
            self.login_button.setDefault(True)
            self.login_button.setObjectName('login')

            # Creating  Vertical layout 
            layout = QVBoxLayout(self)

            # Adding widget to Layout
            layout.addWidget(self.title)
            layout.addWidget(self.judge_id)
            layout.addWidget(self.password)
            layout.addWidget(self.login_button)

            layout.setContentsMargins(100, 0, 0, 150)


            self.setLayout(layout)
            self.setObjectName('loginwindow')
            self.show()

        except Exception as e:
            print(e)
        return 

    def onClick(self):
        print("button clicked")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('Assets/login.qss', "r").read())
    ex = App()
    ex.show()
    sys.exit(app.exec_())