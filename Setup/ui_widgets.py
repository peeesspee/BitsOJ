from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import *
import socket

# This class creates pages for the setup wizard, based on the page id given to it.
class wizard_page(QWizardPage):
	def __init__(self, config, page_id = 1, parent=None):
		super(wizard_page, self).__init__(parent)
		self.config = config
		self.top_bar = QWidget()
		self.top_bar_layout = QHBoxLayout(self.top_bar)
		self.logo = QLabel()
		self.logo.setPixmap(QPixmap('Elements/bitwise_header.png').scaledToWidth(104))
		self.top_bar_layout.addWidget(self.logo)
		
		# Based on page_id, return the corresponding widget
		if page_id == 1:
			self.main_widget = self.home_page()
		elif page_id == 2:
			self.main_widget = self.contest_page()
		elif page_id == 3:
			self.main_widget = self.rabbitmq_page()
		elif page_id == 4:
			self.main_widget = self.problems_page()
		elif page_id == 5:
			self.main_widget = self.languages_page()
		elif page_id == 6:
			self.main_widget = self.ranking_page()
		elif page_id == 7:
			self.main_widget = self.all_done_page()

		self.top_layout = QVBoxLayout()
		self.top_layout.addWidget(self.top_bar)
		self.top_layout.addWidget(self.main_widget)
		self.top_layout.setStretch(0, 10)
		self.top_layout.setStretch(1, 90)
		self.setLayout(self.top_layout)

	def get_horizontal_widget(self, widget_1, widget_2):
		layout = QHBoxLayout()
		layout.addWidget(widget_1)
		layout.addWidget(widget_2)
		layout.addStretch(1)
		widget = QWidget()
		widget.setLayout(layout)
		return widget

	def home_page(self):
		self.title_label = QLabel('Home')
		self.title_label.setObjectName('main_screen_heading')
		self.welcome_label = QLabel('Welcome to BitsOJ!')
		self.welcome_label.setObjectName('main_screen_sub_heading')
		message = (
			"This utility will help you to generate configuration " +
			"files for the Client, Server, and the Judge,\nabsolutely hassle free." +
			"Many of the details will remain same if you are using the same setup to\nhost " +
			"multiple contests ( Recommended! ).\nAll the Best for your contest, and many more to come!\n" + 
			" \t\t\t\t\t\t\t- Team Bitwise @ JUET, Guna"
		)
		self.message_label = QLabel(message)
		self.message_label.setObjectName('main_screen_content')
		self.bottom_label = QLabel(
			"BitsOJ is an Open Source project, and we would love to have your contributions!"
		)
		self.bottom_label.setObjectName('main_screen_content')
		self.contribute_label = QLabel("Contribute here: ")
		self.contribute_label.setObjectName('main_screen_sub_heading2')
		self.contribute_content = QLabel(
			"<a href='https://github.com/peeesspee/BitsOJ' style = 'color: #23B2EE;'>github.com/peeesspee/BitsOJ</a>"
		)
		self.contribute_content.setObjectName('main_screen_content')
		self.contribute_content.setToolTip(
			'Opens github repository link in web browser.'
		)
		self.contribute_content.setTextInteractionFlags(Qt.TextBrowserInteraction)
		self.contribute_content.setOpenExternalLinks(True)
		self.contribute_widget = self.get_horizontal_widget(self.contribute_label, self.contribute_content)
		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.welcome_label)
		self.main_layout.addWidget(self.message_label)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.bottom_label)
		self.main_layout.addWidget(self.contribute_widget)
		return self.main_widget

	def contest_page(self):
		self.title_label = QLabel('Contest Settings')
		self.title_label.setObjectName('main_screen_heading')

		message = (
			"Admin Key should be remembered to do critical contest tasks."
		)
		self.message_contest_page = QLabel(message)
		self.message_contest_page.setObjectName('main_screen_content')

		self.sub_head_1 = QLabel('Contest Decoration')
		self.sub_head_1.setObjectName('main_screen_sub_heading')

		self.contest_name_label = QLabel('&Contest Name:   ')
		self.contest_name_label.setObjectName('main_screen_content')
		self.contest_name_entry = QLineEdit()
		self.contest_name_entry.setToolTip('Contest title')
		self.contest_name_entry.setPlaceholderText('Example: Kodeathon')
		self.contest_name_entry.setText(self.config.get("Contest Name", "Kodeathon"))
		# Register this entry as a global value, which can be accessed by the main class
		self.registerField("Contest_Name", self.contest_name_entry)
		self.contest_name_label.setBuddy(self.contest_name_entry)
		self.contest_name_widget = self.get_horizontal_widget(
			self.contest_name_label,
			self.contest_name_entry
		)

		self.contest_theme_label = QLabel('&Contest Theme: ')
		self.contest_theme_label.setObjectName('main_screen_content')
		self.contest_theme_entry = QLineEdit()
		self.contest_theme_entry.setToolTip('Contest Theme')
		self.contest_theme_entry.setPlaceholderText('Example: Harry Potter')
		self.contest_theme_entry.setText(self.config.get("Contest Theme", " "))
		# Register this entry as a global value, which can be accessed by the main class
		self.registerField("Contest_Theme", self.contest_theme_entry)
		self.contest_theme_label.setBuddy(self.contest_theme_entry)
		self.contest_theme_widget = self.get_horizontal_widget(
			self.contest_theme_label,
			self.contest_theme_entry
		)

		self.sub_head_2 = QLabel('Contest Security')
		self.sub_head_2.setObjectName('main_screen_sub_heading')

		self.admin_key_label = QLabel('&Administrator Password: ')
		self.admin_key_label.setObjectName('main_screen_content')
		self.admin_key_entry = QLineEdit()
		self.admin_key_entry.setEchoMode(QLineEdit.Password)
		self.admin_key_entry.setToolTip('This password will be used to do critical tasks on the Server.')
		self.admin_key_entry.setPlaceholderText('Remember this!')
		self.admin_key_entry.setText(self.config.get("Admin Key", ""))
		# Register this entry as a global value, which can be accessed by the main class
		self.registerField("Admin_Key", self.admin_key_entry)
		self.admin_key_label.setBuddy(self.admin_key_entry)
		self.admin_key_widget = self.get_horizontal_widget(
			self.admin_key_label,
			self.admin_key_entry
		)
		
		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.message_contest_page)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.sub_head_1)
		self.main_layout.addWidget(self.contest_name_widget)
		self.main_layout.addWidget(self.contest_theme_widget)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.sub_head_2)
		self.main_layout.addWidget(self.admin_key_widget)
		self.main_layout.addStretch(1)
		self.main_layout.addStretch(1)
		return self.main_widget

	def rabbitmq_page(self):
		self.title_label = QLabel('RabbitMQ Connections')
		self.title_label.setObjectName('main_screen_heading')

		self.message_rabbitmq = QLabel(
			'Fill in the account details of Server, Client and Judge, which were ' +
			'created in the RabbitMQ\nManagement Portal: '
		)
		self.message_rabbitmq.setObjectName('main_screen_content')

		self.server_label = QLabel('Server')
		self.server_label.setObjectName('main_screen_sub_heading')
		self.server_username_label = QLabel('&Username: ')
		self.server_username_label.setObjectName('main_screen_content')
		self.server_username_entry = QLineEdit()
		self.server_username_entry.setToolTip('RabbitMQ Server account username')
		self.server_username_entry.setPlaceholderText('Example: BitsOJ')
		self.server_username_entry.setText(self.config.get("Server Username", ""))
		# Register this entry as a global value
		self.registerField("Server_Username", self.server_username_entry)
		self.server_username_label.setBuddy(self.server_username_entry)
		self.server_username_widget = self.get_horizontal_widget(
			self.server_username_label,
			self.server_username_entry
		)
		self.server_password_label = QLabel('&Password:  ')
		self.server_password_label.setObjectName('main_screen_content')
		self.server_password_entry = QLineEdit()
		self.server_password_entry.setEchoMode(QLineEdit.Password)
		self.server_password_entry.setToolTip('RabbitMQ Server account password')
		self.server_password_entry.setText(self.config.get("Server Password", ""))
		self.registerField("Server_Password", self.server_password_entry)
		self.server_password_label.setBuddy(self.server_password_entry)
		self.server_password_widget = self.get_horizontal_widget(
			self.server_password_label,
			self.server_password_entry
		)
		self.server_creds_widget = self.get_horizontal_widget(
			self.server_username_widget,
			self.server_password_widget
		)

		self.client_label = QLabel('Client')
		self.client_label.setObjectName('main_screen_sub_heading')
		self.client_username_label = QLabel('&Username: ')
		self.client_username_label.setObjectName('main_screen_content')
		self.client_username_entry = QLineEdit()
		self.client_username_entry.setToolTip('RabbitMQ Client account username')
		self.client_username_entry.setPlaceholderText('Example: Client')
		self.client_username_entry.setText(self.config.get("Client Username", ""))
		self.registerField("Client_Username", self.client_username_entry)
		self.client_username_label.setBuddy(self.client_username_entry)
		self.client_username_widget = self.get_horizontal_widget(
			self.client_username_label,
			self.client_username_entry
		)
		self.client_password_label = QLabel('&Password:  ')
		self.client_password_label.setObjectName('main_screen_content')
		self.client_password_entry = QLineEdit()
		self.client_password_entry.setEchoMode(QLineEdit.Password)
		self.client_password_entry.setToolTip('RabbitMQ Client account password')
		self.client_password_entry.setText(self.config.get("Client Password", ""))
		self.registerField("Client_Password", self.client_password_entry)
		self.client_password_label.setBuddy(self.client_password_entry)
		self.client_password_widget = self.get_horizontal_widget(
			self.client_password_label,
			self.client_password_entry
		)
		self.client_creds_widget = self.get_horizontal_widget(
			self.client_username_widget,
			self.client_password_widget
		)

		self.judge_label = QLabel('Judge')
		self.judge_label.setObjectName('main_screen_sub_heading')
		self.judge_username_label = QLabel('&Username: ')
		self.judge_username_label.setObjectName('main_screen_content')
		self.judge_username_entry = QLineEdit()
		self.judge_username_entry.setToolTip('RabbitMQ Judge account username')
		self.judge_username_entry.setPlaceholderText('Example: Client')
		self.judge_username_entry.setText(self.config.get("Judge Username", ""))
		self.registerField("Judge_Username", self.judge_username_entry)
		self.judge_username_label.setBuddy(self.judge_username_entry)
		self.judge_username_widget = self.get_horizontal_widget(
			self.judge_username_label,
			self.judge_username_entry
		)
		self.judge_password_label = QLabel('&Password:  ')
		self.judge_password_label.setObjectName('main_screen_content')
		self.judge_password_entry = QLineEdit()
		self.judge_password_entry.setEchoMode(QLineEdit.Password)
		self.judge_password_entry.setToolTip('RabbitMQ Judge account password')
		self.judge_password_entry.setText(self.config.get("Judge Password", ""))
		self.registerField("Judge_Password", self.judge_password_entry)
		self.judge_password_label.setBuddy(self.judge_password_entry)
		self.judge_password_widget = self.get_horizontal_widget(
			self.judge_password_label,
			self.judge_password_entry
		)
		self.judge_creds_widget = self.get_horizontal_widget(
			self.judge_username_widget,
			self.judge_password_widget
		)

		self.host_label = QLabel('Host:  ')
		self.host_label.setObjectName('main_screen_sub_heading')

		self.host_entry = QLineEdit()
		self.host_entry.setToolTip('RabbitMQ Host IP Address')
		self.host_entry.setText(self.config.get("Host", "localhost"))
		self.registerField("Host", self.host_entry)
		self.automatic_switch = QCheckBox('This PC')
		self.automatic_switch.stateChanged.connect(self.ip_switch_change)
		self.host_widget = self.get_horizontal_widget(
			self.host_entry,
			self.automatic_switch
		)
		
		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.message_rabbitmq)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.server_label)
		self.main_layout.addWidget(self.server_creds_widget)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.client_label)
		self.main_layout.addWidget(self.client_creds_widget)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.judge_label)
		self.main_layout.addWidget(self.judge_creds_widget)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.host_label)
		self.main_layout.addWidget(self.host_widget)
		self.main_layout.addStretch(1)
		return self.main_widget

	def ip_switch_change(self, state):
		if state == Qt.Checked:
			print('[ SETUP ] Fetch IP')
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))
			ip = s.getsockname()[0]
			s.close()
			self.host_entry.setText(ip)
		else:
			self.host_entry.setText('localhost')

	def problems_page(self):
		self.title_label = QLabel('Problems')
		self.title_label.setObjectName('main_screen_heading')
		
		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
	
		self.main_layout.addStretch(1)
		return self.main_widget

	def languages_page(self):
		self.title_label = QLabel('Languages')
		self.title_label.setObjectName('main_screen_heading')

		self.message_languages = QLabel(
			'Set the allowed languages in the contest.' + 
			'\nPlease check if you have a compiler available for the language you select.'
		)
		self.message_languages.setObjectName('main_screen_content')

		# All the languages that are in the Judge
		self.languages = self.config.get("Languages", ["TEXT"])
		self.number_of_languages = len(self.languages)
		# All the languages that were selected earlier, read from the config file
		# Assuming this is a restart of setup, else this list is empty by default
		self.allowed_languages = self.config.get("Allowed Languages", ["TEXT"])
		# This list holds all the checkbox widgets generated ahead
		self.language_widgets_list = []
		# This widget holds all the checkboxes for the view
		self.language_widget = QWidget()
		self.language_layout = QVBoxLayout(self.language_widget)
		# Mapper for checkbox signals, Read the clarification ahead
		self.list_signal_mapper = QSignalMapper()
		for i in range(0, self.number_of_languages):
			language_checkbox = QCheckBox(self.languages[i])
			self.language_widgets_list.append(language_checkbox)
			if self.languages[i] in self.allowed_languages:
				self.language_widgets_list[i].setChecked(True)
			else:
				self.language_widgets_list[i].setChecked(False)
			self.language_layout.addWidget(self.language_widgets_list[i])
		# Map each indexed widget to a mapper function which can handle state changes based on index
		# WRONG : widget_list[i].stateChanged.connect(function) : This only selects the last widget in the list
		# CORRECT : widget_list[] -----> mapper[] ----> function
		for language_widget in self.language_widgets_list:
			self.list_signal_mapper.setMapping(
				language_widget, 
				self.language_widgets_list.index(
					language_widget
				)
			)
			language_widget.stateChanged.connect(self.list_signal_mapper.map)
		# Now the signal mapper connects the checkbox to appropiae function call
		self.list_signal_mapper.mapped[int].connect(
			self.language_checkbox_state_change_handler
		)
		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.message_languages)
		self.main_layout.addWidget(self.language_widget)
		self.main_layout.addStretch(1)
		return self.main_widget

	def language_checkbox_state_change_handler(self, index):
		widget = self.language_widgets_list[index]
		state = widget.checkState()
		if state == Qt.Checked:
			print("[ SETUP ] Language " + self.languages[index], " : Allowed")
			self.wizard().selected_languages[self.languages[index]] = "TRUE"
		else:
			print("[ SETUP ] Language " + self.languages[index], " : Not Allowed")
			self.wizard().selected_languages[self.languages[index]] = "FALSE"

	def ranking_page(self):
		self.title_label = QLabel('Ranking')
		self.title_label.setObjectName('main_screen_heading')

		self.message_ranklist = QLabel(
			'Set the Ranking style in the contest.'
		)
		self.message_ranklist.setObjectName('main_screen_content')

		self.rbutton_signal_mapper = QSignalMapper()
		self.ranklist_rbutton_list = []
		
		self.available_ranklists = self.config.get("Ranking Styles")
		self.selected_ranklist = self.config.get("Selected Ranklist")

		self.ranklist_widget = QWidget()
		self.ranklist_layout  = QVBoxLayout(self.ranklist_widget)

		for ranklist in self.available_ranklists:
			ranklist_radiobutton = QRadioButton(ranklist)
			if ranklist == self.selected_ranklist:
				ranklist_radiobutton.setChecked(True)
			self.ranklist_layout.addWidget(ranklist_radiobutton)
			self.ranklist_rbutton_list.append(ranklist_radiobutton)
			self.ranklist_layout.addStretch(1)
		self.ranklist_layout.addStretch(1)

		for ranklist in self.ranklist_rbutton_list:
			self.rbutton_signal_mapper.setMapping(
				ranklist, 
				self.ranklist_rbutton_list.index(
					ranklist
				)
			)
			ranklist.toggled.connect(self.rbutton_signal_mapper.map)
		# Now the signal mapper connects the checkbox to appropiae function call
		self.rbutton_signal_mapper.mapped[int].connect(
			self.ranklist_rbutton_state_change_handler
		)

		problem_config_score = self.config.get("Problem Max Score", 100)
		self.problem_max_score_label = QLabel('Problem Score:')
		self.problem_max_score = QLineEdit()
		self.problem_max_score.setPlaceholderText("Max Score")
		self.problem_max_score_widget = self.get_horizontal_widget(
			self.problem_max_score_label,
			self.problem_max_score
		)
		self.registerField("Problem Score", self.problem_max_score)

		penalty_config_score = self.config.get("Penalty Score", 0)
		self.penalty_score_label = QLabel('Penalty Score:  ')
		self.penalty_score = QLineEdit()
		self.penalty_score.setPlaceholderText("No Penalty")
		self.penalty_score_widget = self.get_horizontal_widget(
			self.penalty_score_label,
			self.penalty_score
		)
		self.registerField("Penalty Score", self.penalty_score)
		
		penalty_config_score = self.config.get("Penalty Time", 0)
		self.penalty_time_label = QLabel('Penalty Time:   ')
		self.penalty_time = QLineEdit()
		self.penalty_time.setPlaceholderText("0 Minutes")
		self.penalty_time_widget = self.get_horizontal_widget(
			self.penalty_time_label,
			self.penalty_time
		)
		self.registerField("Penalty Time", self.penalty_time)
		
		self.ranklist_layout.addWidget(self.problem_max_score_widget)
		self.ranklist_layout.addWidget(self.penalty_score_widget)
		self.ranklist_layout.addWidget(self.penalty_time_widget)


		
		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.message_ranklist)
		self.main_layout.addWidget(self.ranklist_widget)
		self.main_layout.setStretch(0, 10)
		self.main_layout.setStretch(1, 10)
		self.main_layout.setStretch(2, 80)
		return self.main_widget

	def ranklist_rbutton_state_change_handler(self, index):
		widget = self.ranklist_rbutton_list[index]
		state = widget.isChecked()
		if state == True:
			print("[ SETUP ] Ranklist " + self.available_ranklists[index], " : Selected")
			self.wizard().ranklist_states[self.available_ranklists[index]] = "TRUE"
		else:
			self.wizard().ranklist_states[self.available_ranklists[index]] = "FALSE"

	def all_done_page(self):
		self.title_label = QLabel('Finalize')
		self.title_label.setObjectName('main_screen_heading')
		message = (
			"You're all done here!\nCopy the generated config files into Server, Client and Judge folders\n" + 
			"and proceed to start the Server."
		)
		self.all_done_content = QLabel(message)
		self.all_done_content.setObjectName('main_screen_content')

		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.all_done_content)
		self.main_layout.setAlignment(self.all_done_content, Qt.AlignCenter)
		self.main_layout.addStretch(1)
		return self.main_widget