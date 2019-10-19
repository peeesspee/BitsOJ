import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler




class contest_setup(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowIcon(QIcon('Elements/logo.png'))
		self.setWindowTitle('BitsOJ v1.0.1 Contest Setup')
		self.resize(1200,700)


	def closeEvent(self, event):
		message = "Pressing 'Yes' will SHUT the Client.\nAre you sure you want to exit?"
		detail_message = "Any active contest might end prematurely. "

		custom_close_box = QMessageBox()
		custom_close_box.setIcon(QMessageBox.Critical)
		custom_close_box.setWindowTitle('Warning!')
		custom_close_box.setText(message)
		custom_close_box.setInformativeText(detail_message)


		custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		custom_close_box.setDefaultButton(QMessageBox.No)

		button_yes = custom_close_box.button(QMessageBox.Yes)
		button_yes.setText('Yes')
		button_no = custom_close_box.button(QMessageBox.No)
		button_no.setText('No')

		button_yes.setObjectName("close_button_yes")
		button_no.setObjectName("close_button_no")

		# button_yes.setStyleSheet(open('Elements/style.qss', "r").read())
		# button_no.setStyleSheet(open('Elements/style.qss', "r").read())

		custom_close_box.exec_()

		if custom_close_box.clickedButton() == button_yes:
			event.accept()
		elif custom_close_box.clickedButton() == button_no:
			event.ignore()



class setup_window(contest_setup):
	def __init__(self):
		app = QApplication(sys.argv)
		app.setStyle("Fusion")

		client_app = contest_setup()

		app.aboutToQuit.connect(self.closeEvent)

		client_app.showMaximized()

		app.exec_()

setup_window()