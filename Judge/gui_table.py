import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QCursor, QFont, QColor 
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, QSize, QRect


class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = 'All Judgements'
		self.left = 0
		self.top = 0
		self.width = 1200
		self.height = 800
		self.db = self.init_qt_database()
		

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

		# view_judgements_button = QPushButton('View judgements')
		# view_judgements_button.setFixedSize(200, 50)
		# view_judgements_button.clicked.connect(lambda: self.view_judgements(judgements_table.selectionModel().currentIndex().row()))
		# view_judgements_button.setObjectName('submit')

		judgements_model = self.judgements_models(self.db, 'verdict')

		
		judgements_model.setHeaderData(0, Qt.Horizontal, 'Run ID')
		judgements_model.setHeaderData(1, Qt.Horizontal, 'Client ID')
		judgements_model.setHeaderData(2, Qt.Horizontal, 'Verdict')
		judgements_model.setHeaderData(3, Qt.Horizontal, 'Language')
		judgements_model.setHeaderData(4, Qt.Horizontal, 'Problem Code')
		judgements_model.setHeaderData(5, Qt.Horizontal, 'Time Stamp')

		judgements_table = self.generate_view(judgements_model)
		# judgements_table.doubleClicked.connect(
		# 	lambda: self.view_judgements(
		# 		judgements_table.selectionModel().currentIndex().row()
		# 		))


		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		# head_layout.addWidget(view_judgements_button,  alignment=Qt.AlignRight)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)


		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(judgements_table)
		main_layout.setStretch(0, 5)
		main_layout.setStretch(1, 95)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")
		main.show()
		return main, judgements_model

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


	@pyqtSlot()
	def on_click(self):
		print("\n")
		for currentQTableWidgetItem in self.tableWidget.selectedItems():
			print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(open('Assets/style.qss', "r").read())
	ex = App()
	sys.exit(app.exec_())