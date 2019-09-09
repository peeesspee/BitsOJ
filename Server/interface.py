import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSlot

global current_status 
current_status = "STOPPED"

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'BitsOJ v1.0.1 [ SERVER ]'
		self.setWindowIcon(QIcon('Elements/icon1.png'))
		self.setWindowTitle(self.title)
		self.showMaximized()
		self.status = self.statusBar()
		self.show()
		App.main_window(self)
		return
	

	def main_window(self):
		self.status.showMessage(App.get_status())
		return

	def get_status():
		global current_status
		return current_status

class init_gui(App):
	def __init__(self):
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('Elements/style.qss', "r").read())

		ex = App()
		
		sys.exit(app.exec_())
