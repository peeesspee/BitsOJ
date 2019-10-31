from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import problem_management




class problem_table():

	def problem_model(self):

		self.problem_table_model = self.manage_models(self.db, 'problems')

		self.problem_table_model.setHeaderData(0, Qt.Horizontal, 'No')
		self.problem_table_model.setHeaderData(1, Qt.Horizontal, 'Problem No')
		self.problem_table_model.setHeaderData(2, Qt.Horizontal, 'Problem Name')
		self.problem_table_model.setHeaderData(3, Qt.Horizontal, 'Problem Code')

		self.problem_table_view = self.generate_view(self.problem_table_model)

		return self.problem_table_view,self.problem_table_model


class add_problem_ui(QMainWindow):
	no = ''

	def __init__(self,no, table_model,client_config ,parent=None):
		super(add_problem_ui, self).__init__(parent)

		self.setWindowTitle('Add Problem')
		self.setFixedSize(800,400)
		add_problem_ui.no = no

		main = self.add_problem_view_ui(table_model,client_config)
		self.setCentralWidget(main)

		return

	def add_problem_view_ui(self,table_model,client_config):
		try:
			main = QVBoxLayout()
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
			problem_name.addWidget(problem_name_label)
			problem_name.addWidget(self.problem_name_text)
			problem_name_widget = QWidget()
			problem_name_widget.setLayout(problem_name)
			problem_code = QHBoxLayout()
			problem_code_label = QLabel('Problem Code : ')
			problem_code_label.setObjectName('general')
			self.problem_code_text = QLineEdit()
			self.problem_code_text.setPlaceholderText('Problem Code ')
			self.problem_code_text.setObjectName('general_text')
			self.problem_code_text.setFixedWidth(400)
			self.problem_code_text.setFixedHeight(50)
			problem_code.addWidget(problem_code_label)
			problem_code.addWidget(self.problem_code_text)
			problem_code_widget = QWidget()
			problem_code_widget.setLayout(problem_code)
			self.save = QPushButton('Save')
			self.save.setObjectName('general')
			self.save.setFixedSize(200,50)
			self.save.clicked.connect(lambda:self.save_data(table_model,client_config))

			main.addWidget(problem_no, alignment = Qt.AlignCenter)
			main.addWidget(problem_name_widget)
			main.addWidget(problem_code_widget)
			main.addWidget(self.save, alignment = Qt.AlignRight)
			main_widget = QWidget()
			main_widget.setLayout(main)
			main_widget.setObjectName('add_problem')
		except Exception as Error:
			print(str(Error))

		return main_widget

	def save_data(self,table_model,client_config):
		if self.problem_name_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Problem Name cannot be empty')
		elif self.problem_code_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Problem Code cannot be empty')
		else:
			problem_tuple = ()
			problem_tuple = (self.problem_name_text.text(), self.problem_code_text.text())
			client_config["Problems"]["Problem " + str(add_problem_ui.no)] = problem_tuple
			problem_management.insert_problem(str(add_problem_ui.no),self.problem_name_text.text(),self.problem_code_text.text())
			table_model.select()
			self.close()



class edit_problem_ui(QMainWindow):
	no = ''
	name = ''
	code = ''

	def __init__(self,no, name,code, table_model ,parent=None):
		super(edit_problem_ui, self).__init__(parent)

		self.setWindowTitle('Edit Problem')
		self.setFixedSize(800,400)
		edit_problem_ui.no = no
		edit_problem_ui.name = name
		edit_problem_ui.code = code

		main = self.edit_problem_view_ui(table_model)
		self.setCentralWidget(main)

		return

	def edit_problem_view_ui(self,table_model):
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
			self.save = QPushButton('Save')
			self.save.setObjectName('general')
			self.save.setFixedSize(200,50)
			self.save.clicked.connect(lambda:self.save_data(table_model))

			main.addWidget(problem_no, alignment = Qt.AlignCenter)
			main.addWidget(problem_name_widget)
			main.addWidget(problem_code_widget)
			main.addWidget(self.save, alignment = Qt.AlignRight)
			main_widget = QWidget()
			main_widget.setLayout(main)
			main_widget.setObjectName('add_problem')
		except Exception as Error:
			print(str(Error))

		return main_widget

	def save_data(self,table_model):
		if self.problem_name_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Problem Name cannot be empty')
		elif self.problem_code_text.text() == '':
			QMessageBox.warning(self, 'Message', 'Problem Code cannot be empty')
		else:
			problem_tuple = ()
			problem_tuple = (self.problem_name_text.text(), self.problem_code_text.text())
			client_config["Problems"]["Problem " + str(add_problem_ui.no)] = problem_tuple
			problem_management.update_problem(str(edit_problem_ui.no),self.problem_name_text.text(),self.problem_code_text.text())
			table_model.select()
			self.close()

