import sys
import time
import socket
import json
import os
import random
import string
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from Interface.table_interface import problem_table, add_problem_ui, edit_problem_ui
from database_management import manage_database, manage_local_ids, reset_database
from init_setup import read_write




class contest_setup(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowIcon(QIcon('Elements/logo.png'))
		self.setWindowTitle('BitsOJ v1.0.1 Contest Setup')
		self.resize(1200,700)
		os.system('mkdir Problems')
		self.flag = 0
		cur = manage_database.initialize_client_tables()
		manage_local_ids.initialize_local_id()
		self.client_config = {
			"client_id" : 'Null',
			"client_key" : '',
			"Username" : '',
			"rabbitmq_username" : '',
			"rabbitmq_password" : '',
			"host" : '',
			"No_of_Problems" : None,
			"Problems" : {},
			"Languages" : '',
			"Contest" : 'START',
			"Duration" : '00:00:00',
			"Start Time" : '00:00:00',
			"End Time" : '00:00:00',
			"Contest_Name" : '',
			"Contest_Theme" : ''
			}

		self.server_config = {
			"Server Username": "BitsOJ",
            "Server Password": "root",
            "Server IP": "localhost",
            "Judge Username": "judge1",
            "Judge Password": "judge1",
            "Login Allowed": "True",
            "Judge Login Allowed": "True",
            "Submission Allowed": "True",
            "Scoreboard Update Allowed": "True",
            "Judge Key": "000000000000000",
            "Client Key": "000000000000000",
            "File Password": "papa",
            "Contest Duration": "00:00:00",
            "Contest Status": "SETUP",
            "Contest Start Time": "00:00:00",
            "Contest End Time": "00:00:00",
            "Contest Set Time": 0,
            "Number Of Problems": "5",
            "Problems": {
                "Problem 1": "('The Begining of the End','TBE', 1, 1)",
                "Problem 2": "('Privet Drive','PD', 1, 1)",
                "Problem 3": "('Dumbledores Cloak','DC', 1, 1)",
                "Problem 4": "('The Auror Mania','TAM', 1, 1)",
                "Problem 5": "('A New Start','ANS', 1, 1)"
            },
            "Problem Codes": "('TBE', 'PD', 'DC', 'TAM', 'ANS')",
            "Languages": "('C','C++','JAVA','PYTHON-2')",
            "Ranking Algorithm": "IOI",
            "AC Points": 100,
            "Penalty Score": -20,
            "Penalty Time": 20,
            "Manual Review": "False",
            "Submision Time Limit" : 0
		}
		self.judge_config = {}

		self.language_tuple = ()
		
		self.data = {"Problems" : {}}


		self.db = self.init_qt_database()

		contest_setup.init_GUI(self)
		contest_setup.rabbitmq(self)
		contest_setup.problem(self)
		contest_setup.language(self)
		contest_setup.contest(self)
		contest_setup.security(self)
		contest_setup.ranking(self)
		return

	def init_GUI(self):

		#Define our top bar
		logo = QLabel(self)
		logo_image = QPixmap('Elements/bitwise_header.png')
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
		self.rabbitmq_tab = QWidget()
		self.problem_tab = QWidget()
		self.language_tab = QWidget()
		self.contest_tab = QWidget()
		self.security_tab = QWidget()
		self.ranking_tab = QWidget()
		self.final_tab = QWidget()

		self.top_tab.addTab(self.rabbitmq_tab, "RabbitMQ Details")
		self.top_tab.addTab(self.problem_tab, "Problems")
		self.top_tab.addTab(self.language_tab, "Languages")
		self.top_tab.addTab(self.contest_tab, "Contest")
		self.top_tab.addTab(self.security_tab, "Security")
		self.top_tab.addTab(self.ranking_tab, "Ranking")
		self.top_tab.addTab(self.final_tab, 'Final Save')


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

	def rabbitmq(self):
		self.client_tab_layout = QVBoxLayout()
		self.tabs = QTabWidget()
		self.tabs.setObjectName('client_tabs')
		self.rabbitmq_client_detail = QWidget()
		self.rabbitmq_server_detail = QWidget()
		self.rabbitmq_judge_detail = QWidget()

		


		###################################################################
		##################### RABBITMQ CLIENT TAB #########################
		###################################################################

		self.rabbitmq_creds = QVBoxLayout()
		rabbitmq_heading = QLabel('RabbitMQ Client Details')
		rabbitmq_heading.setObjectName('heading')
		self.rabbitmq_username = QHBoxLayout()
		self.rabbitmq_username_label = QLabel('RABBIT_MQ USERNAME    :   ')
		self.rabbitmq_username_label.setObjectName('general')
		self.rabbitmq_username_text = QLineEdit()
		self.rabbitmq_username_text.setPlaceholderText('Example : Client')
		self.rabbitmq_username_text.setObjectName('general_text')
		self.rabbitmq_username_text.setFixedWidth(400)
		self.rabbitmq_username_text.setFixedHeight(50)
		self.rabbitmq_username.addWidget(self.rabbitmq_username_label)
		self.rabbitmq_username.addWidget(self.rabbitmq_username_text)
		self.rabbitmq_username.addStretch(1)
		self.rabbitmq_username.addSpacing(0)
		self.username_widget = QWidget()
		self.username_widget.setLayout(self.rabbitmq_username)
		self.rabbitmq_password = QHBoxLayout()
		self.rabbitmq_password_label = QLabel('RABBIT_MQ PASSWORD   :   ')
		self.rabbitmq_password_label.setObjectName('general')
		self.rabbitmq_password_text = QLineEdit()
		self.rabbitmq_password_text.setPlaceholderText('Example : Client')
		self.rabbitmq_password_text.setObjectName('general_text')
		self.rabbitmq_password_text.setFixedWidth(400)
		self.rabbitmq_password_text.setFixedHeight(50)
		self.rabbitmq_password.addWidget(self.rabbitmq_password_label)
		self.rabbitmq_password.addWidget(self.rabbitmq_password_text)
		self.rabbitmq_password.addStretch(1)
		self.rabbitmq_password.addSpacing(0)
		self.password_widget = QWidget()
		self.password_widget.setLayout(self.rabbitmq_password)
		self.manual = QRadioButton('Manual IP')
		self.manual.setChecked(True)
		self.manual.toggled.connect(lambda:self.button_state(self.manual))
		self.automatic = QRadioButton('Automatic IP')
		self.automatic.toggled.connect(lambda:self.button_state(self.automatic))
		self.rabbitmq_host = QHBoxLayout()
		self.rabbitmq_host_label = QLabel('RABBIT_MQ HOST              :   ')
		self.rabbitmq_host_label.setObjectName('general')
		self.rabbitmq_host_text = QLineEdit()
		self.rabbitmq_host_text.setPlaceholderText('Example : 127.0.0.1')
		self.rabbitmq_host_text.setObjectName('general_text')
		self.rabbitmq_host_text.setFixedWidth(400)
		self.rabbitmq_host_text.setFixedHeight(50)
		self.rabbitmq_host.addWidget(self.rabbitmq_host_label)
		self.rabbitmq_host.addWidget(self.rabbitmq_host_text)
		self.rabbitmq_host.addWidget(self.manual)
		self.rabbitmq_host.addWidget(self.automatic)
		self.rabbitmq_host.addStretch(1)
		self.rabbitmq_host.addSpacing(0)
		self.host_widget = QWidget()
		self.host_widget.setLayout(self.rabbitmq_host)
		self.rabbitmq_button = QHBoxLayout()
		self.save_button = QPushButton('Save')
		self.save_button.setObjectName('general')
		self.save_button.setFixedSize(200,50)
		self.save_button.clicked.connect(lambda:self.save_client_rabbitmq())
		self.edit_button = QPushButton('Edit')
		self.edit_button.setObjectName('general')
		self.edit_button.setFixedSize(200,50)
		self.edit_button.clicked.connect(lambda:self.edit_client_rabbitmq())
		self.rabbitmq_button.addWidget(self.save_button, alignment=Qt.AlignRight)
		self.rabbitmq_button.addWidget(self.edit_button, alignment=Qt.AlignRight)
		self.rabbitmq_button.addStretch(1)
		self.rabbitmq_button.addSpacing(0)
		self.button_widget = QWidget()
		self.button_widget.setLayout(self.rabbitmq_button)
		self.rabbitmq_creds.addWidget(rabbitmq_heading)
		self.rabbitmq_creds.addWidget(self.username_widget)
		self.rabbitmq_creds.addWidget(self.password_widget)
		self.rabbitmq_creds.addWidget(self.host_widget)
		self.rabbitmq_creds.addWidget(self.button_widget, alignment=Qt.AlignBottom)
		self.rabbitmq_creds.addStretch(1)
		self.rabbitmq_creds.addSpacing(0)
		self.rabbitmq_client_detail.setLayout(self.rabbitmq_creds)


		###################################################################
		##################### RABBITMQ SERVER TAB #########################
		###################################################################


		self.rabbitmq_server_creds = QVBoxLayout()
		rabbitmq_server_heading = QLabel('RabbitMQ Server Details')
		rabbitmq_server_heading.setObjectName('heading')
		self.rabbitmq_server_username = QHBoxLayout()
		self.rabbitmq_server_username_label = QLabel('RABBIT_MQ USERNAME    :   ')
		self.rabbitmq_server_username_label.setObjectName('general')
		self.rabbitmq_server_username_text = QLineEdit()
		self.rabbitmq_server_username_text.setPlaceholderText('Example : Client')
		self.rabbitmq_server_username_text.setObjectName('general_text')
		self.rabbitmq_server_username_text.setFixedWidth(400)
		self.rabbitmq_server_username_text.setFixedHeight(50)
		self.rabbitmq_server_username.addWidget(self.rabbitmq_server_username_label)
		self.rabbitmq_server_username.addWidget(self.rabbitmq_server_username_text)
		self.rabbitmq_server_username.addStretch(1)
		self.rabbitmq_server_username.addSpacing(0)
		self.username_server_widget = QWidget()
		self.username_server_widget.setLayout(self.rabbitmq_server_username)
		self.rabbitmq_server_password = QHBoxLayout()
		self.rabbitmq_server_password_label = QLabel('RABBIT_MQ PASSWORD   :   ')
		self.rabbitmq_server_password_label.setObjectName('general')
		self.rabbitmq_server_password_text = QLineEdit()
		self.rabbitmq_server_password_text.setPlaceholderText('Example : Client')
		self.rabbitmq_server_password_text.setObjectName('general_text')
		self.rabbitmq_server_password_text.setFixedWidth(400)
		self.rabbitmq_server_password_text.setFixedHeight(50)
		self.rabbitmq_server_password.addWidget(self.rabbitmq_server_password_label)
		self.rabbitmq_server_password.addWidget(self.rabbitmq_server_password_text)
		self.rabbitmq_server_password.addStretch(1)
		self.rabbitmq_server_password.addSpacing(0)
		self.password_server_widget = QWidget()
		self.password_server_widget.setLayout(self.rabbitmq_server_password)
		self.manual_server = QRadioButton('Manual IP')
		self.manual_server.setChecked(True)
		self.manual_server.toggled.connect(lambda:self.button_state_server(self.manual_server))
		self.automatic_server = QRadioButton('Automatic IP')
		self.automatic_server.toggled.connect(lambda:self.button_state_server(self.automatic_server))
		self.rabbitmq_server_host = QHBoxLayout()
		self.rabbitmq_server_host_label = QLabel('RABBIT_MQ HOST              :   ')
		self.rabbitmq_server_host_label.setObjectName('general')
		self.rabbitmq_server_host_text = QLineEdit()
		self.rabbitmq_server_host_text.setPlaceholderText('Example : 127.0.0.1')
		self.rabbitmq_server_host_text.setObjectName('general_text')
		self.rabbitmq_server_host_text.setFixedWidth(400)
		self.rabbitmq_server_host_text.setFixedHeight(50)
		self.rabbitmq_server_host.addWidget(self.rabbitmq_server_host_label)
		self.rabbitmq_server_host.addWidget(self.rabbitmq_server_host_text)
		self.rabbitmq_server_host.addWidget(self.manual_server)
		self.rabbitmq_server_host.addWidget(self.automatic_server)
		self.rabbitmq_server_host.addStretch(1)
		self.rabbitmq_server_host.addSpacing(0)
		self.host_server_widget = QWidget()
		self.host_server_widget.setLayout(self.rabbitmq_server_host)
		self.rabbitmq_server_button = QHBoxLayout()
		self.save_server_button = QPushButton('Save')
		self.save_server_button.setObjectName('general')
		self.save_server_button.setFixedSize(200,50)
		self.save_server_button.clicked.connect(lambda:self.save_server_rabbitmq())
		self.edit_server_button = QPushButton('Edit')
		self.edit_server_button.setObjectName('general')
		self.edit_server_button.setFixedSize(200,50)
		self.edit_server_button.clicked.connect(lambda:self.edit_server_rabbitmq())
		self.rabbitmq_server_button.addWidget(self.save_server_button, alignment=Qt.AlignRight)
		self.rabbitmq_server_button.addWidget(self.edit_server_button, alignment=Qt.AlignRight)
		self.rabbitmq_server_button.addStretch(1)
		self.rabbitmq_server_button.addSpacing(0)
		self.button_server_widget = QWidget()
		self.button_server_widget.setLayout(self.rabbitmq_server_button)
		self.rabbitmq_server_creds.addWidget(rabbitmq_server_heading)
		self.rabbitmq_server_creds.addWidget(self.username_server_widget)
		self.rabbitmq_server_creds.addWidget(self.password_server_widget)
		self.rabbitmq_server_creds.addWidget(self.host_server_widget)
		self.rabbitmq_server_creds.addWidget(self.button_server_widget, alignment=Qt.AlignBottom)
		self.rabbitmq_server_creds.addStretch(1)
		self.rabbitmq_server_creds.addSpacing(0)
		self.rabbitmq_server_detail.setLayout(self.rabbitmq_server_creds)



		###################################################################
		##################### RABBITMQ JUDGE TAB ##########################
		###################################################################


		self.rabbitmq_judge_creds = QVBoxLayout()
		rabbitmq_judge_heading = QLabel('RabbitMQ Judge Details')
		rabbitmq_judge_heading.setObjectName('heading')
		self.rabbitmq_judge_username = QHBoxLayout()
		self.rabbitmq_judge_username_label = QLabel('RABBIT_MQ USERNAME    :   ')
		self.rabbitmq_judge_username_label.setObjectName('general')
		self.rabbitmq_judge_username_text = QLineEdit()
		self.rabbitmq_judge_username_text.setPlaceholderText('Example : Client')
		self.rabbitmq_judge_username_text.setObjectName('general_text')
		self.rabbitmq_judge_username_text.setFixedWidth(400)
		self.rabbitmq_judge_username_text.setFixedHeight(50)
		self.rabbitmq_judge_username.addWidget(self.rabbitmq_judge_username_label)
		self.rabbitmq_judge_username.addWidget(self.rabbitmq_judge_username_text)
		self.rabbitmq_judge_username.addStretch(1)
		self.rabbitmq_judge_username.addSpacing(0)
		self.username_judge_widget = QWidget()
		self.username_judge_widget.setLayout(self.rabbitmq_judge_username)
		self.rabbitmq_judge_password = QHBoxLayout()
		self.rabbitmq_judge_password_label = QLabel('RABBIT_MQ PASSWORD   :   ')
		self.rabbitmq_judge_password_label.setObjectName('general')
		self.rabbitmq_judge_password_text = QLineEdit()
		self.rabbitmq_judge_password_text.setPlaceholderText('Example : Client')
		self.rabbitmq_judge_password_text.setObjectName('general_text')
		self.rabbitmq_judge_password_text.setFixedWidth(400)
		self.rabbitmq_judge_password_text.setFixedHeight(50)
		self.rabbitmq_judge_password.addWidget(self.rabbitmq_judge_password_label)
		self.rabbitmq_judge_password.addWidget(self.rabbitmq_judge_password_text)
		self.rabbitmq_judge_password.addStretch(1)
		self.rabbitmq_judge_password.addSpacing(0)
		self.password_judge_widget = QWidget()
		self.password_judge_widget.setLayout(self.rabbitmq_judge_password)
		self.manual_judge = QRadioButton('Manual IP')
		self.manual_judge.setChecked(True)
		self.manual_judge.toggled.connect(lambda:self.button_state_judge(self.manual_judge))
		self.automatic_judge = QRadioButton('Automatic IP')
		self.automatic_judge.toggled.connect(lambda:self.button_state_judge(self.automatic_judge))
		self.rabbitmq_judge_host = QHBoxLayout()
		self.rabbitmq_judge_host_label = QLabel('RABBIT_MQ HOST              :   ')
		self.rabbitmq_judge_host_label.setObjectName('general')
		self.rabbitmq_judge_host_text = QLineEdit()
		self.rabbitmq_judge_host_text.setPlaceholderText('Example : 127.0.0.1')
		self.rabbitmq_judge_host_text.setObjectName('general_text')
		self.rabbitmq_judge_host_text.setFixedWidth(400)
		self.rabbitmq_judge_host_text.setFixedHeight(50)
		self.rabbitmq_judge_host.addWidget(self.rabbitmq_judge_host_label)
		self.rabbitmq_judge_host.addWidget(self.rabbitmq_judge_host_text)
		self.rabbitmq_judge_host.addWidget(self.manual_judge)
		self.rabbitmq_judge_host.addWidget(self.automatic_judge)
		self.rabbitmq_judge_host.addStretch(1)
		self.rabbitmq_judge_host.addSpacing(0)
		self.host_judge_widget = QWidget()
		self.host_judge_widget.setLayout(self.rabbitmq_judge_host)
		self.rabbitmq_judge_button = QHBoxLayout()
		self.save_judge_button = QPushButton('Save')
		self.save_judge_button.setObjectName('general')
		self.save_judge_button.setFixedSize(200,50)
		self.save_judge_button.clicked.connect(lambda:self.save_judge_rabbitmq())
		self.edit_judge_button = QPushButton('Edit')
		self.edit_judge_button.setObjectName('general')
		self.edit_judge_button.setFixedSize(200,50)
		self.edit_judge_button.clicked.connect(lambda:self.edit_judge_rabbitmq())
		self.rabbitmq_judge_button.addWidget(self.save_judge_button, alignment=Qt.AlignRight)
		self.rabbitmq_judge_button.addWidget(self.edit_judge_button, alignment=Qt.AlignRight)
		self.rabbitmq_judge_button.addStretch(1)
		self.rabbitmq_judge_button.addSpacing(0)
		self.button_judge_widget = QWidget()
		self.button_judge_widget.setLayout(self.rabbitmq_judge_button)
		self.rabbitmq_judge_creds.addWidget(rabbitmq_judge_heading)
		self.rabbitmq_judge_creds.addWidget(self.username_judge_widget)
		self.rabbitmq_judge_creds.addWidget(self.password_judge_widget)
		self.rabbitmq_judge_creds.addWidget(self.host_judge_widget)
		self.rabbitmq_judge_creds.addWidget(self.button_judge_widget, alignment=Qt.AlignBottom)
		self.rabbitmq_judge_creds.addStretch(1)
		self.rabbitmq_judge_creds.addSpacing(0)
		self.rabbitmq_judge_detail.setLayout(self.rabbitmq_judge_creds)
		


		######################################################################
		######################## FINAL TAB ###################################
		######################################################################


		
		self.tabs.addTab(self.rabbitmq_server_detail, "Server Creds")
		self.tabs.addTab(self.rabbitmq_judge_detail, "Judge Creds")
		self.tabs.addTab(self.rabbitmq_client_detail, "Client Creds")

		

		self.client_tab_layout.addWidget(self.tabs)
		self.rabbitmq_tab.setLayout(self.client_tab_layout)
		self.rabbitmq_tab.setObjectName('client_tab')
		return


	def problem(self):

		##################################################################
		####################### PROBLEM TAB ##############################
		##################################################################

		
		problem_tab = QVBoxLayout()
		problem_heading = QLabel('Add Problems')
		problem_heading.setObjectName('heading')
		self.add_table_view,self.table_model = problem_table.problem_model(self)
		if self.flag == 0:
			reset_database.reset_problem(self.table_model)
			self.flag = 1
		problem_button = QHBoxLayout()
		self.add_problem = QPushButton('Add')
		self.add_problem.setObjectName('general')
		self.add_problem.setFixedSize(200,50)
		self.add_problem.clicked.connect(lambda:self.add_problem_client())
		self.edit_problem = QPushButton('Edit')
		self.edit_problem.setObjectName('general')
		self.edit_problem.setFixedSize(200,50)
		self.edit_problem.clicked.connect(lambda:self.edit_problem_client(self.add_table_view.selectionModel().currentIndex().row()))
		self.reset_problem = QPushButton('Reset')
		self.reset_problem.setObjectName('general')
		self.reset_problem.setFixedSize(200,50)
		self.reset_problem.clicked.connect(lambda:self.confirm_event())
		problem_button.addWidget(self.add_problem)
		problem_button.addWidget(self.edit_problem)
		problem_button.addWidget(self.reset_problem)
		problem_button.addStretch(1)
		problem_button.addSpacing(0)
		problem_button_widget = QWidget()
		problem_button_widget.setLayout(problem_button)
		problem_tab.addWidget(problem_heading)
		problem_tab.addWidget(self.add_table_view)
		problem_tab.addWidget(problem_button_widget)
		problem_tab.addStretch(1)
		problem_tab.addSpacing(0)
		self.problem_tab.setLayout(problem_tab)


	def language(self):
		#####################################################################
		###################### LANGUAGE TAB #################################
		#####################################################################

		languages = QVBoxLayout()
		language_heading = QLabel('Select Languages')
		language_heading.setObjectName('heading')
		base = QHBoxLayout()
		self.all = QRadioButton('Select All')
		self.some = QRadioButton('Manual Selection')
		self.some.setChecked(True)
		self.all.toggled.connect(lambda:self.select_language_base(self.all))
		self.some.toggled.connect(lambda:self.select_language_base(self.some))
		base.addWidget(self.all, alignment=Qt.AlignCenter)
		base.addWidget(self.some, alignment=Qt.AlignCenter)
		base.addStretch(1)
		base.addSpacing(0)
		base_widget = QWidget()
		base_widget.setLayout(base)
		self.c = QCheckBox("C",self)
		self.cplusplus = QCheckBox('C++',self)
		self.python2 = QCheckBox('PYTHON-2',self)
		self.python3 = QCheckBox("PYTHON-3",self)
		self.java = QCheckBox('JAVA',self)
		self.general = QCheckBox('TEXT ANSWER',self)

		self.c.setObjectName('checkbox')
		self.cplusplus.setObjectName('checkbox')
		self.python2.setObjectName('checkbox')
		self.python3.setObjectName('checkbox')
		self.java.setObjectName('checkbox')
		self.general.setObjectName('checkbox')

		self.language_button = QHBoxLayout()
		self.save_language_button = QPushButton('Save')
		self.save_language_button.setObjectName('general')
		self.save_language_button.setFixedSize(200,50)
		self.save_language_button.clicked.connect(lambda:self.save_client_language())
		self.edit_language_button = QPushButton('Edit')
		self.edit_language_button.setObjectName('general')
		self.edit_language_button.setFixedSize(200,50)
		self.edit_language_button.clicked.connect(lambda:self.edit_client_language())
		self.language_button.addWidget(self.save_language_button, alignment=Qt.AlignRight)
		self.language_button.addWidget(self.edit_language_button, alignment=Qt.AlignRight)
		self.language_button.addStretch(1)
		self.language_button.addSpacing(0)
		self.language_button_widget = QWidget()
		self.language_button_widget.setLayout(self.language_button)

		languages.addWidget(language_heading)
		languages.addWidget(base_widget)
		languages.addWidget(self.c)
		languages.addWidget(self.cplusplus)
		languages.addWidget(self.python2)
		languages.addWidget(self.python3)
		languages.addWidget(self.java)
		languages.addWidget(self.general)
		languages.addWidget(self.language_button_widget)
		languages.addStretch(1)
		languages.addSpacing(0)

		self.language_tab.setLayout(languages)


	def contest(self):

		#####################################################################
		######################## CONTEST TAB ################################
		#####################################################################

		contest_tab = QVBoxLayout()
		contest_heading = QLabel('Contest Details')
		contest_heading.setObjectName('heading')
		contest_name = QHBoxLayout()
		contest_name_label = QLabel('CONTEST NAME              :   ')
		contest_name_label.setObjectName('general')
		self.contest_name_text = QLineEdit()
		self.contest_name_text.setPlaceholderText('')
		self.contest_name_text.setObjectName('general_text')
		self.contest_name_text.setFixedWidth(400)
		self.contest_name_text.setFixedHeight(50)
		contest_name.addWidget(contest_name_label)
		contest_name.addWidget(self.contest_name_text)
		contest_name.addStretch(1)
		contest_name.addSpacing(0)
		contest_name_widget = QWidget()
		contest_name_widget.setLayout(contest_name)
		contest_theme = QHBoxLayout()
		contest_theme_label = QLabel('CONTEST THEME            :   ')
		contest_theme_label.setObjectName('general')
		self.contest_theme_text = QLineEdit()
		self.contest_theme_text.setPlaceholderText('')
		self.contest_theme_text.setObjectName('general_text')
		self.contest_theme_text.setFixedWidth(400)
		self.contest_theme_text.setFixedHeight(50)
		contest_theme.addWidget(contest_theme_label)
		contest_theme.addWidget(self.contest_theme_text)
		contest_theme.addStretch(1)
		contest_theme.addSpacing(0)
		contest_theme_widget = QWidget()
		contest_theme_widget.setLayout(contest_theme)
		client_key = QHBoxLayout()
		client_key_label = QLabel('CLIENT KEY                     :   ')
		client_key_label.setObjectName('general')
		self.client_key_text = QLineEdit()
		self.client_key_text.setPlaceholderText('')
		self.client_key_text.setObjectName('general_text')
		self.client_key_text.setEchoMode(QLineEdit.Password)
		self.client_key_text.setReadOnly(True)
		self.client_key_text.setFixedWidth(400)
		self.client_key_text.setFixedHeight(50)
		generate_client_key = QPushButton('Generate')
		generate_client_key.setObjectName('general')
		generate_client_key.setFixedSize(200,50)
		generate_client_key.clicked.connect(lambda:self.generate_key(0))
		client_key.addWidget(client_key_label)
		client_key.addWidget(self.client_key_text)
		client_key.addWidget(generate_client_key)
		client_key.addStretch(1)
		client_key.addSpacing(0)
		client_key_widget = QWidget()
		client_key_widget.setLayout(client_key)
		judge_key = QHBoxLayout()
		judge_key_label = QLabel('JUDGE KEY                      :   ')
		judge_key_label.setObjectName('general')
		self.judge_key_text = QLineEdit()
		self.judge_key_text.setPlaceholderText('')
		self.judge_key_text.setObjectName('general_text')
		self.judge_key_text.setReadOnly(True)
		self.judge_key_text.setEchoMode(QLineEdit.Password)
		self.judge_key_text.setFixedWidth(400)
		self.judge_key_text.setFixedHeight(50)
		generate_judge_key = QPushButton('Generate')
		generate_judge_key.setObjectName('general')
		generate_judge_key.setFixedSize(200,50)
		generate_judge_key.clicked.connect(lambda:self.generate_key(1))
		judge_key.addWidget(judge_key_label)
		judge_key.addWidget(self.judge_key_text)
		judge_key.addWidget(generate_judge_key)
		judge_key.addStretch(1)
		judge_key.addSpacing(0)
		judge_key_widget = QWidget()
		judge_key_widget.setLayout(judge_key)
		contest_duration = QHBoxLayout()
		contest_duration_label = QLabel('CONTEST DURATION     :   ')
		contest_duration_label.setObjectName('general')
		self.contest_duration_text = QLineEdit()
		self.contest_duration_text.setPlaceholderText('Duration  -  HH:MM:SS')
		self.contest_duration_text.setObjectName('general_text')
		self.contest_duration_text.setFixedWidth(400)
		self.contest_duration_text.setFixedHeight(50)
		contest_duration.addWidget(contest_duration_label)
		contest_duration.addWidget(self.contest_duration_text)
		contest_duration.addStretch(1)
		contest_duration.addSpacing(0)
		contest_duration_widget = QWidget()
		contest_duration_widget.setLayout(contest_duration)
		start_time = QHBoxLayout()
		start_time_label = QLabel('CONTEST START TIME   :   ')
		start_time_label.setObjectName('general')
		self.start_time_text = QLineEdit()
		self.start_time_text.setPlaceholderText('12 Hour - HH:MM:SS')
		self.start_time_text.setObjectName('general_text')
		self.start_time_text.setFixedWidth(400)
		self.start_time_text.setFixedHeight(50)
		self.am_pm = QComboBox()
		self.am_pm.setFixedWidth(50)
		self.am_pm.setFixedHeight(40)
		self.am_pm.setObjectName('general')
		self.am_pm.addItem('AM')
		self.am_pm.addItem('PM')
		self.hour_12 = QRadioButton('12 Hour')
		self.hour_24 = QRadioButton('24 Hour')
		self.hour_12.setChecked(True)
		self.hour_12.toggled.connect(lambda:self.select_format(self.hour_12))
		self.hour_24.toggled.connect(lambda:self.select_format(self.hour_24))

		start_time.addWidget(start_time_label)
		start_time.addWidget(self.start_time_text)
		start_time.addWidget(self.am_pm)
		start_time.addWidget(self.hour_12)
		start_time.addWidget(self.hour_24)
		start_time.addStretch(1)
		start_time.addSpacing(0)
		start_time_widget = QWidget()
		start_time_widget.setLayout(start_time)

		client_key_button = QHBoxLayout()
		self.save_client_key_button = QPushButton('Save')
		self.save_client_key_button.setObjectName('general')
		self.save_client_key_button.setFixedSize(200,50)
		self.save_client_key_button.clicked.connect(lambda:self.save_contest_tab())
		self.edit_client_key_button = QPushButton('Edit')
		self.edit_client_key_button.setObjectName('general')
		self.edit_client_key_button.setFixedSize(200,50)
		self.edit_client_key_button.clicked.connect(lambda:self.edit_contest_tab())
		client_key_button.addWidget(self.save_client_key_button, alignment=Qt.AlignRight)
		client_key_button.addWidget(self.edit_client_key_button, alignment=Qt.AlignRight)
		client_key_button.addStretch(1)
		client_key_button.addSpacing(0)
		self.client_key_button_widget = QWidget()
		self.client_key_button_widget.setLayout(client_key_button)

		contest_tab.addWidget(contest_heading)
		contest_tab.addWidget(contest_name_widget)
		contest_tab.addWidget(contest_theme_widget)
		contest_tab.addWidget(client_key_widget)
		contest_tab.addWidget(judge_key_widget)
		# contest_tab.addWidget(contest_duration_widget)
		# contest_tab.addWidget(start_time_widget)
		contest_tab.addWidget(self.client_key_button_widget)
		contest_tab.addStretch(1)
		contest_tab.addSpacing(0)

		self.contest_tab.setLayout(contest_tab)



	###################################### SECURITY #########################################

	def security(self):
		main_security = QVBoxLayout()
		heading = QLabel('Security')
		heading.setObjectName('heading')

		problems_password = QHBoxLayout()
		problems_password_label = QLabel('Problems Password  :  ')
		problems_password_label.setObjectName('general')
		self.problems_password_text = QLineEdit()
		self.problems_password_text.setObjectName('general_text')
		self.problems_password_text.setEchoMode(QLineEdit.Password)
		self.problems_password_text.setReadOnly(True)
		problems_password.addWidget(problems_password_label)
		problems_password.addWidget(self.problems_password_text)
		generate_password_key = QPushButton('Generate')
		generate_password_key.setObjectName('general')
		generate_password_key.setFixedSize(200,50)
		generate_password_key.clicked.connect(lambda:self.generate_key(2))
		problems_password.addWidget(generate_password_key)
		problems_password.addStretch(0)
		problems_password.addSpacing(1)
		problems_password_widget = QWidget()
		problems_password_widget.setLayout(problems_password)

		password_key_button = QHBoxLayout()
		self.save_password_key_button = QPushButton('Save')
		self.save_password_key_button.setObjectName('general')
		self.save_password_key_button.setFixedSize(200,50)
		self.save_password_key_button.clicked.connect(lambda:self.save_security_tab())
		self.edit_password_key_button = QPushButton('Edit')
		self.edit_password_key_button.setObjectName('general')
		self.edit_password_key_button.setFixedSize(200,50)
		self.edit_password_key_button.clicked.connect(lambda:self.edit_security_tab())
		password_key_button.addWidget(self.save_password_key_button, alignment=Qt.AlignRight)
		password_key_button.addWidget(self.edit_password_key_button, alignment=Qt.AlignRight)
		password_key_button.addStretch(0)
		password_key_button.addSpacing(1)
		self.password_key_button_widget = QWidget()
		self.password_key_button_widget.setLayout(password_key_button)


		main_security.addWidget(heading)
		main_security.addWidget(problems_password_widget)

		main_security.addStretch(0)
		main_security.addSpacing(1)
		main_security.addWidget(self.password_key_button_widget)

		self.security_tab.setLayout(main_security)


	###################################### RANKING ##########################################

	def ranking(self):

		main = QVBoxLayout()


		heading = QLabel('Ranking System')
		heading.setObjectName('heading')
		ranking_system = QHBoxLayout()
		self.IOI = QRadioButton('IOI System')
		self.IOI.setChecked(True)
		self.IOI.toggled.connect(lambda:self.rank_state(self.IOI))
		self.ACM = QRadioButton('ACM System')
		self.ACM.toggled.connect(lambda:self.rank_state(self.ACM))
		self.LONG = QRadioButton('LONG System')
		self.LONG.toggled.connect(lambda:self.rank_state(self.LONG))
		ranking_system.addWidget(self.IOI)
		ranking_system.addWidget(self.ACM)
		ranking_system.addWidget(self.LONG)
		ranking_system.addStretch(0)
		ranking_system.addSpacing(1)
		ranking_widget = QWidget()
		ranking_widget.setLayout(ranking_system)
		ac = QHBoxLayout()
		ac_label = QLabel('AC Points               :  ')
		ac_label.setObjectName('general')
		self.ac_text = QLineEdit()
		self.ac_text.setPlaceholderText('AC Points')
		self.ac_text.setText('100')
		self.ac_text.setObjectName('general_text')
		self.ac_text.setReadOnly(True)
		self.ac_text.setFixedWidth(400)
		self.ac_text.setFixedHeight(50)
		ac.addWidget(ac_label)
		ac.addWidget(self.ac_text)
		ac.addStretch(0)
		ac.addSpacing(1)
		ac_widget = QWidget()
		ac_widget.setLayout(ac)
		penalty_points = QHBoxLayout()
		penalty_points_label = QLabel('Penalty Points       :  ')
		penalty_points_label.setObjectName('general')
		self.penalty_points_text = QLineEdit()
		self.penalty_points_text.setPlaceholderText('Penalty Points')
		self.penalty_points_text.setText('-20')
		self.penalty_points_text.setObjectName('general_text')
		self.penalty_points_text.setReadOnly(True)
		self.penalty_points_text.setFixedWidth(400)
		self.penalty_points_text.setFixedHeight(50)
		penalty_points.addWidget(penalty_points_label)
		penalty_points.addWidget(self.penalty_points_text)
		penalty_points.addStretch(0)
		penalty_points.addSpacing(1)
		penalty_points_widget = QWidget()
		penalty_points_widget.setLayout(penalty_points)
		penalty_time = QHBoxLayout()
		penalty_time_label = QLabel('Penalty Time          :  ')
		penalty_time_label.setObjectName('general')
		self.penalty_time_text = QLineEdit()
		self.penalty_time_text.setPlaceholderText('Penalty Time')
		self.penalty_time_text.setText('20')
		self.penalty_time_text.setObjectName('general_text')
		self.penalty_time_text.setReadOnly(True)
		self.penalty_time_text.setFixedWidth(400)
		self.penalty_time_text.setFixedHeight(50)
		penalty_time.addWidget(penalty_time_label)
		penalty_time.addWidget(self.penalty_time_text)
		penalty_time.addStretch(0)
		penalty_time.addSpacing(1)
		penalty_time_widget = QWidget()
		penalty_time_widget.setLayout(penalty_time)

		ranking_button = QHBoxLayout()
		self.save_ranking_button = QPushButton('Save')
		self.save_ranking_button.setObjectName('general')
		self.save_ranking_button.setFixedSize(200,50)
		self.save_ranking_button.clicked.connect(lambda:self.save_rank_tab())
		self.edit_ranking_button = QPushButton('Edit')
		self.edit_ranking_button.setObjectName('general')
		self.edit_ranking_button.setFixedSize(200,50)
		self.edit_ranking_button.clicked.connect(lambda:self.edit_rank_tab())
		ranking_button.addWidget(self.save_ranking_button, alignment=Qt.AlignRight)
		ranking_button.addWidget(self.edit_ranking_button, alignment=Qt.AlignRight)
		ranking_button.addStretch(1)
		ranking_button.addSpacing(0)
		ranking_button_widget = QWidget()
		ranking_button_widget.setLayout(ranking_button)


		main.addWidget(heading)
		main.addWidget(ranking_widget)
		main.addWidget(ac_widget)
		main.addWidget(penalty_points_widget)
		main.addWidget(penalty_time_widget)
		main.addWidget(ranking_button_widget)
		main.addStretch(0)
		main.addSpacing(1)
		self.ranking_tab.setLayout(main)





	def generate_key(self,i):
		if i == 0:
			key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
			self.client_key_text.setText(key)
			self.client_key_text.setReadOnly(True)
		elif i == 1:
			key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
			self.judge_key_text.setText(key)
			self.judge_key_text.setReadOnly(True)
		else:
			key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
			self.problems_password_text.setText(key)
			self.problems_password_text.setReadOnly(True)


	def save_rank_tab(self):
		self.IOI.setDisabled(True)
		self.ACM.setDisabled(True)
		self.LONG.setDisabled(True)

	def edit_rank_tab(self):
		self.IOI.setDisabled(False)
		self.ACM.setDisabled(False)
		self.LONG.setDisabled(False)

	############################### ADD PROBLEM ################################
	def add_problem_client(self):
		no = manage_local_ids.get_new_id()
		self.client_config["No_of_Problems"] = int(no)
		self.data = read_write.read_json()
		self.window = add_problem_ui(no,self.table_model,self.client_config,self.data)
		self.window.show()

	############################## EDIT PROBLEM ###############################
	def edit_problem_client(self, selected_row):
		no = self.table_model.index(selected_row, 0).data()
		name = self.table_model.index(selected_row, 2).data()
		code = self.table_model.index(selected_row, 3).data()
		self.window = edit_problem_ui(no,name,code,self.table_model,self.client_config)
		self.window.show()

	############################# RESET PROBLEM ################################

	def confirm_event(self):
		message = "Pressing 'Yes' will DELETE all Problems.\nAre you sure you want to delete?"
		detail_message = "You may lose all data. "

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

		button_yes.setStyleSheet(open('Elements/style.qss', "r").read())
		button_no.setStyleSheet(open('Elements/style.qss', "r").read())

		custom_close_box.exec_()

		if custom_close_box.clickedButton() == button_yes:
			self.reset_problem_client()
		elif custom_close_box.clickedButton() == button_no:
			pass

	def reset_problem_client(self):
		read_write.write_json(self.data)
		reset_database.reset_problem(self.table_model)
		manage_local_ids.initialize_local_id()
		for i in os.listdir('./Problems/'):
			os.system('rm -rf ./Problems/' + i)

	############################ SAVE CONTEST TAB ##############################
	def save_contest_tab(self):
		if self.contest_name_text.text() == '':
			QMessageBox.warning(self,'Message','Contest Name cannot be empty')
		elif self.contest_theme_text.text() == '':
			QMessageBox.warning(self,'Message','Contest Theme cannot be empty')
		elif self.client_key_text.text() == '':
			QMessageBox.warning(self,'Message','Client Key cannot be empty')
		else:
			self.client_config["Contest_Name"] = self.contest_name_text.text()
			self.client_config["Contest_Theme"] = self.contest_theme_text.text()
			self.client_config["client_key"] = self.client_key_text.text()
			with open("../Client/config.json", 'w') as contest:
				json.dump(self.client_config, contest, indent = 4)
			self.contest_name_text.setReadOnly(True)
			self.contest_theme_text.setReadOnly(True)
			self.client_key_text.setReadOnly(True)
			self.contest_duration_text.setReadOnly(True)
			self.start_time_text.setReadOnly(True)
			self.am_pm.setEnabled(False)
			self.hour_12.setEnabled(False)
			self.hour_24.setEnabled(False)
			QMessageBox.warning(self,'Message','Contest Details has been saved')

	########################## EDIT CONTEST TAB #################################
	def edit_contest_tab(self):
		self.contest_name_text.setReadOnly(False)
		self.contest_theme_text.setReadOnly(False)
		self.client_key_text.setReadOnly(False)
		self.contest_duration_text.setReadOnly(False)
		self.start_time_text.setReadOnly(False)
		self.am_pm.setEnabled(True)
		self.hour_12.setEnabled(True)
		self.hour_24.setEnabled(True)

	######################### SELECT AM OR PM ###################################
	def select_format(self,button):
		if button.text() == '12 Hour':
			if button.isChecked() == True:
				self.am_pm.setEnabled(True)
				self.start_time_text.setText('')
				self.start_time_text.setPlaceholderText('12 Hour - HH:MM:SS')
		else:
			if button.isChecked() == True:
				self.am_pm.setEnabled(False)
				self.start_time_text.setText('')
				self.start_time_text.setPlaceholderText('24 Hour - HH:MM:SS')

	#################### SELECT ALL LANGUAGE OR MANUAL #####################

	def select_language_base(self,button):
		if button.text() == 'Select All':
			if button.isChecked() == True:
				self.c.setChecked(True)
				self.cplusplus.setChecked(True)
				self.python2.setChecked(True)
				self.python3.setChecked(True)
				self.java.setChecked(True)
				self.general.setChecked(True)
				self.c.setDisabled(True)
				self.cplusplus.setDisabled(True)
				self.python2.setDisabled(True)
				self.python3.setDisabled(True)
				self.java.setDisabled(True)
				self.general.setDisabled(True)
				self.language_tuple = "('C','C++','PYTHON-2','PYTHON-3','JAVA','TEXT')"
				
		else:
			if button.isChecked() == True:
				self.c.setChecked(False)
				self.cplusplus.setChecked(False)
				self.python2.setChecked(False)
				self.python3.setChecked(False)
				self.java.setChecked(False)
				self.general.setChecked(False)
				self.c.setEnabled(True)
				self.cplusplus.setEnabled(True)
				self.python2.setEnabled(True)
				self.python3.setEnabled(True)
				self.java.setEnabled(True)
				self.general.setEnabled(True)


	########################### SAVE RABBITMQ DETAILS FOR CLIENT ###########################
	def save_client_rabbitmq(self):
		if self.rabbitmq_username_text.text() == '':
			QMessageBox.warning(self,'Message','USERNAME cannot be empty')
		elif self.rabbitmq_password_text.text() == '':
			QMessageBox.warning(self,'Message','PASSWORD cannot be empty')
		elif self.rabbitmq_host_text.text() == '':
			QMessageBox.warning(self,'Message','HOST cannot be empty')
		else:
			self.rabbitmq_username_text.setReadOnly(True)
			self.rabbitmq_password_text.setReadOnly(True)
			self.rabbitmq_host_text.setReadOnly(True)
			self.manual.setDisabled(True)
			self.automatic.setDisabled(True)
			self.client_config["rabbitmq_username"] = self.rabbitmq_username_text.text()
			self.client_config["rabbitmq_password"] = self.rabbitmq_password_text.text()
			self.client_config["host"] = self.rabbitmq_host_text.text()
			QMessageBox.warning(self,'Message','RabbitMQ Details has been saved')

	def save_server_rabbitmq(self):
		pass

	def save_judge_rabbitmq(self):
		pass

	########################## EDIT RABBITMQ DETAILS FOR CLIENT ############################
	def edit_client_rabbitmq(self):
		self.rabbitmq_username_text.setReadOnly(False)
		self.rabbitmq_password_text.setReadOnly(False)
		self.rabbitmq_host_text.setReadOnly(False)
		self.manual.setEnabled(True)
		self.automatic.setEnabled(True)


	def edit_server_rabbitmq(self):
		pass


	def edit_judge_rabbitmq(self):
		pass


	########################### SAVE LANGUAGE DETAILS FOR CLIENT ###########################
	def save_client_language(self):
		if self.all.isChecked() == True:
			self.client_config["Languages"] = self.language_tuple
		else:
			language_list = []
			if self.c.isChecked() == True:
				language_list.append('C')
			if self.cplusplus.isChecked() == True:
				language_list.append('C++')
			if self.python2.isChecked() == True:
				language_list.append('PYTHON-2')
			if self.python3.isChecked() == True:
				language_list.append('PYTHON-3')
			if self.java.isChecked() == True:
				language_list.append('JAVA')
			if self.general.isChecked() == True:
				language_list.append('TEXT')
			self.language_tuple = str(tuple(language_list))
			self.client_config["Languages"] = self.language_tuple
		print(self.client_config)
		self.c.setDisabled(True)
		self.cplusplus.setDisabled(True)
		self.python2.setDisabled(True)
		self.python3.setDisabled(True)
		self.java.setDisabled(True)
		self.general.setDisabled(True)
		self.all.setDisabled(True)
		self.some.setDisabled(True)

	########################### EDIT LANGUAGE DETAILS FOR CLIENT ###########################
	def edit_client_language(self):
		self.c.setEnabled(True)
		self.cplusplus.setEnabled(True)
		self.python2.setEnabled(True)
		self.python3.setEnabled(True)
		self.java.setEnabled(True)
		self.general.setEnabled(True)
		self.all.setEnabled(True)
		self.some.setEnabled(True)

	########################## FETCH IP ADDRESS AUTOMATICALLY ################################
	def get_ip_address(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		return s.getsockname()[0]

	################################## BUTTON STATE SIGNAL ###################################
	def button_state(self,button):
		if button.text() == 'Manual IP':
			if button.isChecked() == True:
				self.rabbitmq_host_text.setReadOnly(False)
				self.rabbitmq_host_text.setText('')
				self.rabbitmq_host_text.setPlaceholderText('Example : 127.0.0.1')
		else:
			if button.isChecked() == True:
				ip = self.get_ip_address()
				self.rabbitmq_host_text.setText(ip)
				self.rabbitmq_host_text.setReadOnly(True)


	def button_state_server(self,button):
		if button.text() == 'Manual IP':
			if button.isChecked() == True:
				self.rabbitmq_server_host_text.setReadOnly(False)
				self.rabbitmq_server_host_text.setText('')
				self.rabbitmq_server_host_text.setPlaceholderText('Example : 127.0.0.1')
		else:
			if button.isChecked() == True:
				ip = self.get_ip_address()
				self.rabbitmq_server_host_text.setText(ip)
				self.rabbitmq_server_host_text.setReadOnly(True)


	def button_state_judge(self,button):
		if button.text() == 'Manual IP':
			if button.isChecked() == True:
				self.rabbitmq_judge_host_text.setReadOnly(False)
				self.rabbitmq_judge_host_text.setText('')
				self.rabbitmq_judge_host_text.setPlaceholderText('Example : 127.0.0.1')
		else:
			if button.isChecked() == True:
				ip = self.get_ip_address()
				self.rabbitmq_judge_host_text.setText(ip)
				self.rabbitmq_judge_host_text.setReadOnly(True)


	def rank_state(self,button):
		if button.text() == 'IOI System':
			if button.isChecked() == True:
				self.ac_text.setText('100')
				self.penalty_points_text.setText('-20')
				self.penalty_time_text.setText('20')
				self.ac_text.setReadOnly(True)
				self.penalty_points_text.setReadOnly(True)
				self.penalty_time_text.setReadOnly(True)
		elif button.text() == 'ACM System':
			if button.isChecked() == True:
				self.ac_text.setText('100')
				self.penalty_points_text.setText('-20')
				self.penalty_time_text.setText('20')
				self.ac_text.setReadOnly(True)
				self.penalty_points_text.setReadOnly(True)
				self.penalty_time_text.setReadOnly(True)
		else:
			if button.isChecked() == True:
				self.ac_text.setText('100')
				self.penalty_points_text.setText('0')
				self.penalty_time_text.setText('0')
				self.ac_text.setReadOnly(True)
				self.penalty_points_text.setReadOnly(True)
				self.penalty_time_text.setReadOnly(True)


	def call_gui(self):
		pass


	################################ GENERATE DATABASE VIEW  #######################################
	def generate_view(self,model):
		table = QTableView() 
		table.setModel(model)
		# Enable sorting in the table view 
		table.setSortingEnabled(True)
		# Enable alternate row colors for readability
		table.setAlternatingRowColors(True)
		# Select whole row when clicked
		table.setSelectionBehavior(QAbstractItemView.SelectRows)
		# Allow only one row to be selected 
		table.setSelectionMode(QAbstractItemView.SingleSelection)
		# fit view to whole space 
		table.resizeColumnsToContents()
		# Make table non editable
		table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		# Set view to delete when gui is closed
		table.setAttribute(Qt.WA_DeleteOnClose)

		horizontal_header = table.horizontalHeader()
		horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
		vertical_header = table.verticalHeader()
		# vertical_header.setSectionResizeMode(QHeaderView.Stretch)
		vertical_header.setVisible(False)
		return table

	################################ INITIALIZE DATABASE  #######################################
	def init_qt_database(self):
		try:
			db = QSqlDatabase.addDatabase('QSQLITE')
			db.setDatabaseName('client_setup.db')
			return db
		except Exception as Error:
			print('[ CRITICAL ] Database loading error......')
			print(str(Error))

	###################################### MODEL TABLE ##########################################
	def manage_models(self, db, table_name):
		if db.open():
			model = QSqlTableModel()
			model.setTable(table_name)
			model.setEditStrategy(QSqlTableModel.OnFieldChange)
			model.select()
		return model

	################################### CLOSE BUTTON CLICKED ####################################
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
		app.setStyleSheet(open('Elements/style.qss', "r").read())
		app.setStyle("Fusion")

		client_app = contest_setup()

		app.aboutToQuit.connect(self.closeEvent)

		client_app.showMaximized()

		app.exec_()

setup_window()
