import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import problem_management
from Interface.test_file_gui import test_file
from init_setup import read_write




class problem_table():

	def problem_model(self):

		self.problem_table_model = self.manage_models(self.db, 'problems')

		self.problem_table_model.setHeaderData(0, Qt.Horizontal, 'No')
		self.problem_table_model.setHeaderData(1, Qt.Horizontal, 'Problem No')
		self.problem_table_model.setHeaderData(2, Qt.Horizontal, 'Problem Name')
		self.problem_table_model.setHeaderData(3, Qt.Horizontal, 'Problem Code')
		self.problem_table_model.setHeaderData(4, Qt.Horizontal, 'Time Limit')

		problem_table_view = self.generate_view(self.problem_table_model)

		problem_table_view.doubleClicked.connect(
			lambda : problem_table.add_test_cases(
				self,
				problem_table_view.selectionModel().currentIndex().row()
				))

		return problem_table_view,self.problem_table_model

	def add_test_cases(self,selected_row):
		self.test_file_ui = test_file(selected_row,self.problem_table_model)
		self.test_file_ui.show()


class add_problem_ui(QMainWindow):
	no = ''

	def __init__(self,no, table_model,client_config, data ,parent=None):
		super(add_problem_ui, self).__init__(parent)

		self.setWindowTitle('Add Problem')
		self.setFixedSize(1600,800)
		add_problem_ui.no = no

		main = self.add_problem_view_ui(table_model,client_config,data)
		self.setCentralWidget(main)

		return

	def add_problem_view_ui(self,table_model,client_config,data):
		try:
			main = QVBoxLayout()
			main2 = QScrollArea()
			problem_no = QLabel('Problem ' + str(add_problem_ui.no))
			problem_no.setObjectName('general')
			problem_name = QHBoxLayout()
			problem_name_label = QLabel('Problem Name : ')
			problem_name_label.setObjectName('general')
			self.problem_name_text = QLineEdit()
			self.problem_name_text.setPlaceholderText('Problem Name ')
			self.problem_name_text.setObjectName('general_text')
			self.problem_name_text.setFixedWidth(400)
			self.problem_name_text.setFixedHeight(50)
			problem_code_label = QLabel('Problem Code : ')
			problem_code_label.setObjectName('general')
			self.problem_code_text = QLineEdit()
			self.problem_code_text.setPlaceholderText('Problem Code ')
			self.problem_code_text.setObjectName('general_text')
			self.problem_code_text.setFixedWidth(400)
			self.problem_code_text.setFixedHeight(50)
			problem_name.addWidget(problem_name_label)
			problem_name.addWidget(self.problem_name_text)
			problem_name.addStretch(0)
			problem_name.addSpacing(1)
			problem_name.addWidget(problem_code_label)
			problem_name.addWidget(self.problem_code_text)
			problem_name.addStretch(0)
			problem_name.addSpacing(1)
			problem_name_widget = QWidget()
			problem_name_widget.setLayout(problem_name)
			time_limit = QHBoxLayout()
			time_limit_label = QLabel('Time Limit        : ')
			time_limit_label.setObjectName('general')
			self.time_limit_text = QLineEdit()
			self.time_limit_text.setPlaceholderText('Time Limit ')
			self.time_limit_text.setObjectName('general_text')
			self.time_limit_text.setFixedWidth(400)
			self.time_limit_text.setFixedHeight(50)
			author_label = QLabel('Author Name : ')
			author_label.setObjectName('general')
			self.author_text = QLineEdit()
			self.author_text.setPlaceholderText('Author Name ')
			self.author_text.setObjectName('general_text')
			self.author_text.setFixedWidth(400)
			self.author_text.setFixedHeight(50)
			time_limit.addWidget(time_limit_label)
			time_limit.addWidget(self.time_limit_text)
			time_limit.addStretch(0)
			time_limit.addSpacing(1)
			time_limit.addWidget(author_label)
			time_limit.addWidget(self.author_text)
			time_limit.addStretch(0)
			time_limit.addSpacing(1)
			time_limit_widget = QWidget()
			time_limit_widget.setLayout(time_limit)
			problem_statement_label = QLabel('Problem')
			problem_statement_label.setObjectName('general2')
			self.problem_statement_text = QPlainTextEdit()
			self.problem_statement_text.setFixedSize(1500,500)
			self.problem_statement_text.setObjectName('general_text2')
			input_label = QLabel('Input: ')
			input_label.setObjectName('general2')
			self.input_text = QPlainTextEdit()
			self.input_text.setFixedSize(1500,200)
			self.input_text.setObjectName('general_text2')
			output_label = QLabel('Output: ')
			output_label.setObjectName('general2')
			self.output_text = QPlainTextEdit()
			self.output_text.setFixedSize(1500,200)
			self.output_text.setObjectName('general_text2')
			constraints_label = QLabel('Constraints: ')
			constraints_label.setObjectName('general2')
			self.constraints_text = QPlainTextEdit()
			self.constraints_text.setFixedSize(1500,200)
			self.constraints_text.setObjectName('general_text2')
			example_label = QLabel('Example: ')
			example_label.setObjectName('general2')
			example_input_label = QLabel('Example Input: ')
			example_input_label.setObjectName('general3')
			self.example_input_text = QPlainTextEdit()
			self.example_input_text.setFixedSize(1200,200)
			self.example_input_text.setObjectName('general_text3')
			example_output_label = QLabel('Example Output: ')
			example_output_label.setObjectName('general3')
			self.example_output_text = QPlainTextEdit()
			self.example_output_text.setFixedSize(1200,200)
			self.example_output_text.setObjectName('general_text3')
			self.save = QPushButton('Save')
			self.save.setObjectName('general')
			self.save.setFixedSize(200,50)
			self.save.clicked.connect(lambda:self.save_data(table_model,client_config,data))

			main.addWidget(problem_no, alignment = Qt.AlignCenter)
			main.addWidget(problem_name_widget)
			main.addWidget(time_limit_widget)
			main.addWidget(problem_statement_label)
			main.addWidget(self.problem_statement_text)
			main.addWidget(input_label)
			main.addWidget(self.input_text)
			main.addWidget(output_label)
			main.addWidget(self.output_text)
			main.addWidget(constraints_label)
			main.addWidget(self.constraints_text)
			main.addWidget(example_label)
			main.addWidget(example_input_label)
			main.addWidget(self.example_input_text)
			main.addWidget(example_output_label)
			main.addWidget(self.example_output_text)
			main.addStretch(0)
			main.addSpacing(1)
			main.addWidget(self.save, alignment = Qt.AlignRight)
			main_widget = QWidget()
			main_widget.setLayout(main)
			main_widget.setObjectName('add_problem')
			main2.setWidget(main_widget)
			main2.setWidgetResizable(True)
			main2.setFixedHeight(780)
			layout = QVBoxLayout()
			layout.addWidget(main2)
			main_layout = QWidget()
			main_layout.setLayout(layout)
		except Exception as Error:
			print(str(Error))

		return main_layout

	def save_data(self,table_model,client_config,data):
		if self.problem_name_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Problem Name cannot be empty')
		elif self.problem_code_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Problem Code cannot be empty')
		elif self.time_limit_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Time Limit cannot be empty')
		else:
			os.system('mkdir Problems/' + self.problem_code_text.text())
			problem_tuple = ()
			problem_tuple = (self.problem_name_text.text(), self.problem_code_text.text(),self.time_limit_text.text())
			client_config["Problems"]["Problem " + str(add_problem_ui.no)] = problem_tuple
			try:
				random_dict = {}
				random_dict["Test File Path"] = 'Null'
				random_dict["Input File"] = 'Null'
				random_dict["Output File"] = 'Null'
				data["Problems"]['Problem ' + str(add_problem_ui.no)] = random_dict
			except Exception as Error:
				print(str(Error))
			read_write.write_json(data)
			problem_management.insert_problem(str(add_problem_ui.no),self.problem_name_text.text(),self.problem_code_text.text(),self.time_limit_text.text())
			try:
				problem = {
					"Problem Name" : self.problem_name_text.text(),
					"Problem Code" : self.problem_code_text.text(),
					"Time Limit" : self.time_limit_text.text(),
					"Author Name" : self.author_text.text(),
					"Problem Statement" : self.problem_statement_text.toPlainText(),
					"Input" : self.input_text.toPlainText(),
					"Output" : self.output_text.toPlainText(),
					"Constraints" : self.constraints_text.toPlainText(),
					"Example Input" : self.example_input_text.toPlainText(),
					"Example Output" : self.example_output_text.toPlainText()
				}
				with open('./Problem_Statement/Problem_' + str(add_problem_ui.no) + '.json', 'w') as write:
					json.dump(problem, write, indent = 4)
			except Exception as Error:
				print(str(Error))
			table_model.select()
			self.close()



class edit_problem_ui(QMainWindow):
	no = ''
	name = ''
	code = ''

	def __init__(self,no, name,code, table_model, client_config ,parent=None):
		super(edit_problem_ui, self).__init__(parent)

		self.setWindowTitle('Edit Problem')
		self.setFixedSize(800,400)
		edit_problem_ui.no = no
		edit_problem_ui.name = name
		edit_problem_ui.code = code

		main = self.edit_problem_view_ui(table_model, client_config)
		self.setCentralWidget(main)

		return

	def edit_problem_view_ui(self, table_model, client_config):
		try:
			main = QVBoxLayout()
			problem_no = QLabel('Problem ' + str(edit_problem_ui.no))
			problem_no.setObjectName('general')
			problem_name = QHBoxLayout()
			problem_name_label = QLabel('Problem Name : ')
			problem_name_label.setObjectName('general')
			self.problem_name_text = QLineEdit()
			self.problem_name_text.setPlaceholderText('Problem Name ')
			self.problem_name_text.setText(edit_problem_ui.name)
			self.problem_name_text.setObjectName('general_text')
			self.problem_name_text.setFixedWidth(400)
			self.problem_name_text.setFixedHeight(50)
			problem_name.addWidget(problem_name_label)
			problem_name.addWidget(self.problem_name_text)
			problem_name_widget = QWidget()
			problem_name_widget.setLayout(problem_name)
			problem_code = QHBoxLayout()
			problem_code_label = QLabel('Problem Code : ')
			problem_code_label.setObjectName('general')
			self.problem_code_text = QLineEdit()
			self.problem_code_text.setPlaceholderText('Problem Code ')
			self.problem_code_text.setText(edit_problem_ui.code)
			self.problem_code_text.setObjectName('general_text')
			self.problem_code_text.setFixedWidth(400)
			self.problem_code_text.setFixedHeight(50)
			problem_code.addWidget(problem_code_label)
			problem_code.addWidget(self.problem_code_text)
			problem_code_widget = QWidget()
			problem_code_widget.setLayout(problem_code)
			time_limit = QHBoxLayout()
			time_limit_label = QLabel('Time Limit  : ')
			time_limit_label.setObjectName('general')
			self.time_limit_text = QLineEdit()
			self.time_limit_text.setPlaceholderText('Time Limit ')
			self.time_limit_text.setObjectName('general_text')
			self.time_limit_text.setFixedWidth(400)
			self.time_limit_text.setFixedHeight(50)
			time_limit.addWidget(time_limit_label)
			time_limit.addWidget(self.time_limit_text)
			time_limit_widget = QWidget()
			time_limit_widget.setLayout(time_limit)
			self.save = QPushButton('Save')
			self.save.setObjectName('general')
			self.save.setFixedSize(200,50)
			self.save.clicked.connect(lambda:self.save_data(table_model, client_config))

			main.addWidget(problem_no, alignment = Qt.AlignCenter)
			main.addWidget(problem_name_widget)
			main.addWidget(problem_code_widget)
			main.addWidget(time_limit_widget)
			main.addWidget(self.save, alignment = Qt.AlignRight)
			main_widget = QWidget()
			main_widget.setLayout(main)
			main_widget.setObjectName('add_problem')
			self.previous_code = self.problem_code_text.text()
		except Exception as Error:
			print(str(Error))

		return main_widget

	def save_data(self,table_model, client_config):
		if self.problem_name_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Problem Name cannot be empty')
		elif self.problem_code_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Problem Code cannot be empty')
		elif self.time_limit_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Time Limit cannot be empty')
		else:
			os.system('mkdir Problems/' + self.problem_code_text.text())
			os.system('rm -rf Problems/' + self.previous_code)
			problem_tuple = ()
			problem_tuple = (self.problem_name_text.text(), self.problem_code_text.text(),self.time_limit_text.text())
			client_config["Problems"]["Problem " + str(add_problem_ui.no)] = problem_tuple
			problem_management.update_problem(str(edit_problem_ui.no),self.problem_name_text.text(),self.problem_code_text.text(),self.time_limit_text.text())
			table_model.select()
			self.close()


