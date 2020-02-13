from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
# from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import *
from problem_ui import *
import socket, time, os

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
		self.automatic_switch.setChecked(False)
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
		# Signal mapper for Open Buttons
		self.problem_signal_mapper = QSignalMapper()
		self.problem_tests_mapper = QSignalMapper()

		self.title_label = QLabel('Problems')
		self.title_label.setObjectName('main_screen_heading')
		
		self.add_problem_button = QPushButton("Add Problem")
		self.add_problem_button.setFixedSize(200, 40)
		self.add_problem_button.setToolTip("Add a Problem")
		self.add_problem_button.clicked.connect(self.add_problem)

		self.reset_problems_button = QPushButton("Reset Problems")
		self.reset_problems_button.setFixedSize(200, 40)
		self.reset_problems_button.setToolTip("Delete all the Problems")
		self.reset_problems_button.clicked.connect(self.reset_all_problems)

		self.topbar_widget = QWidget()
		self.topbar_layout = QHBoxLayout(self.topbar_widget)
		self.topbar_layout.addWidget(self.title_label)
		self.topbar_layout.addStretch(1)
		self.topbar_layout.addWidget(self.add_problem_button)
		self.topbar_layout.addWidget(self.reset_problems_button)

		self.problems_list = QWidget()
		self.problems_list_layout = QVBoxLayout(self.problems_list)
		self.problems_list_layout.setAlignment(Qt.AlignTop)

		# Add existing problems to this scroll area
		self.problems = self.config.get('Problems', {})
		self.number_of_problems = self.config.get('Number Of Problems', 0)

		for i in range(1, self.number_of_problems + 1):
			# Make the card widget
			problem_id = "Problem " + str(i)
			problem = self.problems.get(problem_id)
			problem_name = problem["Name"]
			problem_code = problem["Code"]

			# Make problem directory for test data
			try:
				os.mkdir('./Problems/' + problem_code)
			except FileExistsError:
				pass
			except Exception as error:
				print(
					'[ CRITICAL ] The current directory requires sudo elevation to create folders.' + 
					'\nRestart Setup with sudo privileges.'
				)
				return


			card_widget = QWidget()
			card_widget.setFixedHeight(100)
			card_widget.setObjectName('problem_card')
			card_layout = QHBoxLayout(card_widget)
			main_label = QLabel( problem_id + " : ")
			main_label.setObjectName('main_screen_content')
			problem_name_widget = QLabel(problem_name)
			problem_name_widget.setObjectName('main_screen_sub_heading')
			problem_code_widget = QLabel(" [ " + problem_code + " ] ")
			problem_code_widget.setObjectName('main_screen_sub_heading2')
			problem_open_widget = QPushButton('Open')
			problem_test_files_widget = QPushButton('Test Files')
			card_layout.addWidget(main_label)
			card_layout.addWidget(problem_name_widget)
			card_layout.addWidget(problem_code_widget)
			card_layout.addStretch(1)
			card_layout.addWidget(problem_test_files_widget)
			card_layout.addWidget(problem_open_widget)
			card_layout.setAlignment(Qt.AlignLeft)
			card_layout.setAlignment(problem_open_widget, Qt.AlignRight)
			card_layout.setAlignment(problem_test_files_widget, Qt.AlignRight)
			self.problems_list_layout.addWidget(card_widget)

			self.problem_signal_mapper.setMapping(
				problem_open_widget, 
				i
			)
			self.problem_tests_mapper.setMapping(
				problem_test_files_widget, 
				i
			)
			problem_open_widget.clicked.connect(self.problem_signal_mapper.map)
			problem_test_files_widget.clicked.connect(self.problem_tests_mapper.map)

		self.problem_signal_mapper.mapped[int].connect(
			self.open_problem
		)
		self.problem_tests_mapper.mapped[int].connect(
			self.problem_test_files_manager
		)

		self.scroll_area = QScrollArea()
		self.scroll_area.setWidget(self.problems_list)
		self.scroll_area.setWidgetResizable(True)

		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.topbar_widget)
		self.main_layout.addWidget(self.scroll_area)
		self.main_layout.setStretch(0, 10)
		self.main_layout.setStretch(1, 90)
		self.main_layout.setAlignment(Qt.AlignTop)
		return self.main_widget

	def open_problem(self, p_id):
		print('[ OPEN ] Problem ', p_id)
		try:
			self.window.close()
		except:
			pass
		self.window = edit_problem_ui(
			p_id,
			self.config,
			self.wizard()
		)
		self.wizard().setVisible(False)
		self.window.show()
		self.window.activateWindow()

	def problem_test_files_manager(self, p_id):
		print('[ TESTS ] Problem ', p_id)
		try:
			self.window.close()
		except:
			pass
		self.window = test_files_ui(
			p_id,
			self.wizard()
		)
		self.wizard().setVisible(False)
		self.window.show()
		self.window.activateWindow()

	def reset_all_problems(self):
		try:
			self.window.close()
		except:
			pass

		remove_all_problems(self.wizard(), self.scroll_area)


	def add_problem(self):
		try:
			self.window.close()
		except:
			pass
		self.window = add_problem_ui(
			self.config, 
			self.wizard(), 
			self.problem_signal_mapper,
			self.problem_tests_mapper
		)
		self.wizard().setVisible(False)
		self.window.show()
		self.window.activateWindow()
	

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

		self.message_ranklist = QLabel('Ranklist Style')
		self.message_ranklist.setObjectName('main_screen_sub_heading')

		self.rbutton_signal_mapper = QSignalMapper()
		self.ranklist_rbutton_list = []
		
		self.available_ranklists = self.config.get("Ranking Styles")
		self.selected_ranklist = self.config.get("Selected Ranklist")

		self.ranklist_widget = QWidget()
		self.ranklist_layout  = QVBoxLayout(self.ranklist_widget)
		self.ranklist_layout.addWidget(self.message_ranklist)

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

		self.scoring_label = QLabel('Scoring')
		self.scoring_label.setObjectName('main_screen_sub_heading')

		problem_config_score = self.config.get("Problem Max Score", 100)
		self.problem_max_score_label = QLabel('Problem Score:')
		self.problem_max_score = QLineEdit()
		self.problem_max_score.setPlaceholderText("Max Score")
		self.problem_max_score.setText('100')
		self.problem_max_score_widget = self.get_horizontal_widget(
			self.problem_max_score_label,
			self.problem_max_score
		)
		self.registerField("Problem_Score", self.problem_max_score)

		penalty_config_score = self.config.get("Penalty Score", 0)
		self.penalty_score_label = QLabel('Penalty Score:  ')
		self.penalty_score = QLineEdit()
		self.penalty_score.setPlaceholderText("No Penalty")
		self.penalty_score.setText('0')
		self.penalty_score_widget = self.get_horizontal_widget(
			self.penalty_score_label,
			self.penalty_score
		)
		self.registerField("Penalty_Score", self.penalty_score)
		
		penalty_config_score = self.config.get("Penalty Time", 0)
		self.penalty_time_label = QLabel('Penalty Time:   ')
		self.penalty_time = QLineEdit()
		self.penalty_time.setPlaceholderText("0 Minutes")
		self.penalty_time.setText('0')
		self.penalty_time_widget = self.get_horizontal_widget(
			self.penalty_time_label,
			self.penalty_time
		)
		self.registerField("Penalty_Time", self.penalty_time)

		if self.selected_ranklist in ["IOI", "LONG"]:
			self.penalty_score.setReadOnly(True)
			self.penalty_score.setToolTip('This Ranklist has no penalty score')
			self.penalty_time.setReadOnly(True)
			self.penalty_time.setToolTip('This Ranklist has no penalty time')
		else:
			self.penalty_score.setReadOnly(False)
			self.penalty_score.setToolTip('Penalty score per wrong answer')
			self.penalty_time.setReadOnly(False)
			self.penalty_time.setToolTip('Penalty time (in minutes) per wrong answer')
		
		self.ranklist_layout.addWidget(self.scoring_label)
		self.ranklist_layout.addWidget(self.problem_max_score_widget)
		self.ranklist_layout.addWidget(self.penalty_score_widget)
		self.ranklist_layout.addWidget(self.penalty_time_widget)
		
		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.ranklist_widget)
		self.main_layout.setStretch(0, 10)
		self.main_layout.setStretch(1, 90)
	
		return self.main_widget

	def ranklist_rbutton_state_change_handler(self, index):
		widget = self.ranklist_rbutton_list[index]
		ranklist = self.available_ranklists[index]
		state = widget.isChecked()
		if state == True:
			print("[ SETUP ] Ranklist ", ranklist, " : Selected")
			self.wizard().ranklist_states[ranklist] = "TRUE"
			if ranklist in ["IOI", "LONG"]:
				self.penalty_score.setReadOnly(True)
				self.penalty_score.setToolTip('This Ranklist has no penalty score')
				self.penalty_time.setReadOnly(True)
				self.penalty_time.setToolTip('This Ranklist has no penalty time')
			else:
				self.penalty_score.setReadOnly(False)
				self.penalty_score.setToolTip('Penalty score per wrong answer')
				self.penalty_time.setReadOnly(False)
				self.penalty_time.setToolTip('Penalty time (in minutes) per wrong answer')

		else:
			self.wizard().ranklist_states[ranklist] = "FALSE"

	def all_done_page(self):
		self.title_label = QLabel('Finalize')
		self.title_label.setObjectName('main_screen_heading')
		message = (
			"You're all done here!\n" + 
			"Press the Finish button to generate the configuration files.\n" + 
			"Copy the generated config files into Server, Client and Judge folders in BitsOJ directory\n" + 
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