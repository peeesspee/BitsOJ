# Special thanks to www.pythonspot.com for this!
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, pyqtProperty
from ui_widgets import *
import time

class main_window(QWizard):
	def __init__(self, config, parent=None):
		super(main_window, self).__init__(parent)
		self.setStyleSheet(open('Elements/style.qss', "r").read())
		self.setWindowIcon(QIcon('Elements/logo.png'))

		self.config = config
		self.home_page = wizard_page(config, 1)
		self.addPage(self.home_page)
		self.contest_page = wizard_page(config, 2)
		self.addPage(self.contest_page)
		self.rabbitmq_page = wizard_page(config, 3)
		self.addPage(self.rabbitmq_page)
		self.problems_page = wizard_page(config, 4)
		self.addPage(self.problems_page)
		self.languages_page = wizard_page(config, 5)
		self.addPage(self.languages_page)
		self.ranking_page = wizard_page(config, 6)
		self.addPage(self.ranking_page)
		self.all_done_page = wizard_page(config, 7)
		self.addPage(self.all_done_page)
		
		self.setWindowTitle("BitsOJ v1.1 [ CONTEST SETUP ]")
		self.setFixedSize(1366, 768)

		server_username = self.field("Server_Username")
		server_password = self.field("Server_Password")
		client_username = self.field("Client_Username")
		client_password = self.field("Client_Password")
		judge_username = self.field("Judge_Username")
		judge_password = self.field("Judge_Password")
		contest_name = self.field("Contest_Name")
		contest_theme = self.field("Contest_Theme")
		admin_key = self.field("Admin_Key")

			
		
