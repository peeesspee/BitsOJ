from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase 
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, QSize, QRect
import os
import time
import json
import webbrowser
from functools import partial
from manage_code import send_code
from database_management import submission_management, query_management, manage_local_ids

with open("config.json", "r") as read_config:
	config = json.load(read_config)



class ui_widgets():
	#############################################################################
	# Handle UI for various button presses
	var = {}
	def problems_ui(self):

		main_layout = QVBoxLayout() 
		heading = QLabel('Problems')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		
		column = 0
		row = 0
		number_of_buttons = 1 
		self.scrollArea = QScrollArea(self)
		self.scrollArea.setWidgetResizable(True)
		self.scrollAreaWidgetContents = QWidget()
		self.scrollAreaWidgetContents.setObjectName('myobject')
		problems_layout = QGridLayout(self.scrollAreaWidgetContents)
		# problems_layout = QGridLayout()
		# problems_layout.setSpacing(20)
		while(number_of_buttons <= config["No_of_Problems"]):
		# for i in range(config["No_of_Problems"]):
			ui_widgets.var['Problem_{}'.format(number_of_buttons)] = QPushButton('Problem_'+str(number_of_buttons),self)
			ui_widgets.var['Problem_{}'.format(number_of_buttons)].setObjectName('problem_buttons')
			ui_widgets.var['Problem_{}'.format(number_of_buttons)].setFixedSize(500, 200)
			ui_widgets.var['Problem_{}'.format(number_of_buttons)].clicked.connect(partial(ui_widgets.show_problem, number_of_buttons, self.data_changed_flag, self))
			problems_layout.addWidget(ui_widgets.var['Problem_{}'.format(number_of_buttons)],row,column)
			if(column==1):
				row+=1;
				column=0;
			else:
				column+=1;
			number_of_buttons+=1;

		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.scrollArea.setFixedHeight(700)
		self.scrollArea.setObjectName('myscrollarea')
		problems_layout.setObjectName('mygrid')
		# problems_widget = QWidget()
		# problems_widget.setLayout(problems_layout)
		main_layout.addWidget(self.scrollArea)
		# main_layout.addWidget(problems_widget)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def submissions_ui(self):
		heading = QLabel('My Submissions')
		heading.setObjectName('main_screen_heading')

		submission_model = self.manage_models(self.db, 'my_submissions')

		submission_model.setHeaderData(0, Qt.Horizontal, 'Local Id')
		submission_model.setHeaderData(1, Qt.Horizontal, 'Run Id')
		submission_model.setHeaderData(2, Qt.Horizontal, 'Verdict')
		submission_model.setHeaderData(3, Qt.Horizontal, 'Source File')
		submission_model.setHeaderData(4, Qt.Horizontal, 'Language')
		submission_model.setHeaderData(5, Qt.Horizontal, 'Problem Code')
		submission_model.setHeaderData(6, Qt.Horizontal, 'Time')

		submission_table = self.generate_view(submission_model)


		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(submission_table)
		main_layout.setStretch(0, 5)
		main_layout.setStretch(1, 95)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")
		main.show()
		return main, submission_model

	def submit_ui(self):

		heading = QLabel('Submit Solution')
		heading.setObjectName('main_screen_heading')

		self.drop_down = QHBoxLayout()
		ui_widgets.language_box = QComboBox()
		ui_widgets.language_box.setGeometry(QRect(10, 10, 491, 31))
		ui_widgets.language_box.setFixedWidth(250)
		ui_widgets.language_box.setFixedHeight(40)
		ui_widgets.language_box.setObjectName(("language_box_content"))
		ui_widgets.language_box.addItem("PYTHON-3")
		ui_widgets.language_box.addItem("PYTHON-2")
		ui_widgets.language_box.addItem("C")
		ui_widgets.language_box.addItem("C++")
		ui_widgets.language_box.addItem("JAVA")

		ui_widgets.problem_box = QComboBox()
		ui_widgets.problem_box.setGeometry(QRect(10, 10, 491, 31))
		ui_widgets.problem_box.setFixedWidth(250)
		ui_widgets.problem_box.setFixedHeight(40)
		ui_widgets.problem_box.setObjectName(("language_box_content"))
		for i in range(config["No_of_Problems"]):
			ui_widgets.problem_box.addItem("Problem_"+str(i+1))

		self.drop_down.addWidget(ui_widgets.language_box)
		self.drop_down.addWidget(ui_widgets.problem_box)
		self.drop_widget = QWidget()
		self.drop_widget.setLayout(self.drop_down)

		ui_widgets.text_area = QTextEdit()
		ui_widgets.text_area.setFixedHeight(650)
		ui_widgets.text_area.setObjectName('text_area_content')
		ui_widgets.text_area.setPlaceholderText('Paste your code here')

		self.horizontal_layout = QHBoxLayout()
		self.submit_solution = QPushButton('Submit', self)
		self.submit_solution.setObjectName('submit')
		self.submit_solution.setFixedSize(200, 50)
		self.submit_solution.clicked.connect(lambda:ui_widgets.submit_call(self, self.data_changed_flag))
		self.horizontal_layout.addWidget(self.submit_solution,  alignment=Qt.AlignRight)

		self.horizontal_widget = QWidget()
		self.horizontal_widget.setLayout(self.horizontal_layout)



		main_layout = QVBoxLayout() 

		main_layout.addWidget(heading)
		main_layout.addWidget(self.drop_widget)
		main_layout.addWidget(ui_widgets.text_area)
		main_layout.addWidget(self.horizontal_widget)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def query_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Query')
		heading.setObjectName('main_screen_heading')

		query_model = self.manage_models(self.db, 'my_query')

		query_model.setHeaderData(0, Qt.Horizontal, 'Query')
		query_model.setHeaderData(1, Qt.Horizontal, 'Response')

		query_table = self.generate_view(query_model)

		ui_widgets.ask_query = QLineEdit(self)
		ui_widgets.ask_query.setFixedWidth(500)
		ui_widgets.ask_query.setFixedHeight(50)
		ui_widgets.ask_query.setPlaceholderText('    Problem 1 : Your Query ')
		ui_widgets.ask_query.setToolTip(" Send the query in this format only.\n Else it might get ignored.")
		ui_widgets.ask_query.setObjectName('ask_query')

		self.send_query = QPushButton('Send', self)
		self.send_query.setFixedSize(200, 50)
		self.send_query.clicked.connect(lambda:ui_widgets.sending(self,self.data_changed_flag))
		self.send_query.setObjectName('ask')


		main_layout.addWidget(heading)
		main_layout.addWidget(query_table)
		main_layout.addWidget(ui_widgets.ask_query, alignment=Qt.AlignLeft)
		main_layout.addWidget(self.send_query, alignment=Qt.AlignLeft)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main, query_model

	def leaderboard_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Leaderboard')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def about_ui(self):
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



	def submit_call(self, data_changed_flag):

		if data_changed_flag[0] == 0:
			QMessageBox.warning(self, 'Message', 'Contest not yet started.\nPlease wait.')
		elif data_changed_flag[0] == 3:
			QMessageBox.warning(self, 'Message', 'Contest has been STOPPED')
		elif data_changed_flag[0] == 4:
			QMessageBox.warning(self, 'Message', 'Your Time Up.\n Now you cannot submit solution')
		else:
			with open("config.json", "r") as read_config:
				config = json.load(read_config)
			local_time = time.localtime()
			time_stamp = time.strftime("%H:%M:%S", local_time)
			textbox_value = ui_widgets.text_area.toPlainText()
			selected_language = str(ui_widgets.language_box.currentText())
			problem_code = config["Problems"][str(ui_widgets.problem_box.currentText())]
			if(selected_language == 'C'):
				extention = '.c'
				language_code = 'GCC'
			elif(selected_language == 'C++'):
				extention = '.cpp'
				language_code = 'CPP'
			elif(selected_language == 'JAVA'):
				extention = '.java'
				language_code = 'JVA'
			elif(selected_language == 'PYTHON-3'):
				extention = '.py'
				language_code = 'PY3'
			else:
				extention = '.py'
				language_code = 'PY2'
			local_id = manage_local_ids.get_new_id()
			client_id = config["client_id"]
			submission_management.insert_verdict(
				local_id,
				client_id,
				'-',
				'Queued',
				selected_language,
				language_code,
				problem_code,
				time_stamp,
				textbox_value,
				extention
				)
			print("no")
			data_changed_flag[1] = 1
			print('sachinam')
			send_code.solution_request(
				problem_code,
				selected_language,
				time_stamp,
				textbox_value,
				local_id
				)
			QMessageBox.warning(self, 'Message', 'Your Solution has been successfully send')
		return




	def show_problem(i,data_changed_flag,self):
		if data_changed_flag[0] == 0:
			QMessageBox.warning(self, 'Message', 'Contest not yet started.\nPlease wait.')
		else:
			webbrowser.open('Problems/Problem_'+str(i)+'.pdf')
		return
		# print('Button {0} clicked'.format(i))


	def sending(self,data_changed_flag):
		if data_changed_flag[0] == 0:
			QMessageBox.warning(self, 'Message', 'Contest not yet started.\nPlease wait.')
		elif data_changed_flag[0] == 3:
			QMessageBox.warning(self, 'Message', 'Contest has been STOPPED')
		elif data_changed_flag[0] == 4:
			QMessageBox.warning(self, 'Message', 'Your Time Up.\n Now you cannot submit any query')
		else:
			with open("config.json", "r") as read_config:
				config = json.load(read_config)
			client_id = config["client_id"]
			print(config["client_id"])
			query = ui_widgets.ask_query.text()
			if(query == ''):
				QMessageBox.warning(self, 'Message', "Query Cannot be empty")
				# print("Don't be stupid")
			elif(len(query) > 499):
				QMessageBox.warning(self, 'Message', "Length of query cannot exceed 500 words")
				# print('Length of query cannot exceed 500 words')
			else:
				query_management.insert_query(query,'Waiting for response')
				data_changed_flag[2] = 1
				send_code.query_request(
					client_id,
					query,
					)
		return
		
	###################################################################################




