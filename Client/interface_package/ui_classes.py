from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase 
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, QSize, QRect
import os
import time
import json
# from manage_code import send_code


with open("config.json", "r") as read_config:
	config = json.load(read_config)


class ui_widgets():
	#############################################################################
	# Handle UI for various button presses
	def problems_ui(self):
		main_layout = QVBoxLayout() 
		heading = QLabel('Problems')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		var = {}
		for i in range(config["No_of_Problems"]):
			# print(config["Problems"][0])
			# print(type(config["Problems"][0]))
			# key, value = config["Problems"][0].items()
			# key = config["Problems"][0].keys()
			# print(key)
			var['Problem_{}'.format(i+1)] = QPushButton('Problem_'+str(i),self)
			print(type(var['Problem_{}'.format(i+1)]))
			main_layout.addWidget(var['Problem_{}'.format(i+1)])


		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def submissions_ui(self):
		heading = QLabel('My Submissions')
		heading.setObjectName('main_screen_heading')

		submission_model = self.manage_models(self.db, 'my_submissions')

		submission_model.setHeaderData(0, Qt.Horizontal, 'Run Id')
		submission_model.setHeaderData(1, Qt.Horizontal, 'Verdict')
		submission_model.setHeaderData(2, Qt.Horizontal, 'Source File')
		submission_model.setHeaderData(3, Qt.Horizontal, 'Language')
		submission_model.setHeaderData(4, Qt.Horizontal, 'Problem Code')
		submission_model.setHeaderData(5, Qt.Horizontal, 'Time')

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
		ui_widgets.problem_box.addItem("Problem 1")
		ui_widgets.problem_box.addItem("Problem 2")

		self.drop_down.addWidget(ui_widgets.language_box)
		self.drop_down.addWidget(ui_widgets.problem_box)
		self.drop_widget = QWidget()
		self.drop_widget.setLayout(self.drop_down)

		ui_widgets.text_area = QTextEdit()
		ui_widgets.text_area.setFixedHeight(700)
		ui_widgets.text_area.setObjectName('text_area_content')
		ui_widgets.text_area.setPlaceholderText('Paste your code here')

		self.horizontal_layout = QHBoxLayout()
		self.submit_solution = QPushButton('Submit', self)
		self.submit_solution.setObjectName('submit')
		self.submit_solution.setFixedSize(200, 50)
		print(type(self.submit_solution))
		self.submit_solution.clicked.connect(ui_widgets.submit_call)
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
		heading = QLabel('Page4')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def leaderboard_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page5')
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



	def submit_call(self):
		local_time = time.localtime()
		time_stamp = time.strftime("%H:%M:%S", local_time)
		textbox_value = ui_widgets.text_area.toPlainText()
		selected_language = str(ui_widgets.language_box.currentText())
		print(time_stamp)
		print(textbox_value)
		print(str(ui_widgets.language_box.currentText()))


	###################################################################################


