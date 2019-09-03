import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = ' BitsOJ - Client '
		self.left =800
		self.top = 300
		self.width = 640
		self.height = 480
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		# self.setGeometry(self.left,self.top,self.width,self.height)
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.showMaximized()
	sys.exit(app.exec_())


