import sys
import time
import socket
import json
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, QRect
from database_management import testing
from init_setup import read_write
from shutil import copyfile
from Interface.ui_classes import view_case_ui
from judge_api import judge



class test_file(QMainWindow):

	def __init__(self, selected_row, selected_model, server_config, parent=None):
		super(test_file, self).__init__(parent)

		self.data = testing.get_testing_details()
		self.selected_model = selected_model
		self.setWindowIcon(QIcon('../Elements/logo.png'))
		try:
			self.no = self.selected_model.index(selected_row, 0).data()
			self.problem_no = self.selected_model.index(selected_row, 1).data()
			self.problem_name = self.selected_model.index(selected_row, 2).data()
			self.problem_code = self.selected_model.index(selected_row, 3).data()
			self.time_limit = self.selected_model.index(selected_row, 4).data()
		except Exception as Error:
			print(str(Error))
		self.setWindowTitle('Test files')
		self.input = []
		self.output = []
		self.setFixedSize(1200,800)
		main = self.main_ui(server_config)
		self.setCentralWidget(main)

	def main_ui(self,server_config):
		main = QVBoxLayout()
		problem_no_label = QLabel(self.problem_name)
		problem_no_label.setObjectName('heading')
		problem_code = QLabel('Problem Code : ' + self.problem_code)
		time_limit = QLabel('Time Limit        : ' + str(self.time_limit) + ' second')		
		main.addWidget(problem_no_label, alignment = Qt.AlignCenter)
		problem_code.setObjectName('heading2')
		time_limit.setObjectName('heading2')
		row = 0
		column = 2
		self.test_cases_table = QTableWidget()
		self.test_cases_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.test_cases_table.verticalHeader().setVisible(False)
		self.data = read_write.read_json()
		if self.data["Problems"]["Problem "+str(self.no)]["Test File Path"] == 'Null':
			self.test_cases_table.setRowCount(row)
			self.test_cases_table.setColumnCount(column)
		else:
			self.test_cases_table.setRowCount(len(self.data["Problems"]["Problem " + str(self.no)]["Input File"]))
			self.test_cases_table.setColumnCount(column)
			name = self.data["Problems"]["Problem " + str(self.no)]["Test File Path"]
			self.input = self.data["Problems"]["Problem " + str(self.no)]["Input File"]
			self.output = self.data["Problems"]["Problem " + str(self.no)]["Output File"]
			self.test_cases_table.setRowCount(len(self.input))
			for i in range(len(self.input)):
				for j in range(2):
					if j == 0:
						self.test_cases_table.setItem(i,j, QTableWidgetItem(str(self.input[i])))
					if j == 1:
						self.test_cases_table.setItem(i,j, QTableWidgetItem(str(self.output[i])))
		self.test_cases_table.setHorizontalHeaderLabels(('Input', 'Output'))
		self.test_cases_table.horizontalHeader().setStretchLastSection(True)
		self.test_cases_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.test_cases_table.cellDoubleClicked.connect(
			lambda:self.view_files(
				self.test_cases_table.selectionModel().currentIndex().row(),
				self.test_cases_table.selectionModel().currentIndex().column()
				))

		solutions = QHBoxLayout()
		upload = QPushButton('Upload')
		upload.setFixedSize(200, 50)
		upload.clicked.connect(lambda:self.upload_files('Problem ' + str(self.no),server_config))
		upload.setObjectName('submit')
		self.check_solution_text = QLineEdit()
		self.check_solution_text.setPlaceholderText('Solution Path')
		self.check_solution_text.setObjectName('general_text')
		self.check_solution_text.setFixedWidth(400)
		self.check_solution_text.setFixedHeight(50)
		self.check_solution_text.setReadOnly(True)
		self.problem_box = QComboBox()
		self.problem_box.setGeometry(QRect(10, 10, 491, 31))
		self.problem_box.setFixedWidth(250)
		self.problem_box.setFixedHeight(40)
		self.problem_box.setObjectName("language_box_content")
		self.problem_box.addItem('C')
		self.problem_box.addItem('C++')
		self.problem_box.addItem('PYTHON 2')
		self.problem_box.addItem('PYTHON 3')
		self.problem_box.addItem('JAVA')
		self.problem_box.addItem('TEXT')
		Solution = QPushButton('Solution')
		Solution.setFixedSize(200, 50)
		Solution.clicked.connect(lambda:self.solution_files())
		Solution.setObjectName('submit')
		check = QPushButton('check')
		check.setFixedSize(200, 50)
		check.clicked.connect(lambda:self.check_files())
		check.setObjectName('submit')
		self.result_label = QLabel('')
		solutions.addWidget(self.check_solution_text)
		solutions.addWidget(Solution)
		solutions.addWidget(check)
		solutions.addStretch(0)
		solutions.addSpacing(1)
		solutions.addWidget(self.result_label, alignment = Qt.AlignCenter)
		solution_widget = QWidget()
		solution_widget.setLayout(solutions)
		main.addWidget(problem_code)
		main.addWidget(time_limit)
		main.addWidget(self.test_cases_table)
		main.addWidget(upload, alignment=Qt.AlignRight)
		main.addWidget(self.problem_box)
		main.addWidget(solution_widget)
		main.addStretch(0)
		main.addSpacing(1)
		main_widget = QWidget()
		main_widget.setLayout(main)
		main_widget.setObjectName('add_problem')
		return main_widget



	def view_files(self,row,column):
		print(row)
		print(column)
		name = self.test_cases_table.item(row,column)
		name = name.text()
		print(name)
		print(type(name))
		if column == 0:
			# Input file is selected
			file_path = "./Problems/" + self.problem_code + '/' + name
			self.ui = view_case_ui(
				file_path
			)
			self.ui.show()
		elif column == 1:
			# Output file is selected
			file_path = "./Problems/" + self.problem_code + '/' + name
			self.ui = view_case_ui(
				file_path
			)
			self.ui.show()
	
		# elif column == 2:
		# 	print("Disable File " + str(row) + " for problem " + problem_code)
		return


	def solution_files(self):
		try:
			x = QFileDialog()
			options = QFileDialog.Options()
			options |= QFileDialog.DontUseNativeDialog
			self.fileName, _ = QFileDialog.getOpenFileName(self,"Select Correct Solution", "","All Files (*);;Python Files (*.py)", options=options)
			if self.fileName:
				l = self.fileName.split('/')
				length = len(l)
				self.check_solution_text.setText(l[length - 1])
				self.check_solution_text.setReadOnly(True)
				copyfile(self.fileName,'./Problems/' + self.problem_code + '/' + l[length - 1])
			else:
				return
		except Exception as Error:
			print(str(Error))

	def check_files(self):
		result = judge.main(
			self.problem_box.currentText(),
			self.problem_code,
			self.time_limit,
			self.fileName
			)
		try:
			if result == 'AC':
				self.result_label.setText(result)
				self.result_label.setObjectName('view1')
			else:
				self.result_label.setText(result)
				self.result_label.setObjectName('view2')
		except Exception as Error:
			print(str(Error))


	def upload_files(self,index,server_config):
		self.count = 0
		self.input = []
		self.output = []
		x = QFileDialog()
		x.setFileMode(QFileDialog.DirectoryOnly)
		x.setOption(QFileDialog.ShowDirsOnly, False)
		name = x.getExistingDirectory(self, 'Select Test Case Folder')
		if name != '':
			for i in os.listdir('./Problems/'+self.problem_code+'/'):
				os.remove('./Problems/'+self.problem_code+'/' + i)
			self.data["Problems"]["Problem " + str(self.no)]["Test File Path"] = name
			for i in os.listdir(name):
				if i.endswith(".in"):
					self.count+=1
					self.input.append(i)
				if i.endswith(".ans"):
					self.output.append(i)
			server_config["Problems"]["Problem "+str(self.no)]["IO Files"] = self.count
			self.input.sort()
			self.output.sort()
			try:
				for i in range(len(self.input)):
					dest = ["{0:02}".format(i)]
					copyfile(name + '/' + self.input[i],'./Problems/' + self.problem_code + '/input' + dest[0] + '.in')
					self.input[i] = 'input' + dest[0] + '.in'
					copyfile(name + '/' + self.output[i],'./Problems/' + self.problem_code + '/output' + dest[0] + '.ans')
					self.output[i] = 'output' + dest[0] + '.ans'
				self.data["Problems"]["Problem " + str(self.no)]["Test File Path"] = './Problems/' + self.problem_code
				self.data["Problems"]["Problem " + str(self.no)]["Input File"] = self.input
				self.data["Problems"]["Problem " + str(self.no)]["Output File"] = self.output
				self.test_cases_table.setRowCount(len(self.input))
				for i in range(len(self.input)):
					for j in range(2):
						if j == 0:
							self.test_cases_table.setItem(i,j, QTableWidgetItem(str(self.input[i])))
						if j == 1:
							self.test_cases_table.setItem(i,j, QTableWidgetItem(str(self.output[i])))
				read_write.write_json(self.data)
			except Exception as Error:
				QMessageBox.warning(self, 'Message', str(Error))
		else:
			return
