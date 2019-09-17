import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler


global current_status 
current_status = "STOPPED"

# This is to ignore some warnings which were thrown when gui exited and python deleted some assests in wrong order
# Nothing critical 
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler)

class server_window(QMainWindow):
	def __init__(self, data_changed_flags2):
		super().__init__()
		# Set app icon
		self.setWindowIcon(QIcon('Elements/logo.png'))
		# Set window title
		self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ]')
		# Make  the app run full-screen
		# Initialize status bar (Bottom Bar)
		self.status = self.statusBar()
		self.resize(800, 600)

		self.timer = QTimer()
		self.change_flag = True
		self.timer.timeout.connect(self.update_data)
		self.timer.start(2000)
		
		# make data_changed_flag accessible from the class methods
		self.data_changed_flags = data_changed_flags2
		
		###########################################################
		self.db = self.init_qt_database()
		###########################################################
		# Define Sidebar Buttons and their actions
		button_width = 200
		button_height = 50

		self.button_1 = QPushButton('Submissions', self)
		self.button_1.setFixedSize(button_width, button_height)
		self.button_1.clicked.connect(self.view_submissions)
		self.button_1.setObjectName("sidebar_button")

		self.button_2 = QPushButton('Judges', self)
		self.button_2.setFixedSize(button_width, button_height)
		self.button_2.clicked.connect(self.manage_judges)
		self.button_2.setObjectName("sidebar_button")

		self.button_3 = QPushButton('Clients', self)
		self.button_3.setFixedSize(button_width, button_height)
		self.button_3.clicked.connect(self.manage_clients)
		self.button_3.setObjectName("sidebar_button")

		self.button_4 = QPushButton('Queries', self)
		self.button_4.setFixedSize(button_width, button_height)
		self.button_4.clicked.connect(self.manage_queries)
		self.button_4.setObjectName("sidebar_button")

		self.button_5 = QPushButton('Leaderboard', self)
		self.button_5.setFixedSize(button_width, button_height)
		self.button_5.clicked.connect(self.manage_leaderboard)
		self.button_5.setObjectName("sidebar_button")

		self.button_6 = QPushButton('Problems', self)
		self.button_6.setFixedSize(button_width, button_height)
		self.button_6.clicked.connect(self.manage_problems)
		self.button_6.setObjectName("sidebar_button")

		self.button_7 = QPushButton('Languages', self)
		self.button_7.setFixedSize(button_width, button_height)
		self.button_7.clicked.connect(self.manage_languages)
		self.button_7.setObjectName("sidebar_button")

		self.button_8 = QPushButton('Statistics', self)
		self.button_8.setFixedSize(button_width, button_height)
		self.button_8.clicked.connect(self.show_stats)
		self.button_8.setObjectName("sidebar_button")

		self.button_9 = QPushButton('Settings', self)
		self.button_9.setFixedSize(button_width, button_height)
		self.button_9.clicked.connect(self.contest_settings)
		self.button_9.setObjectName("sidebar_button")

		self.button_10 = QPushButton('Generate Report', self)
		self.button_10.setFixedSize(button_width, button_height)
		self.button_10.clicked.connect(self.generate_report)
		self.button_10.setObjectName("sidebar_button")

		self.button_11 = QPushButton('About', self)
		self.button_11.setFixedSize(button_width, button_height)
		self.button_11.clicked.connect(self.show_about)
		self.button_11.setObjectName("sidebar_button")

		###########################################################

		###########################################################
		# Manage tabs on the right window
		# Each tab is an object returned by the respective function associated with its UI
		self.tab1, self.sub_model = self.submissions_ui()
		self.tab2 = self.judge_ui()
		self.tab3, self.client_model = self.client_ui()
		self.tab4 = self.query_ui()
		self.tab5 = self.leaderboard_ui()
		self.tab6 = self.problem_ui()
		self.tab7 = self.language_ui()
		self.tab8 = self.stats_ui()
		self.tab9 = self.settings_ui()
		self.tab10 = self.reports_ui()
		self.tab11 = self.about_us_ui()

		###########################################################
		
		# Add widgets to our main window
		server_window.init_UI(self)
		return
	

	def init_UI(self):
		self.set_status()
		# Define Layout for sidebar
		side_bar_layout = QVBoxLayout()

		# Add buttons to our layout
		side_bar_layout.addWidget(self.button_1)
		side_bar_layout.addWidget(self.button_2)
		side_bar_layout.addWidget(self.button_3)
		side_bar_layout.addWidget(self.button_4)
		side_bar_layout.addWidget(self.button_5)
		side_bar_layout.addWidget(self.button_6)
		side_bar_layout.addWidget(self.button_7)
		side_bar_layout.addWidget(self.button_8)
		side_bar_layout.addWidget(self.button_9)
		side_bar_layout.addWidget(self.button_10)
		side_bar_layout.addWidget(self.button_11)

		# Set stretch and spacing
		side_bar_layout.addStretch(1)
		side_bar_layout.setSpacing(1)

		# Define our sidebar widget and set side_bar_layout to it.
		side_bar_widget = QWidget()
		side_bar_widget.setLayout(side_bar_layout)
		side_bar_widget.setFixedWidth(215)
		side_bar_widget.setObjectName("sidebar")

		#Define our top bar
		logo = QLabel(self)
		logo_image = QPixmap('Elements/bitwise_header.png')
		logo_image2 = logo_image.scaledToWidth(104)
		logo.setPixmap(logo_image2)

		top_bar_layout = QHBoxLayout()
		top_bar_layout.setContentsMargins(15, 5, 1, 0);
		top_bar_layout.addWidget(logo)

		top_bar_widget = QWidget()
		top_bar_widget.setLayout(top_bar_layout)
		top_bar_widget.setObjectName('top_bar')

		# Define our right side screens corresponding to buttons on the sidebar
		# Basically right screens are tab widgets whose tabs are hidden, 
		# and we map sidebar buttons to each tab switch :)
		# Since sidebars are not natively supported by pyqt5
		self.right_widget = QTabWidget()
		self.right_widget.setObjectName("main_tabs")
		self.right_widget.addTab(self.tab1, '')    # tab names are '' because we don't want them to show up in our screen
		self.right_widget.addTab(self.tab2, '')
		self.right_widget.addTab(self.tab3, '')
		self.right_widget.addTab(self.tab4, '')
		self.right_widget.addTab(self.tab5, '')
		self.right_widget.addTab(self.tab6, '')
		self.right_widget.addTab(self.tab7, '')
		self.right_widget.addTab(self.tab8, '')
		self.right_widget.addTab(self.tab9, '')
		self.right_widget.addTab(self.tab10, '')
		self.right_widget.addTab(self.tab11, '')

		# Screen 1 will be our initial screen 
		self.right_widget.setCurrentIndex(0)

		# Define the combined layout for sidebar + right side screens
		main_layout = QHBoxLayout()
		main_layout.addWidget(side_bar_widget)
		main_layout.addWidget(self.right_widget)

		# setstretch( index, stretch_value )
		main_layout.setStretch(0, 0)
		main_layout.setStretch(1, 90)
		# Define our main wideget = sidebar + windows
		main_widget = QWidget()
		main_widget.setObjectName("screen_widget")
		main_widget.setLayout(main_layout)


		#Define top_layout = logo_bar + main_layout
		top_layout = QVBoxLayout()
		top_layout.addWidget(top_bar_widget)
		top_layout.addWidget(main_widget)
		top_layout.setContentsMargins(1, 0, 1, 1)
		top_layout.setStretch(0, 8)
		top_layout.setStretch(1, 100)

		top_widget = QWidget()
		top_widget.setLayout(top_layout)
		top_widget.setObjectName("main_widget")

		# Set top_widget as our central widget
		self.setCentralWidget(top_widget)

		return

	def view_submissions(self):
		self.right_widget.setCurrentIndex(0)

	def manage_judges(self):
		self.right_widget.setCurrentIndex(1)

	def manage_clients(self):
		self.right_widget.setCurrentIndex(2)

	def manage_queries(self):
		self.right_widget.setCurrentIndex(3)

	def manage_leaderboard(self):
		self.right_widget.setCurrentIndex(4)

	def manage_problems(self):
		self.right_widget.setCurrentIndex(5)

	def manage_languages(self):
		self.right_widget.setCurrentIndex(6)

	def show_stats(self):
		self.right_widget.setCurrentIndex(7)

	def contest_settings(self):
		self.right_widget.setCurrentIndex(8)

	def generate_report(self):
		self.right_widget.setCurrentIndex(9)

	def show_about(self):
		self.right_widget.setCurrentIndex(10)

	def update_data(self):
		# If data has changed in submission table
		if self.data_changed_flags[0] == 1:
			self.sub_model.select()
			# reset data_changed_flag
			self.data_changed_flags[0] = 0
		if self.data_changed_flags[1] == 1:
			self.client_model.select()
			self.data_changed_flags[1] = 0

		return

	
	#####################################################
	# Databse related functions
	def init_qt_database(self):
		try:
			db = QSqlDatabase.addDatabase('QSQLITE')
			db.setDatabaseName('server_database.db')
			return db
		except:
			print('[ CRITICAL ] Database loading error!')


	def manage_models(self, db, table_name):
		if db.open():
			model = QSqlTableModel()
			model.setTable(table_name)
			model.setEditStrategy(QSqlTableModel.OnFieldChange)
			model.select()
		return model

	def generate_view(self, model):
		table = QTableView()
		table.setModel(model)
		# Enable sorting in the table view
		table.setSortingEnabled(True)
		# Enable Alternate row colors for readablity
		table.setAlternatingRowColors(True)
		# Select whole row when clicked
		table.setSelectionBehavior(QAbstractItemView.SelectRows)
		# Allow only one row to be selected
		table.setSelectionMode(QAbstractItemView.SingleSelection)
		# fit view to whole space
		table.resizeColumnsToContents()
		# Make table non-editable
		table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		# Set view to delete when gui is closed
		table.setAttribute(Qt.WA_DeleteOnClose)

		horizontal_header = table.horizontalHeader()
		horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
		vertical_header = table.verticalHeader()
		#vertical_header.setSectionResizeMode(QHeaderView.Stretch)
		vertical_header.setVisible(False)
		return table

	###############################################################

	# Handle UI for various button presses
	def submissions_ui(self):
		heading = QLabel('Submissions')
		heading.setObjectName('main_screen_heading')

		submission_model = self.manage_models(self.db, 'submissions')

		submission_model.setHeaderData(0, Qt.Horizontal, 'Run ID')
		submission_model.setHeaderData(1, Qt.Horizontal, 'Client ID')
		submission_model.setHeaderData(2, Qt.Horizontal, 'Language')
		submission_model.setHeaderData(3, Qt.Horizontal, 'Source File')
		submission_model.setHeaderData(4, Qt.Horizontal, 'Problem Code')
		submission_model.setHeaderData(5, Qt.Horizontal, 'Status')
		submission_model.setHeaderData(6, Qt.Horizontal, 'Time')

		submission_table = self.generate_view(submission_model)

		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(submission_table)
		main_layout.setStretch(0,5)
		main_layout.setStretch(1,95)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		main.show()
		return main, submission_model


	def client_ui(self):
		heading = QLabel('Clients')
		heading.setObjectName('main_screen_heading')

		client_model = self.manage_models(self.db, 'connected_clients')
		client_model.setHeaderData(0, Qt.Horizontal, 'Client ID')
		client_model.setHeaderData(1, Qt.Horizontal, 'Username')
		client_model.setHeaderData(2, Qt.Horizontal, 'Password')

		client_view = self.generate_view(client_model)


		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(client_view)
		main_layout.setStretch(0,5)
		main_layout.setStretch(1,95)		

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, client_model


	def judge_ui(self):
		heading = QLabel('Judges')
		heading.setObjectName('main_screen_content')

		#judge_model = self.manage_models(self.db, )

		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def query_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page4')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def leaderboard_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page5')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def problem_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page6')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def language_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page7')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def stats_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page8')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def settings_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page9')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def reports_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page10')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def about_us_ui(self):
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

	###################################################

	def set_status(self):
		global current_status
		self.status.showMessage(current_status)
	###################################################

	def closeEvent(self, event):
		message = "Pressing 'Yes' will SHUT the Server.\nAre you sure you want to exit?"
		detail_message = "Any active contest might end prematurely. "
		
		custom_close_box = QMessageBox()
		custom_close_box.setIcon(QMessageBox.Critical)
		custom_close_box.setWindowTitle('Warning!')
		custom_close_box.setText(message)
		custom_close_box.setInformativeText(detail_message)

		custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		custom_close_box.setDefaultButton(QMessageBox.No)

		button_yes = custom_close_box.button(QMessageBox.Yes)
		button_yes.setText('Yes')
		button_no = custom_close_box.button(QMessageBox.No)
		button_no.setText('No')

		button_yes.setObjectName("close_button_yes")
		button_no.setObjectName("close_button_no")

		button_yes.setStyleSheet(open('Elements/style.qss', "r").read())
		button_no.setStyleSheet(open('Elements/style.qss', "r").read())

		custom_close_box.exec_()

		if custom_close_box.clickedButton() == button_yes:
			event.accept()
		elif custom_close_box.clickedButton() == button_no : 
			event.ignore()


class init_gui(server_window):
	def __init__(self, data_changed_flags):
		# make a reference of App class
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('Elements/style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)
		
		server_app = server_window(data_changed_flags)

		# Splash screen
		# splash = QSplashScreen(QPixmap("Elements/bitwise.png"))
		# splash.show()
		# splash.finish(server_app)	
		# Splash ends

		
		server_app.showMaximized()
		# Execute the app mainloop
		app.exec_()
		return