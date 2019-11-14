import sys
import time
import socket
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import testing



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
		test_cases_table = QTableWidget()
		test_cases_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		# test_cases_table.setFixedHeight(650)
		test_cases_table.verticalHeader().setVisible(False)
		test_cases_table.setRowCount(row)
		test_cases_table.setColumnCount(column)
		test_cases_table.setHorizontalHeaderLabels(('Input', 'Output'))
		test_cases_table.horizontalHeader().setStretchLastSection(True)
		test_cases_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		upload = QPushButton('Upload')
		upload.setFixedSize(200, 50)
		upload.clicked.connect(lambda:self.upload_files())
		upload.setObjectName('submit')
		main.addWidget(problem_code)
		main.addWidget(time_limit)
		main.addWidget(test_cases_table)
		main.addWidget(upload, alignment=Qt.AlignRight)
		main.addStretch(0)
		main.addSpacing(1)

		main_widget = QWidget()
		main_widget.setLayout(main)
		main_widget.setObjectName('add_problem')
		return main_widget


	def upload_files(self):
		x = QFileDialog()
		x.setFileMode(QFileDialog.DirectoryOnly)
		x.setOption(QFileDialog.ShowDirsOnly, False)
		name = x.getExistingDirectory(self, 'Select Test Case Folder')
		print(name)
