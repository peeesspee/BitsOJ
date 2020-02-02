# Special thanks to www.pythonspot.com for this!
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
# from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import *
from ui_widgets import *
import time

class main_window(QWizard):
	def __init__(self, config, available_width, available_height, parent=None):
		super(main_window, self).__init__(parent)
		self.setWindowIcon(QIcon('Elements/logo.png'))
		self.config = config
		
		self.available_width = available_width
		self.available_height = available_height

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

		self.problems = self.config.get('Problems', {})
		self.number_of_problems = self.config.get('Number Of Problems', 0)

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
			print('[ SETUP ] Updating configuration files...')
			self.write_changes()
			

	def write_changes(self):
		# RabbitMQ Page Data
		self.config['Server Username'] = self.field("Server_Username")
		self.config['Server Password'] = self.field("Server_Password")
		self.config['Client Username'] = self.field("Client_Username")
		self.config['Client Password'] = self.field("Client_Password")
		self.config['Judge Username'] = self.field("Judge_Username")
		self.config['Judge Password'] = self.field("Judge_Password")
		self.config['Host'] = self.field("Host")
		# Contest settings Page Data
		self.config['Contest Name'] = self.field("Contest_Name")
		self.config['Contest Theme'] = self.field("Contest_Theme")
		self.config['Admin Key'] = self.field("Admin_Key")
		# Problems Page Data
		self.config['Problems'] = self.problems
		self.config['Number Of Problems'] = len(self.problems)
		# Languages Page Data
		allowed_languages = []
		for language in self.config["Languages"]:
			if self.selected_languages[language] == "TRUE":
				allowed_languages.append(language)
		self.config['Allowed Languages'] = allowed_languages
		# Ranklist Page Data
		for ranklist in self.config["Ranking Styles"]:
			if self.ranklist_states[ranklist] == "TRUE":
				self.config['Selected Ranklist'] = ranklist
				break
		problem_max_score = self.field("Problem_Score")
		penalty_score = self.field("Penalty_Score")
		penalty_time = self.field("Penalty_Time")
		self.config['Problem Max Score'] = int(problem_max_score)
		self.config['Penalty Score'] = int(penalty_score)
		self.config['Penalty Time'] = int(penalty_time)

		try:
			content = json.dumps(self.config, indent = 4)
			with open('config2.json', 'w') as file:
				file.write(content)
		except Exception as error:
			print('[ ERROR ] File could not be written: ', error)