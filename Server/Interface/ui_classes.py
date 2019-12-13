from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import user_management, query_management, client_authentication, submissions_management
import json 
import ast

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
		delete_account_button.clicked.connect(
			lambda:self.delete_account(accounts_table.selectionModel().selectedRows())
			)
		delete_account_button.setObjectName("topbar_button")
		delete_account_button.setToolTip('Delete account.\nCan be used when contest is \nnot RUNNING')

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
		return main, accounts_model, delete_account_button

	def submissions_ui(self):
		heading = QLabel('All Runs')
		heading.setObjectName('main_screen_heading')

		# TODO
		manual_review_flag = self.check_manual_review_allowed()
		manual_review_label = QLabel('Manual Review')
		manual_review_label.setObjectName('main_screen_content')
		manual_review_label.setToolTip(
			'Review each submission before updating Leaderboard\nand sending client response.\nUse only when necessary!'
		)
		manual_review_button = QCheckBox('')
		manual_review_button.setFixedSize(30, 30)
		manual_review_button.setChecked(manual_review_flag)
		manual_review_button.stateChanged.connect(self.manual_reviews_handler)

		submission_allowed_flag = self.check_submission_allowed()
		allow_submission_label = QLabel('Allow Submissions')
		allow_submission_label.setObjectName('main_screen_content')
		allow_submission_label.setToolTip('Allow/Disallow client submissions.')
		allow_submission_button = QCheckBox('')
		allow_submission_button.setFixedSize(30, 30)
		allow_submission_button.setChecked(submission_allowed_flag)
		allow_submission_button.stateChanged.connect(self.allow_submissions_handler)

		edit_submission_button = QPushButton('Review', self)
		edit_submission_button.setFixedSize(200, 50)
		edit_submission_button.clicked.connect(
			lambda:self.manage_submission(submission_table.selectionModel().currentIndex().row())
		)
		edit_submission_button.setObjectName("topbar_button")
		edit_submission_button.setToolTip('Review selected submission')

		submission_model = self.manage_submissions_model(self.db, 'submissions')

		# run_id, client_id, problem_code, language, timestamp, verdict, sent_status
	
		submission_model.setHeaderData(0, Qt.Horizontal, 'Run ID')
		submission_model.setHeaderData(1, Qt.Horizontal, 'Client ID')
		submission_model.setHeaderData(2, Qt.Horizontal, 'Problem Code')
		submission_model.setHeaderData(3, Qt.Horizontal, 'Language')
		submission_model.setHeaderData(4, Qt.Horizontal, 'Time')
		submission_model.setHeaderData(5, Qt.Horizontal, 'Verdict')
		submission_model.setHeaderData(6, Qt.Horizontal, 'Status')
		submission_model.setHeaderData(7, Qt.Horizontal, 'Judge')
		
		submission_table = self.generate_view(submission_model)
		submission_table.setSortingEnabled(False)
		submission_table.doubleClicked.connect(
			lambda:self.manage_submission(submission_table.selectionModel().currentIndex().row())
		)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(manual_review_label)
		head_layout.addWidget(manual_review_button)
		head_layout.addWidget(allow_submission_label)
		head_layout.addWidget(allow_submission_button)
		head_layout.addWidget(edit_submission_button)
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 5)
		head_layout.setStretch(2, 5)
		head_layout.setStretch(3, 5)
		head_layout.setStretch(4, 5)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(submission_table)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		main.show()
		return main, submission_model, allow_submission_button


	def client_ui(self):
		client_model = self.manage_models(self.db, 'connected_clients')
		client_model.setHeaderData(0, Qt.Horizontal, 'Client ID')
		client_model.setHeaderData(1, Qt.Horizontal, 'Username')
		client_model.setHeaderData(2, Qt.Horizontal, 'Password')
		client_model.setHeaderData(3, Qt.Horizontal, 'State')
		client_view = self.generate_view(client_model)

		client_view.doubleClicked.connect(
			lambda:self.edit_client(client_view.selectionModel().currentIndex().row())
		)

		heading = QLabel('Connected Clients')
		heading.setObjectName('main_screen_heading')

		allow_login_label = QLabel('Allow Logins : ')
		allow_login_label.setObjectName('main_screen_content')

		login_allowed_flag = self.check_login_allowed()
		
		allow_login_button = QCheckBox('')
		allow_login_button.setFixedSize(30, 30)
		allow_login_button.setChecked(login_allowed_flag)
		allow_login_button.stateChanged.connect(self.allow_login_handler)

		edit_client_button = QPushButton('Edit Client', self)
		edit_client_button.setFixedSize(200, 50)
		edit_client_button.clicked.connect(
			lambda:self.edit_client(client_view.selectionModel().currentIndex().row())
		)
		edit_client_button.setObjectName("topbar_button")
		edit_client_button.setToolTip('Change client status.')

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(allow_login_label)
		head_layout.addWidget(allow_login_button)
		head_layout.addWidget(edit_client_button)
		head_layout.setStretch(0, 70)
		head_layout.setStretch(1, 5)
		head_layout.setStretch(2, 5)
		head_layout.setStretch(3, 20)
		
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(client_view)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)		

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, client_model, allow_login_button

	def judge_ui(self):
		heading = QLabel('Manage Judges')
		heading.setObjectName('main_screen_heading')

		allow_login_label = QLabel('Allow Judge Logins : ')
		allow_login_label.setObjectName('main_screen_content')

		login_allowed_flag = self.check_judge_login_allowed()
		
		allow_login_button = QCheckBox('')
		allow_login_button.setFixedSize(30, 30)
		allow_login_button.setChecked(login_allowed_flag)
		allow_login_button.stateChanged.connect(self.allow_judge_login_handler)

		judge_model = self.manage_models(self.db, 'connected_judges')
		judge_model.setHeaderData(0, Qt.Horizontal, 'Judge ID')
		judge_model.setHeaderData(1, Qt.Horizontal, 'Username')
		judge_model.setHeaderData(2, Qt.Horizontal, 'Password')
		judge_model.setHeaderData(3, Qt.Horizontal, 'State')

		judge_view = self.generate_view(judge_model)

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
		main_layout.addWidget(judge_view)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)		

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, judge_model



	def query_ui(self):
		heading = QLabel('All Clarifications')
		heading.setObjectName('main_screen_heading')

		reply_button = QPushButton('Reply')
		reply_button.setFixedSize(200, 50)
		reply_button.clicked.connect(
			lambda: self.query_reply(query_view.selectionModel().currentIndex().row())
			)
		reply_button.setObjectName("topbar_button")

		query_model = self.manage_models(self.db, 'queries')
		query_model.setHeaderData(0, Qt.Horizontal, 'Query ID')
		query_model.setHeaderData(1, Qt.Horizontal, 'Client ID')
		query_model.setHeaderData(2, Qt.Horizontal, 'Query')
		query_model.setHeaderData(3, Qt.Horizontal, 'Response')

		query_view = self.generate_view(query_model)
		query_view.doubleClicked.connect(
			lambda:self.query_reply(query_view.selectionModel().currentIndex().row())
		)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(reply_button)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(query_view)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)	
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, query_model


	def leaderboard_ui(self):
		heading = QLabel('Contest Standings')
		heading.setObjectName('main_screen_heading')

		scoring_num = self.data_changed_flags[17]
		if scoring_num == 1:
			# ACM Style ranking
			scoring_type = 'ACM'
		elif scoring_num == 2:
			# IOI Style ranking
			scoring_type = 'IOI'
		else:
			scoring_type = 'LONG'

		scoring_label = QLabel('Scoring Type: ' + scoring_type)

		update_scoreboard_label = QLabel('Broadcast Scoreboard : ')
		update_scoreboard_label.setObjectName('main_screen_content')

		update_scoreboard_flag = self.check_scoreboard_update_allowed()
		
		update_scoreboard_button = QCheckBox('')
		update_scoreboard_button.setFixedSize(30, 30)
		update_scoreboard_button.setChecked(update_scoreboard_flag)
		update_scoreboard_button.stateChanged.connect(self.allow_scoreboard_update_handler)

		score_model = self.manage_leaderboard_model(self.db, 'scoreboard')

		score_model.setHeaderData(0, Qt.Horizontal, 'Client ID')
		score_model.setHeaderData(1, Qt.Horizontal, 'Team')
		score_model.setHeaderData(2, Qt.Horizontal, 'Score')
		score_model.setHeaderData(3, Qt.Horizontal, 'Problems Solved')
		score_model.setHeaderData(4, Qt.Horizontal, 'Total Time')
		
		score_table = self.generate_view(score_model)
		score_table.setSortingEnabled(False)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(scoring_label)
		head_layout.addWidget(update_scoreboard_label)
		head_layout.addWidget(update_scoreboard_button)
		head_layout.setStretch(0, 40)
		head_layout.setStretch(1, 40)
		head_layout.setStretch(2, 10)
		head_layout.setStretch(3, 10)
		
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(score_table)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		scoring_label.setObjectName('main_screen_content')
		main.show()
		return main, score_model, scoring_label


	# def problem_ui(self):
	# 	main_layout = QVBoxLayout()
	# 	heading = QLabel('Manage Problems')
	# 	heading.setObjectName('main_screen_heading')
	# 	# This is the dictionary which contains all problems in the format:
	# 	# ProblemName, Code, TimeLimit, NoOfTestFiles
	# 	try:
	# 		problem_dict = self.config["Problems"]
	# 		no_of_problems = int(self.config["Number Of Problems"])
	# 		# Problems in the dict are in format "Problem i" where
	# 		# 1<= i <= no_of_problems
	# 		problem_tabs = QTabWidget()
	# 		problem_tabs.setObjectName('main_tabs')
	# 		problem_tabbar = QTabBar()
	# 		problem_tabbar.setObjectName('problem_tabs')

	# 		for i in range(1, no_of_problems + 1):
	# 			problem_str = problem_dict['Problem ' + str(i)]
	# 			problem_tuple = eval(problem_str)

	# 			widget = ui_widgets.get_problem_ui(
	# 				self,
	# 				problem_tuple[0], 
	# 				problem_tuple[1], 
	# 				problem_tuple[2], 
	# 				problem_tuple[3]
	# 			)
	# 			problem_tabs.addTab(widget, '')
	# 			problem_tabbar.addTab('Problem ' + str(i))	

	# 		problem_tabs.setTabBar(problem_tabbar)
	# 		main_layout.addWidget(heading)
	# 		main_layout.addWidget(problem_tabs)
	# 		main_layout.setStretch(0,10)
	# 		main_layout.setStretch(1,90)
			
	# 	except Exception as error:
	# 		print("[ ERROR ]" + str(error))
		
	# 	main = QWidget()
	# 	main.setLayout(main_layout)
	# 	main.setObjectName("main_screen");
	# 	return main

	def problem_ui(self):
		heading = QLabel('Manage Problems')
		heading.setObjectName('main_screen_heading')

		view_problem_button = QPushButton('View Problem', self)
		view_problem_button.setFixedSize(200, 50)
		view_problem_button.clicked.connect(
			lambda:self.view_problem(problem_table.selectionModel().currentIndex().row())
		)
		view_problem_button.setObjectName("topbar_button")

		delete_problem_button = QPushButton('Delete Problem', self)
		delete_problem_button.setFixedSize(200, 50)
		# delete_problem_button.clicked.connect(
		# 	lambda:self.delete_problem(problem_table.selectionModel().selectedRows())
		# )
		delete_problem_button.setObjectName("topbar_button")
		

		problem_model = self.manage_models(self.db, 'problems')
		problem_model.setHeaderData(0, Qt.Horizontal, 'Problem Name')
		problem_model.setHeaderData(1, Qt.Horizontal, 'Code')
		problem_model.setHeaderData(2, Qt.Horizontal, 'Test Files')
		problem_model.setHeaderData(3, Qt.Horizontal, 'Time Limit')
		problem_table = self.generate_view(problem_model)
		problem_table.doubleClicked.connect(
			lambda:self.view_problem(problem_table.selectionModel().currentIndex().row())
		)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(view_problem_button)
		head_layout.addWidget(delete_problem_button)
		
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)


		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(problem_table)
		
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, problem_model
		
	def get_stats_widget():
		contest_problems_subheading = QLabel('Problems: ')

		contest_problems_number = QLabel('Number of Problems: ')
		contest_problems_number_answer = QLabel('')	# Label Index 2
		contest_problems_layout = QHBoxLayout()
		contest_problems_layout.addWidget(contest_problems_number)
		contest_problems_layout.addWidget(contest_problems_number_answer)
		contest_problems_layout.addStretch(1)
		contest_problems_number_widget = QWidget()
		contest_problems_number_widget.setLayout(contest_problems_layout)

		participants_number = QLabel('Number of Teams with 1 or more submissions: ')
		participants_number_answer = QLabel('')	# Label Index 4
		participants_layout = QHBoxLayout()
		participants_layout.addWidget(participants_number)
		participants_layout.addWidget(participants_number_answer)
		participants_layout.addStretch(1)
		participants_number_widget = QWidget()
		participants_number_widget.setLayout(participants_layout)

		participants_pro_number = QLabel('Number of Teams with 1 or more Correct submissions: ')
		participants_pro_number_answer = QLabel('')	# Label Index 6
		participants_pro_layout = QHBoxLayout()
		participants_pro_layout.addWidget(participants_pro_number)
		participants_pro_layout.addWidget(participants_pro_number_answer)
		participants_pro_layout.addStretch(1)
		participants_pro_number_widget = QWidget()
		participants_pro_number_widget.setLayout(participants_pro_layout)

		problem_solved_table = QTableWidget()
		problem_solved_table.setColumnCount(4)
		problem_solved_table.setHorizontalHeaderLabels(
			("Problem", "Correct Submissions", "Total Submissions", "Accuracy")
		)

		problem_solved_table.resizeColumnsToContents()
		problem_solved_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		problem_solved_table.setAlternatingRowColors(True)
		problem_solved_table.setFixedSize(800, 180)
		vertical_header = problem_solved_table.verticalHeader()
		vertical_header.setVisible(False)
		horizontal_header = problem_solved_table.horizontalHeader()
		horizontal_header.setSectionResizeMode(QHeaderView.Stretch)

		main_layout = QVBoxLayout()
		main_layout.addWidget(contest_problems_subheading)
		main_layout.addWidget(contest_problems_number_widget)
		main_layout.addWidget(participants_number_widget)
		main_layout.addWidget(participants_pro_number_widget)
		main_layout.addWidget(problem_solved_table)
		main_layout.addStretch(1)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName('content_box')
		contest_problems_subheading.setObjectName('main_screen_sub_heading')
		contest_problems_number.setObjectName('main_screen_content')
		contest_problems_number_answer.setObjectName('main_screen_content')
		participants_number.setObjectName('main_screen_content')
		participants_number_answer.setObjectName('main_screen_content')
		participants_pro_number.setObjectName('main_screen_content')
		participants_pro_number_answer.setObjectName('main_screen_content')
		problem_solved_table.setObjectName('inner_table')
		return main

	def update_stats(self, stats_widget):
		accuracy = 0
		child_list = stats_widget.findChildren(QLabel)
		table_list = stats_widget.findChildren(QTableWidget)
		# 2nd QLabel in this list is contest_problems_number_answer
		number_of_problems = self.config['Number Of Problems']
		child_list[2].setText(number_of_problems)
		number_of_problems = int(number_of_problems)

		# table_list[0] contains problem_solved_table
		table_list[0].setRowCount(int(number_of_problems))
		code_tuple_string = self.config['Problem Codes']
		code_tuple = eval(code_tuple_string)
		for i in range(0, number_of_problems ):

			table_list[0].setItem(i, 0, QTableWidgetItem(code_tuple[i]))
			# Get how many clients solved this problem
			solve_count = user_management.get_ac_count(code_tuple[i])
			table_list[0].setItem(i, 1, QTableWidgetItem(str(solve_count)))

			# Get how many clients submitted a code for this problem
			submit_count = user_management.get_submission_count(code_tuple[i])
			table_list[0].setItem(i, 2, QTableWidgetItem(str(submit_count)))

			if submit_count == 0:
				accuracy = '{0:.2f}'.format(0)
			else:
				accuracy = float(solve_count*100/submit_count)
				accuracy = '{0:.2f}'.format(accuracy)
			table_list[0].setItem(i, 3, QTableWidgetItem(str(accuracy) + "%"))

		# Get number of active participants
		participant_count = user_management.get_participant_count()
		child_list[4].setText(str(participant_count))

		# Get number of active pro participants
		participant_pro_count = user_management.get_participant_pro_count()
		child_list[6].setText(str(participant_pro_count))

		# Get Accuracy

		return

	def stats_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Contest Stats')
		heading.setObjectName('main_screen_heading')

		stats_widget = ui_widgets.get_stats_widget()

		update_button = QPushButton('Update Stats')
		update_button.clicked.connect(
			lambda:ui_widgets.update_stats(self, stats_widget)
		)
		update_button.setFixedSize(200, 50)

		top_layout = QHBoxLayout()
		top_layout.addWidget(heading)
		top_layout.addWidget(update_button)
		top_layout.setStretch(0, 80)
		top_layout.setStretch(1, 20)
		top_widget = QWidget()
		top_widget.setLayout(top_layout)

		main_layout.addWidget(top_widget)
		main_layout.addWidget(stats_widget)
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		update_button.setObjectName('topbar_button')
		# Update stats UI first time
		ui_widgets.update_stats(self, stats_widget)
		return main

	def time_limit_updater(self, text):
		print('[ SETTING ] Contest submission time limit set to: ' + str(text) + ' minutes.')
		self.data_changed_flags[21] = int(text)
		return

	def contest_time_settings(self):
		# Contest Time Management
		## Contest Time Settings Label:
		contest_time_label = QLabel('Contest Time Settings:')
		contest_time_label.setObjectName('main_screen_sub_heading')

		# Set contest time 
		contest_duration_label = QLabel('> Contest Duration: ')
		contest_duration_label.setObjectName('main_screen_content')
		contest_duration_label.setFixedSize(200, 20)

		contest_time_entry = QLineEdit()
		contest_time_entry.setText(self.config["Contest Duration"])
		contest_time_entry.setPlaceholderText('HH:MM:SS')
		contest_time_entry.setFixedSize(80, 30)
		contest_time_entry.setToolTip('You will not be able to edit this when contest starts.')

		contest_time_layout = QHBoxLayout()
		contest_time_layout.addWidget(contest_duration_label)
		contest_time_layout.addWidget(contest_time_entry)
		contest_time_layout.addStretch(1)
		contest_time_layout.setSpacing(5)
		contest_time_layout.setContentsMargins(5, 0, 10, 0)
		contest_time_widget = QWidget()
		contest_time_widget.setLayout(contest_time_layout)

		contest_extension_label = QLabel("> Extend/Shorten contest by: ")
		contest_extension_label.setObjectName('main_screen_content')
		minutes_label = QLabel(" Minutes")
		minutes_label.setObjectName('main_screen_content')

		change_time_entry = QSpinBox()
		change_time_entry.setMinimum(0)
		change_time_entry.setMaximum(60)
		change_time_entry.setValue(0)
		change_time_entry.setReadOnly(True)
		change_time_entry.setToolTip('You will be able to use it when contest is STARTED')

		change_time_layout = QHBoxLayout()
		change_time_layout.addWidget(contest_extension_label)
		change_time_layout.addWidget(change_time_entry)
		change_time_layout.addWidget(minutes_label)
		change_time_layout.addStretch(1)
		change_time_layout.setSpacing(5)
		change_time_layout.setContentsMargins(5, 0, 10, 0)
		change_time_widget = QWidget()
		change_time_widget.setLayout(change_time_layout)

		submission_limit_label = QLabel('> Submission Limit: ')
		submission_limit_label.setObjectName('main_screen_content')
		submission_limit_label.setToolTip(
			'Set Time limit before a Client\nis allowed to send a new solution.'
			+
			'\nIncrease this when Server is under load'
		)
		submission_limit = QSpinBox()
		submission_limit.setMinimum(0)
		submission_limit.setMaximum(5)
		submission_limit.setToolTip('Increase/Decrease works instantly.')
		submission_limit.valueChanged.connect(
			lambda:ui_widgets.time_limit_updater(self, submission_limit.text())
		)
		minutes1_label = QLabel(" Minutes")
		minutes1_label.setObjectName('main_screen_content')
		submission_limit_layout = QHBoxLayout()
		submission_limit_layout.addWidget(submission_limit_label)
		submission_limit_layout.addWidget(submission_limit)
		submission_limit_layout.addWidget(minutes1_label)
		submission_limit_layout.addStretch(1)
		submission_limit_widget = QWidget()
		submission_limit_widget.setLayout(submission_limit_layout)

		# Start, Stop, Pause contest
		set_button = QPushButton('Set')
		set_button.setFixedSize(70, 25)
		set_button.setObjectName('interior_button')
		set_button.setToolTip('Set contest time.\nThis does NOT broadcast to clients.')
		set_button.clicked.connect(
			lambda: ui_widgets.preprocess_contest_broadcasts(self, 'SET', contest_time_entry.text())
			)

		start_button = QPushButton('Start', self)
		start_button.setFixedSize(70, 25)
		start_button.setObjectName('interior_button')
		start_button.setToolTip('START the contest and broadcast to all clients.')
		start_button.clicked.connect(
			lambda: ui_widgets.preprocess_contest_broadcasts(self, 'START', contest_time_entry.text())
			)

		update_button = QPushButton('Update', self)
		update_button.setEnabled(False)
		update_button.setFixedSize(70, 25)
		update_button.setObjectName('interior_button')
		update_button.setToolTip(
			'UPDATE contest time and broadcast to all clients.\nDisabled until contest Starts'
			)
		update_button.clicked.connect(
			lambda: ui_widgets.preprocess_contest_broadcasts(self, 'UPDATE', change_time_entry.value())
			)

		stop_button = QPushButton('Stop', self)
		stop_button.setEnabled(False)
		stop_button.setFixedSize(70, 25)
		stop_button.setObjectName('interior_button')
		stop_button.setToolTip(
			'STOP the contest and broadcast to all clients.\nDisabled until contest Starts'
			)
		stop_button.clicked.connect(
			lambda: ui_widgets.preprocess_contest_broadcasts(self, 'STOP')
			)
		
		contest_buttons_layout = QHBoxLayout()
		contest_buttons_layout.addWidget(set_button)
		contest_buttons_layout.addWidget(start_button)
		contest_buttons_layout.addWidget(update_button)
		contest_buttons_layout.addWidget(stop_button)

		contest_buttons_layout.addStretch(1)
		contest_buttons_layout.setSpacing(10)
		contest_buttons_widget = QWidget()
		contest_buttons_widget.setLayout(contest_buttons_layout)

		time_management_layout = QVBoxLayout()
		time_management_layout.addWidget(contest_time_label)
		time_management_layout.addWidget(contest_time_widget)
		time_management_layout.addWidget(change_time_widget)
		time_management_layout.addWidget(submission_limit_widget)
		time_management_layout.addWidget(contest_buttons_widget)
		time_management_widget = QWidget()
		time_management_widget.setLayout(time_management_layout)
		time_management_widget.setObjectName('content_box')
		return (
			time_management_widget, contest_time_entry, change_time_entry, 
			set_button, start_button, update_button, stop_button
			)

	def preprocess_contest_broadcasts(self, signal, extra_data = 'NONE'):
		#process_event() is defined in interface package
		if signal == 'SET':
			#Validate extra data to be time
			if ui_widgets.validate_date(self, extra_data) == True:
				self.process_event('SET', extra_data)
			else:
				return
		elif signal == 'START':
			#Validate extra data to be time
			if ui_widgets.validate_date(self, extra_data) == True:
				self.process_event('START', extra_data)	
			else:
				return
			
		elif signal == 'UPDATE':
			status = self.password_verification()
			if status == 1:
				self.process_event('UPDATE', extra_data)
			elif status == 2: 
				return
			else:
				QMessageBox.about(self, "Access Denied!", "Authentication failed!")
			
		elif signal == 'STOP':
			status = self.password_verification()
			if status == 2: 
				# Cancel pressed
				return
			elif status == 1:
				self.process_event('STOP', extra_data)
			else:
				QMessageBox.about(self, "Access Denied!", "Authentication failed!")
		return
		
	def validate_date(self, data):
		#Check that data is a valid date in HH:MM:SS format
		try:
			h, m, s = data.split(':')
			if len(h) != 2 or len(m) != 2 or len(s) != 2:
				print('[ ERROR ] Enter time in HH:MM:SS format only!')
				return False
			h = int(h)
			m = int(m)
			s = int(s)
			if h < 0 or h > 24 or m < 0 or m > 59 or s < 0 or s > 59:
				QMessageBox.about(self, "Error!", "Enter time in HH:MM:SS format only!")
				return False
			return True
		except:
			QMessageBox.about(self, "Error!", "Enter time in HH:MM:SS format only!")
			return False



	def contest_reset_settings(self):
		contest_reset_label = QLabel('Reset Contest:')
		contest_reset_label.setObjectName('main_screen_sub_heading')

		# Reset contest labels and buttons
		account_reset_label = QLabel('> Reset Accounts ')
		account_reset_label.setObjectName('main_screen_content')
		account_reset_label.setFixedSize(200, 25)
		account_reset_button = QPushButton('RESET')
		account_reset_button.setFixedSize(70, 25)
		account_reset_button.setObjectName('interior_button')
		account_reset_button.setToolTip(
			'DELETE all accounts.\nConnected clients will NOT be disconnected.'
			)
		account_reset_button.clicked.connect(self.reset_accounts)
		account_reset_layout = QHBoxLayout()
		account_reset_layout.addWidget(account_reset_label)
		account_reset_layout.addWidget(account_reset_button)
		account_reset_layout.addStretch(1)
		account_reset_widget = QWidget()
		account_reset_widget.setLayout(account_reset_layout)


		submission_reset_label = QLabel('> Reset Submissions ')
		submission_reset_label.setObjectName('main_screen_content')
		submission_reset_label.setFixedSize(200, 25)
		submission_reset_button = QPushButton('RESET')
		submission_reset_button.setFixedSize(70, 25)
		submission_reset_button.setObjectName('interior_button')
		submission_reset_button.setToolTip('DELETE all submissions.')
		submission_reset_button.clicked.connect(self.reset_submissions)
		submission_reset_layout = QHBoxLayout()
		submission_reset_layout.addWidget(submission_reset_label)
		submission_reset_layout.addWidget(submission_reset_button)
		submission_reset_layout.addStretch(1)
		submission_reset_widget = QWidget()
		submission_reset_widget.setLayout(submission_reset_layout)

		query_reset_label = QLabel('> Reset Queries ')
		query_reset_label.setObjectName('main_screen_content')
		query_reset_label.setFixedSize(200, 25)
		query_reset_button = QPushButton('RESET')
		query_reset_button.setFixedSize(70, 25)
		query_reset_button.setObjectName('interior_button')
		query_reset_button.setToolTip('DELETE all queries')
		query_reset_button.clicked.connect(self.reset_queries)
		query_reset_layout = QHBoxLayout()
		query_reset_layout.addWidget(query_reset_label)
		query_reset_layout.addWidget(query_reset_button)
		query_reset_layout.addStretch(1)
		query_reset_widget = QWidget()
		query_reset_widget.setLayout(query_reset_layout)

		client_reset_label = QLabel('> Disconnect Clients ')
		client_reset_label.setObjectName('main_screen_content')
		client_reset_label.setFixedSize(200, 25)
		client_reset_button = QPushButton('RESET')
		client_reset_button.setFixedSize(70, 25)
		client_reset_button.setObjectName('interior_button')
		client_reset_button.setToolTip('Disconnect all clients.')
		client_reset_button.clicked.connect(self.disconnect_all)
		client_reset_layout = QHBoxLayout()
		client_reset_layout.addWidget(client_reset_label)
		client_reset_layout.addWidget(client_reset_button)
		client_reset_layout.addStretch(1)
		client_reset_widget = QWidget()
		client_reset_widget.setLayout(client_reset_layout)

		timer_reset_label = QLabel('> Reset Timer ')
		timer_reset_label.setObjectName('main_screen_content')
		timer_reset_label.setFixedSize(200, 25)
		timer_reset_button = QPushButton('RESET')
		timer_reset_button.setFixedSize(70, 25)
		timer_reset_button.setObjectName('interior_button')
		timer_reset_button.setToolTip('Reset contest timer and state.\nCan be used when contest is STOPPED.')
		timer_reset_button.clicked.connect(self.reset_timer)
		timer_reset_layout = QHBoxLayout()
		timer_reset_layout.addWidget(timer_reset_label)
		timer_reset_layout.addWidget(timer_reset_button)
		timer_reset_layout.addStretch(1)
		timer_reset_widget = QWidget()
		timer_reset_widget.setLayout(timer_reset_layout)

		server_reset_label = QLabel('> Reset SERVER ')
		server_reset_label.setObjectName('main_screen_content')
		server_reset_label.setFixedSize(200, 25)
		server_reset_button = QPushButton('CONFIRM')
		server_reset_button.setEnabled(True)
		server_reset_button.setFixedSize(70, 25)
		server_reset_button.setObjectName('interior_button')
		server_reset_button.setToolTip('Reset the Server.\nCan not be used in RUNNING state.')
		server_reset_button.clicked.connect(self.reset_server)
		server_reset_layout = QHBoxLayout()
		server_reset_layout.addWidget(server_reset_label)
		server_reset_layout.addWidget(server_reset_button)
		server_reset_layout.addStretch(1)
		server_reset_widget = QWidget()
		server_reset_widget.setLayout(server_reset_layout)

		button_layout = QGridLayout()
		button_layout.addWidget(account_reset_widget, 0, 0)
		button_layout.addWidget(submission_reset_widget, 0, 1)
		button_layout.addWidget(query_reset_widget, 1, 0)
		button_layout.addWidget(client_reset_widget, 1, 1)
		button_layout.addWidget(timer_reset_widget, 2, 0)
		button_layout.addWidget(server_reset_widget, 2, 1)
		button_layout.setColumnStretch(0,1)
		button_layout.setColumnStretch(1,3)

		button_widget = QWidget()
		button_widget.setLayout(button_layout)

		contest_reset_layout = QVBoxLayout()
		contest_reset_layout.addWidget(contest_reset_label)
		contest_reset_layout.addWidget(button_widget)
		contest_reset_widget = QWidget()
		contest_reset_widget.setLayout(contest_reset_layout)
		contest_reset_widget.setObjectName('content_box')
		return (
			contest_reset_widget, 
			account_reset_button, 
			submission_reset_button, 
			query_reset_button, 
			client_reset_button, 
			server_reset_button,
			timer_reset_button
		)

	def contest_ranking_settings(self):
		# TODO
		# 1.Select Ranking algorithm
		# 	1.Select Penalty Duration
		# 2.Set if leaderboard is to be shown to clients
		
		main_layout = QVBoxLayout()
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName('account_window')
		return main

	def settings_ui(self):
		heading = QLabel('Server Settings')
		heading.setObjectName('main_screen_heading')
		(
			time_management_widget, 
			contest_time_entry, 
			change_time_entry, 
			set_button, 
			start_button, 
			update_button, 
			stop_button
		) = ui_widgets.contest_time_settings(self)

		(
			contest_reset_widget, account_reset_button, 
			submission_reset_button, query_reset_button, 
			client_reset_button, server_reset_button, timer_reset_button
		) = ui_widgets.contest_reset_settings(self)

		(
			main
		) = ui_widgets.contest_ranking_settings(self)


		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(time_management_widget)
		main_layout.addWidget(contest_reset_widget)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return (
			main, contest_time_entry, change_time_entry, 
			set_button, start_button, update_button, stop_button, 
			account_reset_button, submission_reset_button, 
			query_reset_button, client_reset_button, server_reset_button,
			timer_reset_button
			)

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
	pwd_type = 'Simple'
	client_no = 0
	judge_no = 0
	data_changed_flags = ''
	
	def __init__(self, data_changed_flags, parent=None):
		super(new_accounts_ui, self).__init__(parent)
		self.data_changed_flags = data_changed_flags
		self.setGeometry(800, 450, 300, 200)
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
		new_accounts_ui.client_no = 0
		new_accounts_ui.judge_no = 0
		
		label1 = QLabel('Clients')

		client_entry = QSpinBox()
		client_entry.setMinimum(0)
		client_entry.setMaximum(500)
		client_entry.valueChanged.connect(new_accounts_ui.client_updater)
		
		label2 = QLabel('Judges')

		judge_entry = QSpinBox()
		judge_entry.setMinimum(0)
		judge_entry.setMaximum(10)
		judge_entry.valueChanged.connect(new_accounts_ui.judge_updater)
	
		label3 = QLabel('Password Type:')

		password_type_entry = QComboBox()
		#If you change these labels, also change lines 309, 311 in database_management.py
		password_type_entry.addItem('Simple')
		password_type_entry.addItem('Random')
		password_type_entry.activated[str].connect(new_accounts_ui.combo_box_data_changed)

		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(200, 50)
		confirm_button.clicked.connect(lambda:new_accounts_ui.final_account_status(self))
		confirm_button.setDefault(True)
		
		
		layout = QGridLayout()
		layout.addWidget(label1, 0, 0)
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
		user_management.generate_n_users(
			new_accounts_ui.client_no, new_accounts_ui.judge_no, 
			new_accounts_ui.pwd_type
			)
		# Reset the critical section flag
		self.data_changed_flags[4] = 0
		# Indicate new insertions in accounts
		self.data_changed_flags[5] = 1
		self.close()

class query_reply_ui(QMainWindow):
	button_mode = 1
	query = ''
	query_id = ''
	client_id = ''
	def __init__(
		self, data_changed_flags,task_queue, 
		query, client_id, query_id, parent=None
		):
		super(query_reply_ui, self).__init__(parent)
		query_reply_ui.button_mode = 1

		self.data_changed_flags = data_changed_flags
		self.task_queue = task_queue
		query_reply_ui.query = query
		query_reply_ui.query_id = query_id
		query_reply_ui.client_id = client_id

		self.setWindowTitle('Reply')
		self.setGeometry(750, 350, 400, 400)
		self.setFixedSize(400,400)
		main = self.main_query_reply_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_query_reply_ui(self):
		query_heading = QLabel('New Clarification')
		query_sub_heading = QLabel('Query:')
		response_sub_heading = QLabel('Response:')
		
		query_text = QTextEdit()
		query_text.setText(query_reply_ui.query)
		query_text.setReadOnly(True)

		response_entry = QTextEdit()
		response_entry.setPlaceholderText('Max. 500 Characters')

		
		broadcast_setting_label = QLabel('Reply to: ')
		send_to_client_rbutton = QRadioButton('Client')
		send_to_all_rbutton = QRadioButton('All')
		send_to_client_rbutton.setChecked(True)
		send_to_all_rbutton.setChecked(False)
		send_to_client_rbutton.toggled.connect(
			lambda: query_reply_ui.send_mode_setter(self, send_to_client_rbutton)
		)
		send_to_all_rbutton.toggled.connect(
			lambda: query_reply_ui.send_mode_setter(self, send_to_all_rbutton)
		)

		radiobutton_layout = QHBoxLayout()
		radiobutton_layout.addWidget(broadcast_setting_label)
		radiobutton_layout.addWidget(send_to_client_rbutton)
		radiobutton_layout.addWidget(send_to_all_rbutton)
		radiobutton_layout.addStretch(1)
		radiobutton_layout.setSpacing(50)
		
		radiobutton_widget = QWidget()
		radiobutton_widget.setLayout(radiobutton_layout)
		radiobutton_widget.setContentsMargins(25,0,0,0)


		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(150, 30)
		confirm_button.clicked.connect(
			lambda:query_reply_ui.final_status(self, response_entry.toPlainText())
			)
		confirm_button.setDefault(True)

		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(150, 30)
		cancel_button.clicked.connect(
			lambda:query_reply_ui.cancel(self)
			)
		cancel_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(1)
		#button_layout.setSpacing(5)

		button_widget = QWidget()
		button_widget.setLayout(button_layout)


		main_layout = QVBoxLayout()
		main_layout.addWidget(query_heading)
		main_layout.addWidget(query_sub_heading)
		main_layout.addWidget(query_text)
		main_layout.addWidget(response_sub_heading)
		main_layout.addWidget(response_entry)
		main_layout.addWidget(radiobutton_widget)
		main_layout.addWidget(button_widget)
		main = QWidget()
		main.setLayout(main_layout)

		confirm_button.setObjectName('account_button')
		cancel_button.setObjectName('account_button')
		query_heading.setObjectName('main_screen_heading')
		broadcast_setting_label.setObjectName('main_screen_content')
		main.setObjectName('account_window')
		query_sub_heading.setObjectName('main_screen_sub_heading')
		response_sub_heading.setObjectName('main_screen_sub_heading')
		send_to_all_rbutton.setObjectName('interior_rbutton')
		send_to_client_rbutton.setObjectName('interior_rbutton')
		return main

	def send_mode_setter(self, rbutton):
		if rbutton.text() == 'Client':
			if rbutton.isChecked() == True:
				query_reply_ui.button_mode = 1
		else:
			if rbutton.isChecked() == True:
				query_reply_ui.button_mode = 2
		return

	def final_status(self, response):
		if query_reply_ui.button_mode == 2:
			send_type = 'Broadcast'
		else:
			send_type = 'Client'
		message ={
			'Code' : 'QUERY',
			'Query' : query_reply_ui.query,
			'Response' : response,
			'Mode' : send_type,
			'Query ID' : query_reply_ui.query_id,
			'Client ID' : query_reply_ui.client_id
		}
		message = json.dumps(message)
		self.task_queue.put(message)
		query_management.update_query(query_reply_ui.query_id, response)
		self.data_changed_flags[8] = 0
		self.data_changed_flags[9] = 1
		self.close()

	def cancel(self):
		self.data_changed_flags[8] = 0
		self.close()

class manage_submission_ui(QMainWindow):
	data_changed_flags = ''
	task_queue = ''
	run_id = ''
	client_id = ''
	pcode = ''
	language = ''
	timestamp = ''
	verdict = ''
	sent_status = ''

	verdict_dict = {
	'AC' : 'AC - Correct Answer', 
	'WA' : 'WA - Wrong Answer', 
	'TLE' : 'TLE - Time Limit Exceeded',
	'CMPL' : 'CMPL - Compilation Error',
	'PE' : 'PE - Presentation Error',
	'RE' : 'RE - Run Time Error',
	'OLE' : 'OLE - Output Limit Exceeded',
	'NZEC' : 'NZEC - Non Zero Exit Code'
	}
	inverted_verdict_dict = { v : k for k, v in verdict_dict.items()}
	
	def __init__(
			self, 
			data_changed_flags,
			task_queue, 
			run_id,
			client_id,
			problem_code,
			language ,
			timestamp,
			verdict,
			sent_status,
			parent=None
		):
		super(manage_submission_ui, self).__init__(parent)
		query_reply_ui.button_mode = 1

		self.data_changed_flags = data_changed_flags
		self.task_queue = task_queue
		self.run_id = run_id
		self.client_id = client_id
		self.problem_code = problem_code
		self.language = language
		self.timestamp = timestamp
		self.verdict = verdict
		self.sent_status = sent_status

		width = 800
		height = 500
		self.setGeometry(550, 300, width, height)
		self.setWindowTitle('Run ' + str(run_id) + 'From Client ' + str(client_id))
		self.setFixedSize(width, height)
		main = self.main_manage_sub_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_manage_sub_ui(self):
		submission_heading = QLabel('Manual Validation')

		submission_sub_heading = QLabel('Run Information: ')
		team_name = client_authentication.get_client_username(self.client_id)
		run_id_label = QLabel("Run ID:  " + str(self.run_id))
		client_label = QLabel("Client:  " + team_name + '( ID: ' + str(self.client_id) + ')')
		problem_label = QLabel("Problem:  " + self.problem_code)
		language_label = QLabel("Language:  " + self.language)
		time_label = QLabel("Time:  " + self.timestamp)

		if self.sent_status == 'SENT':
			sent_text = QLabel("Response has been sent to the Team")
			sent_text.setObjectName('main_screen_green_content')
		elif self.sent_status == 'HALTED':
			sent_text = QLabel("<Security Exception> Judge NOT verified.")
			sent_text.setObjectName('main_screen_red_content')
		else:
			sent_text = QLabel("Waiting for Judgement")
			sent_text.setObjectName('main_screen_content')

		run_info_layout = QGridLayout()
		run_info_layout.addWidget(run_id_label, 0, 0)
		run_info_layout.addWidget(client_label, 0, 1)
		run_info_layout.addWidget(problem_label, 1, 0)
		run_info_layout.addWidget(language_label, 1, 1)
		run_info_layout.addWidget(time_label, 2, 0)
		run_info_layout.addWidget(sent_text, 3, 0)
		run_info_widget = QWidget()
		run_info_widget.setLayout(run_info_layout)

		verdict_sub_heading = QLabel("Judgement:")
		judge = submissions_management.get_judge(self.run_id)
		judge_verdict = QLabel(judge + ' Verdict:  ')

		try:
			verdict = QLabel(self.verdict_dict[self.verdict])
		except:
			verdict = QLabel(self.verdict)

		if self.verdict == 'AC':
			verdict.setObjectName('main_screen_green_content')
		else:
			verdict.setObjectName('main_screen_red_content')

		send_button = QPushButton("Accept Verdict")
		send_button.setFixedSize(200, 50)
		send_button.clicked.connect(lambda:manage_submission_ui.accept_verdict(self))
		manual_judgement_label = QLabel("Manual Judgement: ")
		manual_judgement_entry = QComboBox()
		manual_judgement_entry.addItem('<- SELECT ->')
		manual_judgement_entry.addItem(self.verdict_dict['AC'])
		manual_judgement_entry.addItem(self.verdict_dict['WA'])
		manual_judgement_entry.addItem(self.verdict_dict['TLE'])
		manual_judgement_entry.addItem(self.verdict_dict['CMPL'])
		manual_judgement_entry.addItem(self.verdict_dict['PE'])
		manual_judgement_entry.addItem(self.verdict_dict['RE'])
		manual_judgement_entry.addItem(self.verdict_dict['OLE'])
		manual_judgement_entry.addItem(self.verdict_dict['NZEC'])
		
		accept_select_button = QPushButton("Accept Selected")
		accept_select_button.setFixedSize(200, 50)
		accept_select_button.clicked.connect(
			lambda: manage_submission_ui.manual_verdict(
				self,  
				str(manual_judgement_entry.currentText())
			)
		)
		verdict_layout = QGridLayout()
		verdict_layout.addWidget(judge_verdict, 0, 0)
		verdict_layout.addWidget(verdict, 0, 1)
		verdict_layout.addWidget(send_button, 0, 2)
		verdict_layout.addWidget(manual_judgement_label, 1, 0)
		verdict_layout.addWidget(manual_judgement_entry, 1, 1)
		verdict_layout.addWidget(accept_select_button, 1, 2)	
		verdict_layout.setRowStretch(1,60)

		verdict_widget = QWidget()
		verdict_widget.setLayout(verdict_layout)

		

		rejudge_button = QPushButton('Rejudge')
		rejudge_button.setFixedSize(150, 40)
		rejudge_button.clicked.connect(
			lambda:manage_submission_ui.rejudge(self)
			)

		view_output_source_button = QPushButton('Submission Source and Data')
		view_output_source_button.setFixedSize(250, 40)
		view_output_source_button.clicked.connect(
			lambda:manage_submission_ui.load_submission_data(self)
			)
		
		close_button = QPushButton('Close')
		close_button.setFixedSize(150, 40)
		close_button.clicked.connect(
			lambda:manage_submission_ui.close(self)
			)
		close_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addWidget(rejudge_button)
		button_layout.addWidget(view_output_source_button)
		button_layout.addWidget(close_button)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)

		spacer_item = QSpacerItem(0, 50, QSizePolicy.Expanding)
		
		main_layout = QVBoxLayout()
		main_layout.addWidget(submission_heading)
		main_layout.addWidget(submission_sub_heading)
		main_layout.addWidget(run_info_widget)
		main_layout.addWidget(verdict_sub_heading)
		main_layout.addWidget(verdict_widget)
		main_layout.addSpacerItem(spacer_item)
		main_layout.addWidget(button_widget)
		main_layout.setAlignment(Qt.AlignHCenter)
		
		main_layout.addStretch(1)

		main = QWidget()
		main.setLayout(main_layout)

		main.setObjectName('account_window')
		run_info_widget.setObjectName('content_box')
		verdict_widget.setObjectName('content_box')

		submission_heading.setObjectName('main_screen_heading')

		submission_sub_heading.setObjectName('main_screen_sub_heading')
		verdict_sub_heading.setObjectName('main_screen_sub_heading')
		
		client_label.setObjectName('main_screen_content')
		problem_label.setObjectName('main_screen_content')
		language_label.setObjectName('main_screen_content')
		time_label.setObjectName('main_screen_content')
		run_id_label.setObjectName('main_screen_content')
		judge_verdict.setObjectName('main_screen_content')
		manual_judgement_label.setObjectName('main_screen_content')
		
		manual_judgement_entry.setObjectName('account_combobox')

		send_button.setObjectName('interior_button')
		accept_select_button.setObjectName('interior_button')
		rejudge_button.setObjectName('interior_button')
		view_output_source_button.setObjectName('interior_button')
		close_button.setObjectName('interior_button')
		return main

	def rejudge(self):
		print('[ EVENT ][ REJUDGE ] Run ' + str(self.run_id) + ' by ADMIN')
		client_username = client_authentication.get_client_username(self.client_id)
		file_name = submissions_management.get_source_file_name(self.run_id)
		if file_name == 'NONE':
			print('[ ERROR ] Source file not found!')
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Alert')
			info_box.setText('Source file not found!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return

		try:
			file = open("Client_Submissions/" + file_name ,"r")
			source_code = file.read()
			file.close()
		except:
			print('[ ERROR ] Source file could not be accessed!')
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Alert')
			info_box.setText('Source file could not be accessed!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return

		local_run_id = submissions_management.get_local_run_id(self.run_id)
		message = {
			'Code' : 'RJUDGE', 
			'Client ID' : self.client_id, 
			'Client Username' : client_username,
			'Run ID' : self.run_id,
			'Language' : self.language,
			'PCode' : self.problem_code,
			'Source' : source_code,
			'Local Run ID' : local_run_id,
			'Time Stamp' : self.timestamp
		}
		message = json.dumps(message)
		self.task_queue.put(message)
		self.data_changed_flags[8] = 0
		self.close()

	def manual_verdict(self, manual_verdict):
		if self.verdict == 'Running':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Alert')
			info_box.setText('Verdict is not yet Recieved!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		elif self.verdict == 'SECURITY':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Security Alert')
			info_box.setText('Please Rejudge.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		elif manual_verdict == '<- SELECT ->':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Alert')
			info_box.setText('Please select a verdict.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		else:
			buttonReply = QMessageBox.question(
				self, 
				'Confirm Selection', 
				'Are you sure you want to give \'' + manual_verdict + '\' verdict', 
				QMessageBox.Yes | QMessageBox.No, 	# Button Options
				QMessageBox.No 			# Default button
			)
			if buttonReply == QMessageBox.Yes:
				pass
			else:
				return

		client_username = client_authentication.get_client_username(self.client_id)
		local_run_id = submissions_management.get_local_run_id(self.run_id)
		message = {
			'Code' : 'VRDCT', 
			'Receiver' : client_username,
			'Local Run ID' : local_run_id,
			'Run ID' : self.run_id,
			'Status' : self.inverted_verdict_dict[manual_verdict],
			'Message' : self.get_message(self.run_id),
			'Judge' : 'ADMIN'
		}
		message = json.dumps(message)
		self.task_queue.put(message)
		print('[ VERDICT ][ SENT ] Manual Verdict:' + manual_verdict + 'Sent to Client ' + client_username)

		# TODO: UPDATE LEADERBOARD

		self.data_changed_flags[8] = 0
		self.close()

	def accept_verdict(self):
		if self.verdict == 'Running':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Alert')
			info_box.setText('Verdict is not yet Recieved!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		elif self.verdict == 'SECURITY':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Security Alert')
			info_box.setText('Please Rejudge.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return

		client_username = client_authentication.get_client_username(self.client_id)
		local_run_id = submissions_management.get_local_run_id(self.run_id)
		judge = submissions_management.get_judge(self.run_id)
		message = {
			'Code' : 'VRDCT', 
			'Receiver' : client_username,
			'Local Run ID' : local_run_id,
			'Run ID' : self.run_id,
			'Status' : self.verdict,
			'Message' : self.get_message(self.run_id),
			'Judge' : judge
		}
		message = json.dumps(message)
		self.task_queue.put(message)
		print('[ VERDICT ][ SENT ] Judge Verdict accepted and sent to Client ' + client_username)

		# TODO: UPDATE LEADERBOARD AND SUBMISSION TABLE

		self.data_changed_flags[8] = 0
		self.close()

	def get_message(self, run_id):
		try:
			filename = './Client_Submissions/' + str(self.run_id) + '_latest.info'
			with open(filename) as file:
				data = file.read()
			if data != '':
				return data
			else:
				return 'No Error data received!'
		except:
			return 'No Error data received!'

	def load_submission_data(self):
		self.submission_ui = submission_data_ui(self.data_changed_flags, self.run_id)
		self.data_changed_flags[8] = 0
		self.submission_ui.show()

	def cancel(self):
		self.data_changed_flags[8] = 0
		self.close()


class submission_data_ui(QMainWindow):
	def __init__(
			self, 
			data_changed_flags, 
			run_id, 
			parent = None
		):
		super(submission_data_ui, self).__init__(parent)
		
		self.data_changed_flags = data_changed_flags
		self.run_id = run_id
		
		self.setWindowTitle('Run ' + str(self.run_id))

		width = 800
		height = 500
		self.setGeometry(550, 300, width, height)
		self.setFixedSize(width, height)
		main = self.main_submission_data_ui()
		self.setCentralWidget(main)
		return

	def main_submission_data_ui(self):
		self.tabs = QTabWidget()
		self.tabs.setObjectName('main_tabs')
		self.tab_bar = QTabBar()
		self.tab_bar.setObjectName('problem_tabs')

		self.tab1 = self.get_tab1_widget()
		self.tab2 = self.get_tab2_widget()
		
		self.tabs.addTab(self.tab1, '')
		self.tabs.addTab(self.tab2, '')
		self.tab_bar.addTab('Source Data')
		self.tab_bar.addTab('Error Data')
		self.tabs.setTabBar(self.tab_bar)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.tabs)
		main = QWidget()
		main.setLayout(main_layout)

		main.setObjectName('account_window')
		return main

	def get_tab1_widget(self):
		source_layout = QVBoxLayout()
		heading1 = QLabel('Source Data')

		# Read source file
		filename = './Client_Submissions/' + submissions_management.get_source_file_name(self.run_id)
		file_label = QLabel('File: ')
		filename_label = QLabel(filename)
		label_layout = QHBoxLayout()
		label_layout.addWidget(file_label)
		label_layout.addWidget(filename_label)
		label_layout.addStretch(1)
		label_widget = QWidget()
		label_widget.setLayout(label_layout)
		try:
			with open(filename) as file:
				data = file.read()
		except:
			data = 'Error: File not found!'

		content = QTextEdit()
		content.setText(data)

		source_layout.addWidget(heading1)
		source_layout.addWidget(label_widget)
		source_layout.addWidget(content)
		source_widget = QWidget()
		source_widget.setLayout(source_layout)

		heading1.setObjectName('main_screen_heading')
		file_label.setObjectName('main_screen_sub_heading')
		filename_label.setObjectName('main_screen_content')
		return source_widget

	def get_tab2_widget(self):
		error_layout = QVBoxLayout()
		heading1 = QLabel('Error Data')
		# Read error file
		filename = './Client_Submissions/' + str(self.run_id) + '.info'
		file_label = QLabel('File: ')
		filename_label = QLabel(filename)
		label_layout = QHBoxLayout()
		label_layout.addWidget(file_label)
		label_layout.addWidget(filename_label)
		label_layout.addStretch(1)
		label_widget = QWidget()
		label_widget.setLayout(label_layout)
		try:
			with open(filename) as file:
				data = file.read()
		except:
			data = 'Error: File not found!'

		content = QTextEdit()
		content.setText(data)

		error_layout.addWidget(heading1)
		error_layout.addWidget(label_widget)
		error_layout.addWidget(content)
		error_widget = QWidget()
		error_widget.setLayout(error_layout)

		heading1.setObjectName('main_screen_heading')
		file_label.setObjectName('main_screen_sub_heading')
		filename_label.setObjectName('main_screen_content')
		return error_widget

class account_edit_ui(QMainWindow):
	client_id = ''
	username = ''
	password = ''
	state = ''
	state_type = ''
	changed = 0
	def __init__(
		self, data_changed_flags, client_id, 
		username, password, state, parent=None
		):
		super(account_edit_ui, self).__init__(parent)
		
		self.data_changed_flags = data_changed_flags
		account_edit_ui.client_id = client_id
		account_edit_ui.username = username
		account_edit_ui.password = password
		account_edit_ui.state = state
		account_edit_ui.state_type = state
		
		self.setWindowTitle('Manage Client')
		self.setGeometry(750, 350, 400, 350)
		self.setFixedSize(400,350)
		main = self.main_account_edit_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_account_edit_ui(self):
		heading = QLabel('Edit user status')

		username_label = QLabel('Username: ')
		username_content = QLabel(account_edit_ui.username)

		password_label = QLabel('Password: ')
		password_content = QLabel(account_edit_ui.password)

		state_label = QLabel('Current State: ')
		current_state = QLabel(account_edit_ui.state)

		state_entry_label = QLabel('Set State: ')
		state_entry = QComboBox()
		state_entry.addItem('<- SELECT ->')
		state_entry.addItem('Connected')
		state_entry.addItem('Disconnected')
		state_entry.addItem('Blocked')
		state_entry.activated[str].connect(account_edit_ui.combo_box_data_changed)
		
		inner_layout = QGridLayout()
		inner_layout.addWidget(username_label, 0, 0)
		inner_layout.addWidget( username_content, 0, 1)
		inner_layout.addWidget(password_label, 1, 0)
		inner_layout.addWidget(password_content, 1, 1)
		inner_layout.addWidget(state_label, 2, 0)
		inner_layout.addWidget(current_state, 2, 1)
		inner_layout.addWidget(state_entry_label, 3, 0)
		inner_layout.addWidget(state_entry, 3, 1)

		inner_layout.setColumnMinimumWidth(0,50)
		inner_layout.setColumnMinimumWidth(1,50)
		inner_layout.setColumnStretch(0, 1)
		inner_layout.setColumnStretch(1, 1)
		inner_layout.setRowStretch(0, 1)
		inner_layout.setRowStretch(1, 1)
		inner_layout.setVerticalSpacing(10)
		
		# inner_layout.addStretch(1)
		inner_widget = QWidget()
		inner_widget.setLayout(inner_layout)
				
		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(150, 30)
		confirm_button.clicked.connect(lambda:account_edit_ui.final_status(self))
		confirm_button.setDefault(True)
		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(150, 30)
		cancel_button.clicked.connect(lambda:account_edit_ui.exit(self))
		cancel_button.setDefault(True)
		button_layout = QHBoxLayout()
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(1)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)
		button_widget.setContentsMargins(0, 20, 0, 0)

		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(inner_widget)
		main_layout.addWidget(button_widget)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)

		main.setObjectName('account_window')
		heading.setObjectName('main_screen_heading')
		confirm_button.setObjectName('account_button')
		cancel_button.setObjectName('account_button')
		username_label.setObjectName('main_screen_sub_heading')
		username_content.setObjectName('main_screen_content')
		password_label.setObjectName('main_screen_sub_heading')
		password_content.setObjectName('main_screen_content')
		state_label.setObjectName('main_screen_sub_heading')
		current_state.setObjectName('main_screen_content')
		state_entry_label.setObjectName('main_screen_sub_heading')
		state_entry.setObjectName('account_combobox')
		return main

	def combo_box_data_changed(text):
		if str(text) != '<- SELECT ->':
			account_edit_ui.changed = 1
			account_edit_ui.state_type = str(text)
		else:
			account_edit_ui.changed = 0

	def final_status(self):
		# If something is changed in combo box, run query 
		if account_edit_ui.changed == 1:
			user_management.update_user_state(account_edit_ui.username, account_edit_ui.state_type)
			self.data_changed_flags[1] = 1
		self.data_changed_flags[14] = 0
		self.close()

	def exit(self):
		self.data_changed_flags[14] = 0
		self.close()

