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

		contest_setup.init_GUI(self)
		contest_setup.client(self)
		return

	def init_GUI(self):

		#Define our top bar
		logo = QLabel(self)
		logo_image = QPixmap('../Elements/bitwise_header.png')
		logo_image2 = logo_image.scaledToWidth(104)
		logo.setPixmap(logo_image2)

		top_bar_layout = QHBoxLayout()
		top_bar_layout.setContentsMargins(15, 5, 20, 0);
		top_bar_layout.addWidget(logo)
		top_bar_layout.setStretch(0, 70)
		

		top_bar_widget = QWidget()
		top_bar_widget.setLayout(top_bar_layout)
		top_bar_widget.setObjectName('top_bar')

		self.top_tab = QTabWidget()
		self.top_tab.setObjectName('top_tab')
		self.client_tab = QWidget()
		self.server_tab = QWidget()
		self.judge_tab = QWidget()
		self.contest_tab = QWidget()

		self.top_tab.addTab(self.client_tab, "Client Config")
		self.top_tab.addTab(self.server_tab, "Server Config")
		self.top_tab.addTab(self.judge_tab, "Judge Config")
		self.top_tab.addTab(self.contest_tab, "Contest Config")


		#Define top_layout = logo_bar + main_layout
		top_layout = QVBoxLayout()
		top_layout.addWidget(top_bar_widget)
		top_layout.addWidget(self.top_tab)
		top_layout.setContentsMargins(1, 0, 1, 1)
		top_layout.setStretch(0, 8)
		top_layout.setStretch(1, 100)

		top_widget = QWidget()
		top_widget.setLayout(top_layout)
		top_widget.setObjectName("main_widget")

		# Set top_widget as our central widget
		self.setCentralWidget(top_widget)
		return

	def client(self):
		self.client_tab_layout = QVBoxLayout()
		self.tabs = QTabWidget()
		self.tabs.setObjectName('client_tabs')
		self.rabbitmq_detail = QWidget()
		self.problem_tab = QWidget()
		self.language = QWidget()
		self.contest = QWidget()

		self.tabs.addTab(self.rabbitmq_detail, "RabbitMQ Creds")
		self.tabs.addTab(self.problem_tab, "Add Problems")
		self.tabs.addTab(self.language, "Add Language")
		self.tabs.addTab(self.contest, "Contest Config")

		self.client_tab_layout.addWidget(self.tabs)
		self.client_tab.setLayout(self.client_tab_layout)
		self.client_tab.setObjectName('client_tab')
		return

	def call_gui(self):
		pass

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
		app.setStyleSheet(open('../Elements/style.qss', "r").read())
		app.setStyle("Fusion")

		client_app = contest_setup()

		app.aboutToQuit.connect(self.closeEvent)

		client_app.showMaximized()

		app.exec_()

setup_window()
