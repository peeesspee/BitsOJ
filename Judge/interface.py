import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QCursor, QFont, QColor 
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, QSize, QRect
from submission_ui import submission_ui
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler)
 
class judge_window(QMainWindow):
	def __init__(self, data_flags):
		super().__init__()
		self.setWindowIcon(QIcon('./Assets/logo.png'))
		self.setWindowTitle('BitsOJ v1.0.1 [ JUDGE ]')
		self.data_flags = data_flags
		self.left = 0
		self.top = 0
		self.width = 1024
		self.height = 768
		self.resize(1024, 768)
		self.db = self.init_qt_database()
		
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.timer = QTimer()
		self.change_flag = True
		self.timer.timeout.connect(self.update_data)
		self.timer.start(1000)

		main, self.table = self.judgements_ui()
		self.setCentralWidget(main)
		
	def update_data(self):
		try:
			if self.data_flags[4] == 1:
				self.data_flags[4] = 0
				self.table.setQuery(
					"SELECT run_id, client_id, verdict, language, p_code, time_stamp FROM verdict ORDER BY run_id DESC"
				)
				print('[ UI ] Refresh...')

			if self.data_flags[7] == 1:
				# Disconnected by Server
				info_box = QMessageBox()
				info_box.setIcon(QMessageBox.Information)
				info_box.setWindowTitle('Alert')
				info_box.setText('Disconnected by Server')
				info_box.setStandardButtons(QMessageBox.Ok)
				info_box.exec_()
				self.close()

			if self.data_flags[8] == 1:
				# Disconnected by Server
				info_box = QMessageBox()
				info_box.setIcon(QMessageBox.Critical)
				info_box.setWindowTitle('Alert')
				info_box.setText('Blocked by Server')
				info_box.setStandardButtons(QMessageBox.Ok)
				info_box.exec_()
				self.close()

		except Exception as error:
			print('[ UI ][ ERROR ]' + str(error))

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
			)
		)

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

	def view_judgements(self, selected_row):
		run_id = self.table.index(selected_row, 0).data()
		client_id = self.table.index(selected_row, 1).data()
		verdict = self.table.index(selected_row, 2).data()
		language = self.table.index(selected_row, 3).data()
		p_code = self.table.index(selected_row, 4).data()
		time_stamp = self.table.index(selected_row, 5).data()

		source = 'run1.cpp'
		# source = manage_database.get_source(run_id)
		try:
			self.window = submission_ui(
				run_id, 
				client_id,
				verdict, 
				language, 
				p_code,
				time_stamp,
				source
			)
			self.window.show()
		except Exception as Error:
			print('[ JUDGE ][ ERROR ] : ' + str(Error))

	def init_qt_database(self):
		try:
			db = QSqlDatabase.addDatabase('QSQLITE')
			db.setDatabaseName('judge_database.db')
			return db
		except:
			print('[ UI ][ CRITICAL ] Database loading error......')

	def judgements_models(self, db, table_name):
		if db.open():
			model = QSqlQueryModel()
			query = "SELECT run_id, client_id, verdict, language, p_code, time_stamp FROM " + table_name + " ORDER BY run_id DESC"
			model.setQuery(query)
		return model


	def generate_view(self, model):
		table = QTableView() 
		table.setModel(model)
		# Enable sorting in the table view 
		table.setSortingEnabled(False)
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
		vertical_header.setVisible(False)
		return table

	def closeEvent(self, event):
		print('[ SYSTEM EXIT ]')
		self.data_flags[5] = 1
		event.accept()
		
class main_interface(judge_window):
	def __init__(self, data_flags):
		# make a reference of judge_window class
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('Assets/style.qss', "r").read())
		app.aboutToQuit.connect(self.closeEvent)
		judge_app = judge_window(data_flags)
		judge_app.show()
		# Execute the app mainloop
		app.exec_()
		return