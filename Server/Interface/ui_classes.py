from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import user_management

class ui_widgets:

	def accounts_ui(self):
		heading = QLabel('Manage Accounts')
		heading.setObjectName('main_screen_heading')

		create_accounts_button = QPushButton('Create Accounts', self)
		create_accounts_button.setFixedSize(200, 50)
		create_accounts_button.clicked.connect(self.create_accounts)
		create_accounts_button.setObjectName("topbar_button")

		delete_account_button = QPushButton('Delete Account', self)
		delete_account_button.setFixedSize(200, 50)
		delete_account_button.clicked.connect(lambda:self.delete_account(accounts_table.selectionModel().selectedRows()))
		delete_account_button.setObjectName("topbar_button")

		accounts_model = self.manage_models(self.db, 'accounts')
		accounts_model.setHeaderData(0, Qt.Horizontal, 'Username')
		accounts_model.setHeaderData(1, Qt.Horizontal, 'Password')
		accounts_model.setHeaderData(2, Qt.Horizontal, 'Type')
		accounts_table = self.generate_view(accounts_model)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(create_accounts_button)
		head_layout.addWidget(delete_account_button)
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)


		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(accounts_table)
		
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, accounts_model

	def submissions_ui(self):
		heading = QLabel('All Runs')
		heading.setObjectName('main_screen_heading')

		allow_submission_label = QLabel('Allow submissions : ')
		allow_submission_label.setObjectName('main_screen_content')

		submission_allowed_flag = self.check_submission_allowed()
		
		allow_submission_button = QCheckBox('')
		allow_submission_button.setFixedSize(30, 30)
		allow_submission_button.setChecked(submission_allowed_flag)
		allow_submission_button.stateChanged.connect(self.allow_submissions_handler)

		submission_model = self.manage_models(self.db, 'submissions')

		submission_model.setHeaderData(0, Qt.Horizontal, 'Run ID')
		submission_model.setHeaderData(1, Qt.Horizontal, 'Local ID')
		submission_model.setHeaderData(2, Qt.Horizontal, 'Client ID')
		submission_model.setHeaderData(3, Qt.Horizontal, 'Language')
		submission_model.setHeaderData(4, Qt.Horizontal, 'Source File')
		submission_model.setHeaderData(5, Qt.Horizontal, 'Problem Code')
		submission_model.setHeaderData(6, Qt.Horizontal, 'Status')
		submission_model.setHeaderData(7, Qt.Horizontal, 'Time')

		submission_table = self.generate_view(submission_model)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(allow_submission_label)
		head_layout.addWidget(allow_submission_button)
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(submission_table)
		main_layout.setStretch(0,5)
		main_layout.setStretch(1,95)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		main.show()
		return main, submission_model


	def client_ui(self):
		heading = QLabel('Connected Clients')
		heading.setObjectName('main_screen_heading')

		allow_login_label = QLabel('Allow Logins : ')
		allow_login_label.setObjectName('main_screen_content')

		login_allowed_flag = self.check_login_allowed()
		
		allow_login_button = QCheckBox('')
		allow_login_button.setFixedSize(30, 30)
		allow_login_button.setChecked(login_allowed_flag)
		allow_login_button.stateChanged.connect(self.allow_login_handler)

		client_model = self.manage_models(self.db, 'connected_clients')
		client_model.setHeaderData(0, Qt.Horizontal, 'Client ID')
		client_model.setHeaderData(1, Qt.Horizontal, 'Username')
		client_model.setHeaderData(2, Qt.Horizontal, 'Password')

		client_view = self.generate_view(client_model)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(allow_login_label)
		head_layout.addWidget(allow_login_button)
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		

		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(client_view)
		main_layout.setStretch(0,5)
		main_layout.setStretch(1,95)		

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, client_model

	def judge_ui(self):
		heading = QLabel('Manage Judges')
		heading.setObjectName('main_screen_heading')

		#judge_model = self.manage_models(self.db, )

		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def query_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('All Clarifications')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def leaderboard_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Leaderboard')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def problem_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Manage Problems')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def language_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Manage Languages')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def stats_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Server Stats')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def settings_ui(self):
		heading = QLabel('Server Settings')
		heading.setObjectName('main_screen_heading')

		# Contest Time Management
		## Contest Time Settings Label:
		contest_time_label = QLabel('Contest Time Settings:')
		contest_time_label.setObjectName('main_screen_sub_heading')

		# Set contest time 
		contest_time_layout = QHBoxLayout()
		contest_duration_label = QLabel('> Contest Duration :')
		contest_duration_label.setObjectName('main_screen_content')
		contest_duration_label.setFixedSize(200, 20)
		contest_time_entry = QLineEdit()
		contest_time_entry.setPlaceholderText('HH:MM')
		contest_time_entry.setFixedSize(100, 25)
		contest_time_layout.addWidget(contest_duration_label)
		contest_time_layout.addWidget(contest_time_entry)
		contest_time_layout.addStretch(1)
		contest_time_layout.setSpacing(5)
		contest_time_layout.setContentsMargins(5, 0, 10, 0)
		contest_time_widget = QWidget()
		contest_time_widget.setLayout(contest_time_layout)

		# Start, Stop, Pause contest
		set_button = QPushButton('Set')
		set_button.setFixedSize(70, 25)
		set_button.setObjectName('interior_button')
		#set_button.clicked.connect(self.contest_settings)
		start_button = QPushButton('Start', self)
		start_button.setFixedSize(70, 25)
		start_button.setObjectName('interior_button')
		#start_button.clicked.connect(self.contest_settings)
		pause_button = QPushButton('Pause', self)
		pause_button.setFixedSize(70, 25)
		pause_button.setObjectName('interior_button')
		#pause_button.clicked.connect(self.contest_settings)
		stop_button = QPushButton('Stop', self)
		stop_button.setFixedSize(70, 25)
		stop_button.setObjectName('interior_button')
		#stop_button.clicked.connect(self.contest_settings)
		
		
		contest_buttons_layout = QHBoxLayout()
		contest_buttons_layout.addWidget(set_button)
		contest_buttons_layout.addWidget(start_button)
		contest_buttons_layout.addWidget(pause_button)
		contest_buttons_layout.addWidget(stop_button)
		contest_buttons_layout.addStretch(1)
		contest_buttons_layout.setSpacing(10)
		contest_buttons_widget = QWidget()
		contest_buttons_widget.setLayout(contest_buttons_layout)

		time_management_layout = QVBoxLayout()
		time_management_layout.addWidget(contest_time_label)
		time_management_layout.addWidget(contest_time_widget)
		time_management_layout.addWidget(contest_buttons_widget)
		time_management_widget = QWidget()
		time_management_widget.setLayout(time_management_layout)
		time_management_widget.setObjectName('content_box')



		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(time_management_widget)
		main_layout.setSpacing(10)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def reports_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Generate Report')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def about_us_ui(self):
		head1 = QLabel('Made with <3 by team Bitwise')
		head1.setObjectName('about_screen_heading')
		head1.setAlignment(Qt.AlignCenter)

		head2 = QLabel('Guess what! The BitsOJ project is open source!!! ')
		head2.setObjectName('main_screen_content')
		head2.setAlignment(Qt.AlignCenter)

		head3 = QLabel('Contribute at https://github.com/peeesspee/BitsOJ')
		head3.setObjectName('main_screen_content')
		head3.setAlignment(Qt.AlignCenter)



		main_layout = QVBoxLayout()
		main_layout.addWidget(head1)
		main_layout.addWidget(head2)
		main_layout.addWidget(head3)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


class new_accounts_ui(QMainWindow):
	pwd_type = 'Random'
	client_no = 0
	judge_no = 0
	data_changed_flags = ''
	
	def __init__(self, data_changed_flags, parent=None):
		super(new_accounts_ui, self).__init__(parent)
		self.data_changed_flags = data_changed_flags
		self.setWindowTitle('Add new accounts')
		self.setFixedSize(300, 200)
		main = self.add_new_accounts_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)


		return

	def combo_box_data_changed(text):
		new_accounts_ui.pwd_type = str(text)

	def client_updater(text):
		new_accounts_ui.client_no = int(text)
		return
	def judge_updater(text):
		new_accounts_ui.judge_no = int(text)
		return

	def add_new_accounts_ui(self):
		label1 = QLabel('Clients')

		client_entry = QSpinBox()
		client_entry.setMinimum(0)
		client_entry.setMaximum(500)
		client_entry.valueChanged.connect(new_accounts_ui.client_updater)
		
		# client_entry.textEdited.connect(new_accounts_ui.client_updater)
		# client_entry.setInputMask('9000')

		label2 = QLabel('Judges')

		judge_entry = QSpinBox()
		judge_entry.setMinimum(0)
		judge_entry.setMaximum(10)
		judge_entry.valueChanged.connect(new_accounts_ui.judge_updater)
		# judge_entry.textEdited.connect(new_accounts_ui.judge_updater)
		# judge_entry.setInputMask('9000')

		label3 = QLabel('Password Type:')

		password_type_entry = QComboBox()
		password_type_entry.addItem('Random')
		password_type_entry.addItem('Easy')
		password_type_entry.activated[str].connect(new_accounts_ui.combo_box_data_changed)

		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(200, 50)
		confirm_button.clicked.connect(lambda:new_accounts_ui.final_account_status(self))
		confirm_button.setDefault(True)
		
		
		layout = QGridLayout()
		layout.addWidget(label1, 0, 0)
		label1.setStyleSheet('''Qlabel{text-align : center; }''')
		layout.addWidget(client_entry, 0, 1)
		layout.addWidget(label2, 1, 0)
		layout.addWidget(judge_entry, 1, 1)
		layout.addWidget(label3, 2, 0)
		layout.addWidget(password_type_entry, 2, 1)


		layout.setColumnMinimumWidth(0,50)
		layout.setColumnMinimumWidth(1,50)
		layout.setColumnStretch(0, 1)
		layout.setColumnStretch(1, 1)
		layout.setRowStretch(0, 1)
		layout.setRowStretch(1, 1)
		layout.setVerticalSpacing(10)
		upper_widget = QWidget()
		upper_widget.setLayout(layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(upper_widget)
		main_layout.addWidget(confirm_button)
		
		main = QWidget()
		main.setLayout(main_layout)

		label1.setObjectName('account_label')
		label2.setObjectName('account_label')
		label3.setObjectName('account_label')
		client_entry.setObjectName('account_spinbox')
		judge_entry.setObjectName('account_spinbox')
		password_type_entry.setObjectName('account_combobox')
		confirm_button.setObjectName('account_button')
		main.setObjectName('account_window')
		
		return main
		
	def final_account_status(self):
		user_management.generate_n_users(new_accounts_ui.client_no, new_accounts_ui.judge_no, new_accounts_ui.pwd_type)
		# Reset the critical section flag
		self.data_changed_flags[4] = 0
		# Indicate new insertions in accounts
		self.data_changed_flags[5] = 1
		self.close()

 