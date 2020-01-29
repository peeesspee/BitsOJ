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

		self.selected_languages = {}
		languages = self.config["Languages"]
		allowed_languages = self.config.get("Allowed Languages", ["C"])
		for language in languages:
			if language in allowed_languages:
				self.selected_languages[language] = "TRUE"
			else:
				self.selected_languages[language] = "FALSE"

			self.ranklist_states = {}
		ranklists = self.config.get("Available Ranklists", ["IOI"])
		config_selected_rankist = self.config.get("Selected Ranklist", "IOI")
		for ranklist in ranklists:
			if ranklist == config_selected_rankist:
				self.ranklist_states[ranklist] = "TRUE"
			else:
				self.ranklist_states[ranklist] = "FALSE"

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
		self.setFixedSize(1200, 750)

		self.currentIdChanged.connect(self.page_changed_handler)

		server_username = self.field("Server_Username")
		server_password = self.field("Server_Password")
		client_username = self.field("Client_Username")
		client_password = self.field("Client_Password")
		judge_username = self.field("Judge_Username")
		judge_password = self.field("Judge_Password")
		host = self.field("Host")
		contest_name = self.field("Contest_Name")
		contest_theme = self.field("Contest_Theme")
		admin_key = self.field("Admin_Key")

	def page_changed_handler(self, page):
		if page == -1:
			print('[ SETUP ] Cancelled')
		elif page == 0:
			print('[ SETUP ] Home Page View')
		elif page == 1:
			print('[ SETUP ] Contest Settings View')
		elif page == 2:
			print('[ SETUP ] Contest Settings Over')
			print('[ SETUP ] RabbitMQ Page View')
		elif page == 3:
			print('[ SETUP ] RabbitMQ Settings Over')
			print('[ SETUP ] Problems Page View')
		elif page == 4:
			print('[ SETUP ] Problems Added')
			print('[ SETUP ] Language Page View')
		elif page == 5:
			print('[ SETUP ] Languages selected: ', self.selected_languages)
			print('[ SETUP ] Ranking Page View')
			# WORKING
		elif page == 6:
			# Do final config creation here
			print('[ SETUP ] Finish')
			