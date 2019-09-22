import sys
from PyQt5.QtWidgets import QApplication, QWidgets, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QApplication

class App(QWidgets):

	def __init__(self):
		super().__init__()
		self.title = 'Upload Solution File'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480

		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.openFileNameDialog()
		self.openFileNamesDialog()
		self.saveFileDialog()

		self.show()

	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName,