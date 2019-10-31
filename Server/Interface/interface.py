import time 
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from Interface.ui_classes import *
from init_server import initialize_server, save_status
from database_management import user_management, submissions_management, query_management


# This is to ignore some warnings which were thrown when gui exited and 
# python deleted some assests in wrong order
# Nothing critical :)
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler)

# This class handles the main window of server
class server_window(QMainWindow):
	def __init__(self, data_changed_flags2, data_to_client):
		super().__init__()
		# Set app icon
		self.setWindowIcon(QIcon('Elements/logo.png'))
		# Set window title
		self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ]')

		# Make  the app run full-screen
		# Initialize status bar (Bottom Bar)
		self.status = self.statusBar()
		self.resize(1024, 768)

		# Timer to update GUI every 1 second
		self.timer = QTimer()
		self.change_flag = True
		self.timer.timeout.connect(self.update_data)
		self.timer.start(1000)
		self.contest_start_time = ''
		
		# make data_changed_flag accessible from the class methods
		self.data_changed_flags = data_changed_flags2
		self.data_to_client = data_to_client
		
		###########################################################
		self.db = self.init_qt_database()
		###########################################################
		self.config = initialize_server.read_config()
		self.contest_set_time = self.config['Contest Set Time']
		# Define Sidebar Buttons and their actions
		button_width = 200
		button_height = 50

		self.button_0 = QPushButton('Accounts', self)
		self.button_0.setFixedSize(button_width, button_height)
		self.button_0.clicked.connect(self.manage_accounts)
		self.button_0.setObjectName("sidebar_button")

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
		# Tab UI are managed by interface_packages/ui_classes.py file 
		self.tab0, self.account_model, self.delete_account_button = ui_widgets.accounts_ui(self)
		self.tab1, self.sub_model = ui_widgets.submissions_ui(self)
		self.tab2, self.judge_model = ui_widgets.judge_ui(self)
		self.tab3, self.client_model = ui_widgets.client_ui(self)
		self.tab4, self.query_model = ui_widgets.query_ui(self)
		self.tab5, self.score_model = ui_widgets.leaderboard_ui(self)
		self.tab6 = ui_widgets.problem_ui(self)
		self.tab7 = ui_widgets.language_ui(self)
		self.tab8 = ui_widgets.stats_ui(self)
		(
		self.tab9, self.contest_time_entry, self.change_time_entry, self.set_button, 
		self.start_button, self.update_button, self.stop_button, self.account_reset_button, 
		self.submission_reset_button, self.query_reset_button, self.client_reset_button, 
		self.server_reset_button
		) = ui_widgets.settings_ui(self)

		self.tab10 = ui_widgets.reports_ui(self)
		self.tab11 = ui_widgets.about_us_ui(self)
		
		###########################################################
		
		
		# Initialize GUI elements
		server_window.init_UI(self)
		# Load previous state in case of server restart
		server_window.load_previous_state(self)
		return
	

		return
	def init_UI(self):
		self.set_status('SETUP')
		# Define Layout for sidebar
		side_bar_layout = QVBoxLayout()

		# Add buttons to our layout
		side_bar_layout.addWidget(self.button_0)
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
		side_bar_layout.setSpacing(0)

		# Define our sidebar widget and set side_bar_layout to it.
		side_bar_widget = QWidget()
		side_bar_widget.setLayout(side_bar_layout)
		side_bar_widget.setFixedWidth(215)
		side_bar_widget.setObjectName("sidebar")

		#Define our top bar
		logo = QLabel(self)
		logo_image = QPixmap('Interface/bitwise_header.png')
		logo_image2 = logo_image.scaledToWidth(104)
		logo.setPixmap(logo_image2)

		self.timer_widget = QLCDNumber()
		self.timer_widget.setSegmentStyle(QLCDNumber.Flat)
		self.timer_widget.setDigitCount(8)
		self.timer_widget.display('00:00:00')
		self.timer_widget.setFixedSize(150,40)
		

		top_bar_layout = QHBoxLayout()
		top_bar_layout.setContentsMargins(15, 5, 20, 0);
		top_bar_layout.addWidget(logo)
		top_bar_layout.addWidget(self.timer_widget)
		top_bar_layout.setStretch(0, 70)
		

		top_bar_widget = QWidget()
		top_bar_widget.setLayout(top_bar_layout)
		top_bar_widget.setObjectName('top_bar')

		# Define our right side screens corresponding to buttons on the sidebar
		# Basically right screens are tab widgets whose tabs are hidden, 
		# and we map sidebar buttons to each tab switch :)
		# Since sidebars are not natively supported by pyqt5
		self.right_widget = QTabWidget()
		self.right_widget.addTab(self.tab0, '')
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
		self.right_widget.setObjectName("main_tabs")
		

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

	@pyqtSlot()
	def manage_accounts(self):
		self.right_widget.setCurrentIndex(0)

	@pyqtSlot()
	def view_submissions(self):
		self.right_widget.setCurrentIndex(1)

	@pyqtSlot()
	def manage_judges(self):
		self.right_widget.setCurrentIndex(2)

	@pyqtSlot()
	def manage_clients(self):
		self.right_widget.setCurrentIndex(3)

	@pyqtSlot()
	def manage_queries(self):
		self.right_widget.setCurrentIndex(4)

	@pyqtSlot()
	def manage_leaderboard(self):
		self.right_widget.setCurrentIndex(5)

	@pyqtSlot()
	def manage_problems(self):
		self.right_widget.setCurrentIndex(6)

	@pyqtSlot()
	def manage_languages(self):
		self.right_widget.setCurrentIndex(7)

	@pyqtSlot()
	def show_stats(self):
		self.right_widget.setCurrentIndex(8)

	@pyqtSlot()
	def contest_settings(self):
		self.right_widget.setCurrentIndex(9)

	@pyqtSlot()
	def generate_report(self):
		self.right_widget.setCurrentIndex(10)

	@pyqtSlot()
	def show_about(self):
		self.right_widget.setCurrentIndex(11)

	####################################################
	# Functions related to GUI updates
	def load_previous_state(self):
		if self.config["Contest Status"] == "RUNNING":
			server_window.set_button_behavior(self, 'RUNNING')
		elif self.config["Contest Status"] == "STOPPED":
			server_window.set_button_behavior(self, 'STOPPED')
		elif self.config["Contest Status"] == "SETUP":
			server_window.set_button_behavior(self, 'SETUP')

		# TODO: When server restarts, pop up a new notification about contest status
		return
			
	def update_data(self):
		# If data has changed in submission table
		# Update submission table
		if self.data_changed_flags[0] == 1:
			self.sub_model.select()
			self.set_flags(0, 0)
		# Update connected clients table
		if self.data_changed_flags[1] == 1:
			self.client_model.select()
			self.set_flags(1, 0)
		# Update accounts table
		if self.data_changed_flags[5] == 1:
			self.account_model.select()
			self.set_flags(5, 0)
		# Update Query table
		if self.data_changed_flags[9] == 1:
			self.query_model.select()
			self.set_flags(9, 0)
		# Update judge view
		if self.data_changed_flags[13] == 1:
			self.judge_model.select()
			self.set_flags(13, 0)
		# Update scoreboard view
		if self.data_changed_flags[16] == 1:
			self.score_model.select()			#TODO select in ascending order of score
			self.set_flags(16, 0)
		# System EXIT
		if self.data_changed_flags[7] == 1:
			sys.exit()

		# OPTIMISE TODO
		# if self.data_changed_flags[10] == 0:
			# self.set_status('SETUP')
			# self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ][ SETUP ]')

		# Recieved contest start signal
		elif self.data_changed_flags[10] == 1:
			# Find time elapsed since contest start
			total_time = self.contest_set_time
			current_time = time.time()

			elapsed_time = time.strftime('%H:%M:%S', time.gmtime(total_time - current_time ))
			
			#Update timer
			self.timer_widget.display(elapsed_time)

		# Recieved contest stop signal
		# elif self.data_changed_flags[10] == 2:
		# 	self.set_status('STOPPED')
		# 	self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ][ STOPPED ]')
		return

	def convert_to_seconds(time_str):
		print(time_str)
		h, m, s = time_str.split(':')
		return int(h) * 3600 + int(m) * 60 + int(s)

	def set_button_behavior(self, status):
		if status == "SETUP":
			self.set_status('SETUP')
			self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ][ SETUP ]')
			self.data_changed_flags[10] = 0
			contest_duration = self.config["Contest Duration"]
			self.timer_widget.display(contest_duration)
			self.contest_time_entry.setReadOnly(0)
			self.contest_time_entry.setToolTip('You will not be able to edit this when contest starts.')
			self.change_time_entry.setReadOnly(False)
			self.change_time_entry.setToolTip('You will be able to use it when contest is STARTED')
			self.set_button.setEnabled(True)
			self.set_button.setToolTip('Set contest time.\nThis does NOT broadcast to clients.')
			self.start_button.setEnabled(True)
			self.start_button.setToolTip('START the contest and broadcast to all clients.')
			self.stop_button.setEnabled(False)
			self.stop_button.setToolTip('STOP the contest and broadcast to all clients.\nDisabled until contest Starts')
			self.update_button.setEnabled(False)
			self.update_button.setToolTip('UPDATE contest time and broadcast to all clients.\nDisabled until contest Starts')
			self.server_reset_button.setEnabled(True)
			self.server_reset_button.setToolTip('RESET the server.')
			self.account_reset_button.setEnabled(True)
			self.submission_reset_button.setEnabled(True)
			self.query_reset_button.setEnabled(True)
			self.client_reset_button.setEnabled(True)
			self.delete_account_button.setEnabled(True)
		if status == "RUNNING":
			self.set_status('RUNNING')
			self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ][ RUNNING ]')
			self.data_changed_flags[10] = 1
			self.contest_time_entry.setReadOnly(1)
			self.contest_time_entry.setToolTip('Contest has STARTED.\nYou can\'t edit this value now.')
			self.change_time_entry.setReadOnly(False)
			self.change_time_entry.setToolTip('Extend/Shorten contest (in minutes)')
			self.set_button.setEnabled(False)
			self.set_button.setToolTip('Contest has STARTED.\nYou can not set time now!')
			self.start_button.setEnabled(False)
			self.start_button.setToolTip('Contest is already running!')
			self.stop_button.setEnabled(True)
			self.stop_button.setToolTip('STOP the contest.')
			self.update_button.setEnabled(True)
			self.update_button.setToolTip('Update the contest.')
			self.server_reset_button.setEnabled(False)
			self.server_reset_button.setToolTip('RESET the server.\nCan only be used when contest\nis not RUNNING.')
			self.account_reset_button.setEnabled(False)
			self.submission_reset_button.setEnabled(False)
			self.query_reset_button.setEnabled(True)
			self.client_reset_button.setEnabled(True)
			self.delete_account_button.setEnabled(False)
		elif status == "STOPPED":
			self.set_status('STOPPED')
			self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ][ STOPPED ]')
			self.data_changed_flags[10] = 2
			self.contest_time_entry.setReadOnly(1)
			self.contest_time_entry.setToolTip('Contest has STOPPED.\nYou can\'t edit this value now.')
			self.update_button.setEnabled(False)
			self.update_button.setToolTip('Contest has STOPPED.\nYou can not extend it now.')
			self.stop_button.setEnabled(False)
			self.stop_button.setToolTip('Contest has already STOPPED!')
			self.start_button.setEnabled(False)
			self.start_button.setToolTip('Contest has STOPPED!')
			self.set_button.setEnabled(False)
			self.set_button.setToolTip('Contest has STOPPED!')
			self.change_time_entry.setReadOnly(True)
			self.change_time_entry.setToolTip('Contest has STOPPED.\nYou can not change time now!')
			self.server_reset_button.setEnabled(True)
			self.server_reset_button.setToolTip('RESET the server.')
			self.account_reset_button.setEnabled(True)
			self.submission_reset_button.setEnabled(True)
			self.query_reset_button.setEnabled(True)
			self.client_reset_button.setEnabled(True)
			self.delete_account_button.setEnabled(True)
		return

	def process_event(self, data, extra_data):
		if data == 'SET':
			print('\n[ SET ] Contest Duration : ' + str(extra_data))
			save_status.update_entry('Contest Duration', str(extra_data))
			self.timer_widget.display(initialize_server.get_duration())

		elif data == 'START':
			current_time = time.localtime()
			self.contest_start_time = time.time()
			self.contest_duration_seconds = server_window.convert_to_seconds(initialize_server.get_duration())
			self.contest_set_time = self.contest_duration_seconds + self.contest_start_time

			message = {
			'Code' : 'START',
			'Duration' : extra_data
			}
			message = json.dumps(message)
			self.data_to_client.put(message)

			# Update GUI
			server_window.set_button_behavior(self, 'RUNNING')

			# Update config file
			current_time = str(time.strftime("%H:%M:%S", current_time))
			save_status.update_entry('Contest Start Time', current_time)
			save_status.update_entry('Contest Status', 'RUNNING')
			save_status.update_entry('Contest Duration', extra_data)
			save_status.update_entry('Contest Set Time', self.contest_set_time)

		elif data == 'STOP':
			current_time = time.localtime()
			
			message = {
			'Code' : 'STOP'
			}
			message = json.dumps(message)
			self.data_to_client.put(message)

			# Update GUI
			self.set_button_behavior('STOPPED')
			# Update config file
			current_time = str(time.strftime("%H:%M:%S", current_time))
			save_status.update_entry('Contest End Time', current_time)
			save_status.update_entry('Contest Status', 'STOPPED')

			

		elif data == 'UPDATE':
			# Send UPDATE signal
			message = {
			'Code' : 'UPDATE',
			'Time' : extra_data
			}
			message = json.dumps(message)
			self.data_to_client.put(message)
			
		return

	def allow_login_handler(self, state):
		if(state == Qt.Checked):
			# Allow logins
			self.set_flags(2, 1)
		else:
			# Stop logins
			self.set_flags(2, 0)
		return

	def allow_judge_login_handler(self, state):
		if(state == Qt.Checked):
			# Allow logins
			self.set_flags(12, 1)
		else:
			# Stop logins
			self.set_flags(12, 0)
		return

	def allow_submissions_handler(self, state):
		if(state == Qt.Checked):
			# Allow submissions
			self.set_flags(3, 1)
		else:
			# Stop submissions
			self.set_flags(3, 0)
		return

	def allow_scoreboard_update_handler(self, state):
		if(state == Qt.Checked):
			# Allow scoreboard update
			print("Allow")
			self.set_flags(15, 1)
		else:
			# Stop scoreboard update
			print("Disallow")
			self.set_flags(15, 0)
		return

	def check_login_allowed(self):
		if self.data_changed_flags[2] == 1:
			return True
		return False

	def check_judge_login_allowed(self):
		if self.data_changed_flags[12] == 1:
			return True
		return False

	def check_submission_allowed(self):
		if self.data_changed_flags[3] == 1:
			return True
		return False

	def check_scoreboard_update_allowed(self):
		if self.data_changed_flags[15] == 1:
			return True
		return False

	def set_flags(self, index, value):
		self.data_changed_flags[index] = value
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

	@pyqtSlot()
	def create_accounts(self):
		if self.data_changed_flags[4] == 0:
			# CRITICAL section flag set
			self.data_changed_flags[4] = 1
			self.window = new_accounts_ui(self.data_changed_flags)
			self.window.show()			
		else:
			pass
		return

	@pyqtSlot()
	def query_reply(self, selected_row):
		if self.data_changed_flags[8] == 0:
			# CRITICAL section flag set
			self.data_changed_flags[8] = 1
			try:
				query = self.query_model.index(selected_row, 2).data()
				client_id = self.query_model.index(selected_row, 1).data()
				query_id = self.query_model.index(selected_row, 0).data()
				
				if client_id == None and query_id == None:
					pass
				else:
					self.window = query_reply_ui(self.data_changed_flags,self.data_to_client ,query,client_id, query_id)
					self.window.show()

			except Exception as error: 
				# Reset data_changed_flag for deletion of account
				print('[ ERROR ] : ' + str(error))
			finally:
				self.data_changed_flags[8] = 0
				return
		else:
			return

		

	@pyqtSlot()
	def delete_account(self, selected_rows):
		if self.data_changed_flags[6] == 0:
			# Set critical flag
			self.data_changed_flags[6] = 1
		else:
			# If one data deletion window is already opened, process it first.
			return
		# If no row is selected, return
		try:
			username = str(selected_rows[0].data())
		except: 
			# Reset data_changed_flag for deletion of account
			self.data_changed_flags[6] = 0
			return
		message = "Are you sure you want to delete : " + username + " ? "
	
		custom_close_box = QMessageBox()
		custom_close_box.setIcon(QMessageBox.Critical)
		custom_close_box.setWindowTitle('Confirm Deletion')
		custom_close_box.setText(message)

		custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		custom_close_box.setDefaultButton(QMessageBox.No)

		button_yes = custom_close_box.button(QMessageBox.Yes)
		button_yes.setText('Yes')
		button_no = custom_close_box.button(QMessageBox.No)
		button_no.setText('No')

		button_yes.setObjectName("close_button_yes")
		button_no.setObjectName("close_button_no")

		button_yes.setStyleSheet(open('Interface/style.qss', "r").read())
		button_no.setStyleSheet(open('Interface/style.qss', "r").read())

		custom_close_box.exec_()

		if custom_close_box.clickedButton() == button_yes:
			# Delete from accounts table and connected clients table
			user_management.delete_user(username)
			# Broadcast this user disconnection
			message = {
			'Code' : 'DSCNT',
			'Mode' : 1,
			'Client' : username
			}
			message = json.dumps(message)
			self.data_to_client.put(message)
			# Update Accounts and connected clients View
			self.data_changed_flags[5] = 1
			self.data_changed_flags[1] = 1
		elif custom_close_box.clickedButton() == button_no : 
			pass

		# Reset critical flag
		self.data_changed_flags[6] = 0

		return

	@pyqtSlot()
	def edit_client(self, selected_row):
		if self.data_changed_flags[14] == 0:
			# Set critical flag
			self.data_changed_flags[14] = 1
		else:
			# If one client edit window is already opened, process it first.
			return
		# If no row is selected, return
		try:
			client_id = self.client_model.index(selected_row, 0).data()
			username = self.client_model.index(selected_row, 1).data()
			password = self.client_model.index(selected_row, 2).data()
			state = self.client_model.index(selected_row, 3).data()

			if username == None or client_id == None or password == None or state == None:
				pass
			else:
				self.edit_window = account_edit_ui(self.data_changed_flags, client_id, username, password, state)
				self.edit_window.show()
			
		except Exception as error: 
			print('Error' + str(error))
		finally:
			# Reset critical flag
			self.data_changed_flags[14] = 0
			return

	def reset_accounts(self):
		if self.data_changed_flags[11] == 0:
			# Set critical flag
			self.data_changed_flags[11] = 1
		else:
			# If one data deletion window is already opened, process it first.
			return
		# If no row is selected, return
		try:
			message = "Are you sure you want to DELETE ALL accounts?"
		
			custom_close_box = QMessageBox()
			custom_close_box.setIcon(QMessageBox.Critical)
			custom_close_box.setWindowTitle('Confirm RESET')
			custom_close_box.setText(message)

			custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
			custom_close_box.setDefaultButton(QMessageBox.No)

			button_yes = custom_close_box.button(QMessageBox.Yes)
			button_yes.setText('Yes')
			button_no = custom_close_box.button(QMessageBox.No)
			button_no.setText('No')

			button_yes.setObjectName("close_button_yes")
			button_no.setObjectName("close_button_no")

			button_yes.setStyleSheet(open('Interface/style.qss', "r").read())
			button_no.setStyleSheet(open('Interface/style.qss', "r").read())

			custom_close_box.exec_()

			if custom_close_box.clickedButton() == button_yes:
				user_management.delete_all()
				# Update Accounts View
				self.data_changed_flags[5] = 1
			elif custom_close_box.clickedButton() == button_no : 
				pass
		except:
			print('Could not reset database!')

		finally:
			# Reset critical flag
			self.data_changed_flags[11] = 0
			return

	
	def reset_submissions(self):
		if self.data_changed_flags[11] == 0:
			# Set critical flag
			self.data_changed_flags[11] = 1
		else:
			# If one data deletion window is already opened, process it first.
			return
		# If no row is selected, return
		try:
			message = "Are you sure you want to DELETE ALL submissions?"
		
			custom_close_box = QMessageBox()
			custom_close_box.setIcon(QMessageBox.Critical)
			custom_close_box.setWindowTitle('Confirm RESET')
			custom_close_box.setText(message)

			custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
			custom_close_box.setDefaultButton(QMessageBox.No)

			button_yes = custom_close_box.button(QMessageBox.Yes)
			button_yes.setText('Yes')
			button_no = custom_close_box.button(QMessageBox.No)
			button_no.setText('No')

			button_yes.setObjectName("close_button_yes")
			button_no.setObjectName("close_button_no")

			button_yes.setStyleSheet(open('Interface/style.qss', "r").read())
			button_no.setStyleSheet(open('Interface/style.qss', "r").read())

			custom_close_box.exec_()

			if custom_close_box.clickedButton() == button_yes:
				submissions_management.delete_all()
				# Update Submissions View
				self.data_changed_flags[0] = 1
			elif custom_close_box.clickedButton() == button_no : 
				pass
		except Exception as error:
			print('Could not reset database : ' + str(error))

		finally:
			# Reset critical flag
			self.data_changed_flags[11] = 0
		return

	def reset_queries(self):
		if self.data_changed_flags[11] == 0:
			# Set critical flag
			self.data_changed_flags[11] = 1
		else:
			# If one data deletion window is already opened, process it first.
			return
		# If no row is selected, return
		try:
			message = "Are you sure you want to DELETE ALL queries?"
		
			custom_close_box = QMessageBox()
			custom_close_box.setIcon(QMessageBox.Critical)
			custom_close_box.setWindowTitle('Confirm RESET')
			custom_close_box.setText(message)

			custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
			custom_close_box.setDefaultButton(QMessageBox.No)

			button_yes = custom_close_box.button(QMessageBox.Yes)
			button_yes.setText('Yes')
			button_no = custom_close_box.button(QMessageBox.No)
			button_no.setText('No')

			button_yes.setObjectName("close_button_yes")
			button_no.setObjectName("close_button_no")

			button_yes.setStyleSheet(open('Interface/style.qss', "r").read())
			button_no.setStyleSheet(open('Interface/style.qss', "r").read())

			custom_close_box.exec_()

			if custom_close_box.clickedButton() == button_yes:
				query_management.delete_all()
				# Update Queriess View
				self.data_changed_flags[9] = 1
			elif custom_close_box.clickedButton() == button_no : 
				pass
		except Exception as error:
			print('Could not reset database : ' + str(error))

		finally:
			# Reset critical flag
			self.data_changed_flags[11] = 0
		return

	def reset_server(self):
		if self.data_changed_flags[11] == 0:
			# Set critical flag
			self.data_changed_flags[11] = 1
		else:
			# If one data deletion window is already opened, process it first.
			return
		# If no row is selected, return
		try:
			message = "Are you sure to RESET the server?\nContest Information will be lost"
			extra_data = "You should create the contest report first!"
		
			custom_close_box = QMessageBox()
			custom_close_box.setIcon(QMessageBox.Critical)
			custom_close_box.setWindowTitle('SERVER RESET')
			custom_close_box.setText(message)

			custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
			custom_close_box.setDefaultButton(QMessageBox.No)

			button_yes = custom_close_box.button(QMessageBox.Yes)
			button_yes.setText('Yes')
			button_no = custom_close_box.button(QMessageBox.No)
			button_no.setText('No')

			button_yes.setObjectName("close_button_yes")
			button_no.setObjectName("close_button_no")

			button_yes.setStyleSheet(open('Interface/style.qss', "r").read())
			button_no.setStyleSheet(open('Interface/style.qss', "r").read())

			custom_close_box.exec_()

			if custom_close_box.clickedButton() == button_yes:
				print('[ EVENT ] SERVER RESET TRIGGERED')
				print('[ RESET ] Disconnecting all clients...')
				# TODO : Broadcast this to all clients...
				message = {
				'Code' : 'DSCNT',
				'Mode' : 2
				}
				message = json.dumps(message)
				self.data_to_client.put(message)
				# Set DISCONNECTED to all connected clients
				user_management.disconnect_all()
				self.data_changed_flags[1] = 1

				print('[ RESET ] Disconnecting all Judges...')
				# Update judges view
				self.data_changed_flags[13] = 1
				# TODO Broadcast this to all judges

				print('[ RESET ] Resetting Accounts...')
				user_management.delete_all()
				# Update Accounts View
				self.data_changed_flags[5] = 1
				print('[ RESET ] Resetting Submissions...')
				submissions_management.delete_all()
				# Update Submissions View
				self.data_changed_flags[0] = 1
				print('[ RESET ] Resetting Queries...')
				query_management.delete_all()
				# Update Queriess View
				self.data_changed_flags[9] = 1
				print('[ RESET ] Reset environment...')
				server_window.set_button_behavior(self, 'SETUP')
				save_status.update_entry('Contest Duration', '00:00:00')
				save_status.update_entry('Contest Status', 'SETUP')
				save_status.update_entry('Contest Start Time', '00:00:00')
				save_status.update_entry('Contest End Time', '00:00:00')
				save_status.update_entry('Contest Set Time', 0)

			
			elif custom_close_box.clickedButton() == button_no : 
				pass
		except Exception as error:
			print('Could not reset database : ' + str(error))

		finally:
			# Reset critical flag
			self.data_changed_flags[11] = 0
		return

	def disconnect_all(self):
		if self.data_changed_flags[11] == 0:
			# Set critical flag
			self.data_changed_flags[11] = 1
		else:
			# If one data deletion window is already opened, process it first.
			return
		# If no row is selected, return
		try:
			message = "Are you sure to DISCONNECT all clients?\nClients will be able to login again\nif permitted."
			
			custom_close_box = QMessageBox()
			custom_close_box.setIcon(QMessageBox.Critical)
			custom_close_box.setWindowTitle('Disconnect Clients')
			custom_close_box.setText(message)

			custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
			custom_close_box.setDefaultButton(QMessageBox.No)

			button_yes = custom_close_box.button(QMessageBox.Yes)
			button_yes.setText('Yes')
			button_no = custom_close_box.button(QMessageBox.No)
			button_no.setText('No')

			button_yes.setObjectName("close_button_yes")
			button_no.setObjectName("close_button_no")

			button_yes.setStyleSheet(open('Interface/style.qss', "r").read())
			button_no.setStyleSheet(open('Interface/style.qss', "r").read())

			custom_close_box.exec_()

			if custom_close_box.clickedButton() == button_yes:
				print('[ EVENT ] CLIENT DISCONNECT TRIGGERED')
				print('[ EVENT ][ RESET ] Disconnecting all clients...')
				# TODO : Broadcast this to all clients...
				message = {
				'Code' : 'DSCNT',
				'Mode' : 2
				}
				message = json.dumps(message)
				self.data_to_client.put(message)
				# Set DISCONNECTED to all connected clients
				user_management.disconnect_all()
				self.data_changed_flags[1] = 1
			
			elif custom_close_box.clickedButton() == button_no : 
				pass
		except Exception as error:
			print('Could not reset database : ' + str(error))

		finally:
			# Reset critical flag
			self.data_changed_flags[11] = 0
		return


		

	###################################################
	
	###################################################
	def set_status(self, message = 'SETUP'):
		self.status.showMessage('BitsOJ > ' + message)
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

		button_yes.setStyleSheet(open('Interface/style.qss', "r").read())
		button_no.setStyleSheet(open('Interface/style.qss', "r").read())

		custom_close_box.exec_()

		if custom_close_box.clickedButton() == button_yes:
			event.accept()
		elif custom_close_box.clickedButton() == button_no : 
			event.ignore()


class init_gui(server_window):
	# data_from_interface queue is data_to_client queue with respect to interface
	def __init__(self, data_changed_flags, data_to_client):
		# make a reference of App class
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('Interface/style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)
		
		server_app = server_window(data_changed_flags, data_to_client)

		# Splash screen
		# splash = QSplashScreen(QPixmap("Interface/bitwise.png"))
		# splash.show()
		# splash.finish(server_app)	
		# Splash ends

		server_app.showMaximized()

		# Execute the app mainloop
		app.exec_()
		return
