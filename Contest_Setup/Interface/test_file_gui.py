import sys
import time
import socket
import json
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import testing
from init_setup import read_write



class test_file(QMainWindow):

	def __init__(self, selected_row, selected_model, parent=None):
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
		main = self.main_ui()
		self.setCentralWidget(main)

	def main_ui(self):
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
		upload = QPushButton('Upload')
		upload.setFixedSize(200, 50)
		upload.clicked.connect(lambda:self.upload_files('Problem ' + str(self.no)))
		upload.setObjectName('submit')
		main.addWidget(problem_code)
		main.addWidget(time_limit)
		main.addWidget(self.test_cases_table)
		main.addWidget(upload, alignment=Qt.AlignRight)
		main.addStretch(0)
		main.addSpacing(1)

		main_widget = QWidget()
		main_widget.setLayout(main)
		main_widget.setObjectName('add_problem')
		return main_widget


	def upload_files(self,index):
		self.input = []
		self.output = []
		x = QFileDialog()
		x.setFileMode(QFileDialog.DirectoryOnly)
		x.setOption(QFileDialog.ShowDirsOnly, False)
		name = x.getExistingDirectory(self, 'Select Test Case Folder')
		self.data["Problems"]["Problem " + str(self.no)]["Test File Path"] = name
		for i in os.listdir(name):
			if i.endswith(".in"):
				self.input.append(i)
			if i.endswith(".ans"):
				self.output.append(i)
		self.input.sort()
		self.output.sort()
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
		print(name)
