import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QCursor, QFont, QColor 
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, QSize, QRect
from database import manage_database


class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = 'All Judgements'
		self.left = 0
		self.top = 0
		self.width = 1200
		self.height = 800
		self.db = self.init_qt_database()
		manage_database.initialize_database()
		

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.timer = QTimer()
		self.change_flag = True
		self.timer.timeout.connect(self.update_data)
		self.timer.start(1000)

		main, self.table = self.judgements_ui()
		self.setCentralWidget(main)
		self.show()

	def update_data(self):
		try:
			self.table.setQuery("SELECT run_id,client_id,verdict,language,p_code,time_stamp FROM verdict ORDER BY run_id")
		except Exception as error:
			print(str(error))

	def judgements_ui(self):
		heading = QLabel('All Judgements')
		heading.setObjectName('main_screen_heading')

		judgements_model = self.judgements_models(self.db, 'verdict')

		
		judgements_model.setHeaderData(0, Qt.Horizontal, 'Run ID')
		judgements_model.setHeaderData(1, Qt.Horizontal, 'Client ID')
		judgements_model.setHeaderData(2, Qt.Horizontal, 'Verdict')
		judgements_model.setHeaderData(3, Qt.Horizontal, 'Language')
		judgements_model.setHeaderData(4, Qt.Horizontal, 'Problem Code')
		judgements_model.setHeaderData(5, Qt.Horizontal, 'Time Stamp')

		judgements_table = self.generate_view(judgements_model)
		judgements_table.doubleClicked.connect(
			lambda: self.view_judgements(
				judgements_table.selectionModel().currentIndex().row()
				))


		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)


		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget, alignment = Qt.AlignCenter)
		main_layout.addWidget(judgements_table)
		main_layout.setStretch(0, 5)
		main_layout.setStretch(1, 95)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")
		main.show()
		return main, judgements_model


	def view_judgements(self,selected_row):
		run_id = self.table.index(selected_row, 0).data()
		verdict = self.table.index(selected_row, 0).data()
		language = self.table.index(selected_row, 0).data()
		# source = manage_database.get_source(run_id)
		source = './check/4_14.c'
		try:
			self.window = view_source_ui(run_id, verdict, language, source)
			self.window.show()
		except Exception as Error:
			print(str(Error))

	def init_qt_database(self):
		try:
			db = QSqlDatabase.addDatabase('QSQLITE')
			db.setDatabaseName('judge_database.db')
			return db
		except:
			print('[ CRITICAL ] Database loading error......')

	def judgements_models(self,db, table_name):
		if db.open():
			model = QSqlQueryModel()
			model.setQuery("SELECT run_id,client_id,verdict,language,p_code,time_stamp FROM verdict ORDER BY run_id")
		return model


	def generate_view(self, model):
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
		#vertical_header.setSectionResizeMode(QHeaderView.Stretch)
		vertical_header.setVisible(False)
		return table


class view_source_ui(QMainWindow):

	def __init__(self, run_id, verdict, language, source, parent=None):
		super(view_source_ui,self).__init__(parent)
		self.setWindowTitle('Run ID : '+ str(run_id))
		self.setFixedSize(800,600)

		main = self.main_view_source_ui(verdict, language, source)
		self.setCentralWidget(main)

		return

	def main_view_source_ui(self, verdict_show, language_show, source):
		with open(source, 'r') as sol:
			data = sol.read()

		heading = QLabel('Source Code : ')
		heading.setObjectName('source_heading')

		cursor = QTextCursor()
		cursor.setPosition(0)

		submission_text = QPlainTextEdit()
		submission_text.appendPlainText(data)
		submission_text.setReadOnly(True)
		submission_text.setTextCursor(cursor)
		# submission_text.cursorForPosition(0)
		# submission_text.QCursor.pos(0)
		print(verdict_show)

		bottom_layout = QHBoxLayout()
		verdict = QLabel("Judge's Verdict :")
		verdict_layout = QLabel(verdict_show)
		language = QLabel('Language : ')
		language_layout = QLabel(language_show)
		bottom_layout.addWidget(verdict)
		bottom_layout.addWidget(verdict_layout)
		bottom_layout.addWidget(language)
		bottom_layout.addWidget(language_layout)
		bottom_widget = QWidget()
		bottom_widget.setLayout(bottom_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(submission_text)
		main_layout.addWidget(bottom_widget)
		main = QWidget()
		main.setLayout(main_layout)


		submission_text.setObjectName('text')
		verdict.setObjectName('view')
		if verdict == 'AC':
			verdict_layout.setObjectName('view1')
		else:
			verdict_layout.setObjectName('view2')
		language.setObjectName('view')
		language_layout.setObjectName('view3')
		main.setObjectName('query_submission_widget')

		return main

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(open('Assets/style.qss', "r").read())
	ex = App()
	sys.exit(app.exec_())