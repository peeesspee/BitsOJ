import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
# from login import authenticate_login
# from database_management import manage_database
# from login import authenticate_login

global current_status
current_status = "STOPPED"

class client_window(QMainWindow):
	def __init__(self):
		super().__init__()
		# Set app icon
		self.setWindowIcon(QIcon('Elements/logo.png'))
		# Set window title
		self.setWindowTitle('BitsOJ v1.0.1 [ Client ]')
		
		# Initialize status bar
		self.status = self.statusBar()

		# 
		# Make the app run full screen
		

		####################################################################
		# Define Sidebar buttons and their actions
		button_width = 200
		button_height = 50

		self.button_1 = QPushButton('Problems', self)
		self.button_1.setFixedSize(button_width, button_height)
		self.button_1.clicked.connect(self.view_problems)
		self.button_1.setObjectName('sidebar_button')

		self.button_2 = QPushButton('Submissions', self)
		self.button_2.setFixedSize(button_width, button_height)
		self.button_2.clicked.connect(self.view_submissions)
		self.button_2.setObjectName('sidebar_button')

		self.button_3 = QPushButton('Query', self)
		self.button_3.setFixedSize(button_width, button_height)
		self.button_3.clicked.connect(self.send_query)
		self.button_3.setObjectName('sidebar_button')

		self.button_4 = QPushButton('Leaderboard', self)
		self.button_4.setFixedSize(button_width, button_height)
		self.button_4.clicked.connect(self.ranklist)
		self.button_4.setObjectName('sidebar_button')

		self.button_5 = QPushButton('About', self)
		self.button_5.setFixedSize(button_width, button_height)
		self.button_5.clicked.connect(self.show_about)
		self.button_5.setObjectName('sidebar_button') 

		#####################################################################

		#####################################################################
		# Manage tabs o the right window
		# Each tab is an object returned by the respective function associated with its UI
		self.tab1 = self.problems_ui()
		self.tab2 = self.submissions_ui()
		self.tab3 = self.query_ui()
		self.tab4 = self.leaderboard_ui()
		self.tab5 = self.about_ui()

		#####################################################################

		# Add widgets to our main window 
		client_window.init_UI(self)
		return


	def init_UI(self):
		self.set_status()
		# Define layout for sidebar
		side_bar_layout = QVBoxLayout()

		#add buttons to our layout
		side_bar_layout.addWidget(self.button_1)
		side_bar_layout.addWidget(self.button_2)
		side_bar_layout.addWidget(self.button_3)
		side_bar_layout.addWidget(self.button_4)
		side_bar_layout.addWidget(self.button_5)

		# Set stretch and Spacing 
		side_bar_layout.addStretch(1)
		side_bar_layout.addSpacing(1)

		# Define our side bar widget and set side bar layout to it
		side_bar_widget = QWidget()
		side_bar_widget.setLayout(side_bar_layout)
		side_bar_widget.setObjectName("sidebar")

		# Define out top bar
		logo = QLabel(self)
		logo_image = QPixmap('Elements/bitwise_header.png')
		logo_image = logo_image.scaledToWidth(104)
		logo.setPixmap(logo_image)

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
		self.right_widget.addTab(self.tab1, '')
		self.right_widget.addTab(self.tab2, '')
		self.right_widget.addTab(self.tab3, '')
		self.right_widget.addTab(self.tab4, '')
		self.right_widget.addTab(self.tab5, '')

		# Screen 1 will be our initial screen
		self.right_widget.setCurrentIndex(0)

		# Define the combined layout for sidebar + right side screns
		main_layout = QHBoxLayout()
		main_layout.addWidget(side_bar_widget)
		main_layout.addWidget(self.right_widget)

		# setstretch( index, stretch_value )
		main_layout.setStretch(0, 10)
		main_layout.setStretch(1, 100)
		main_layout.setContentsMargins(10, 1 ,10, 1)
		# Define our main widget = sidebar + windows
		main_widget = QWidget()
		main_widget.setObjectName("screen_widget")
		main_widget.setLayout(main_layout)

		#Define top_layout = logo bar + main_layout
		top_layout = QVBoxLayout()
		top_layout.addWidget(top_bar_widget)
		top_layout.addWidget(main_widget)
		top_layout.setContentsMargins(1, 0, 1, 1)
		top_layout.setStretch(0, 8)
		top_layout.setStretch(1, 92)

		top_widget = QWidget()
		top_widget.setLayout(top_layout)
		top_widget.setObjectName("top_widget")

		# Set top_widget as our central widget
		self.setCentralWidget(top_widget)

		return

	def view_problems(self):
		self.right_widget.setCurrentIndex(0)

	def view_submissions(self):
		self.right_widget.setCurrentIndex(1)

	def send_query(self):
		self.right_widget.setCurrentIndex(2)

	def ranklist(self):
		self.right_widget.setCurrentIndex(3)

	def show_about(self):
		self.right_widget.setCurrentIndex(4)


	#############################################################################
	# Handle UI for various button presses
	def problems_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page1')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def submissions_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page2')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def query_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page3')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def leaderboard_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page4')
		heading.setObjectName('main_screen_content')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def about_ui(self):
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

	###############################################################


	def set_status(self):
		global current_status
		self.status.showMessage(current_status)

	def closeEvent(self, event):
		message = "Pressing 'Yes' will SHUT the Client.\nAre you sure you want to exit?"
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
		elif custom_close_box.clickedButton() == button_no:
			event.ignore()



class init_gui(client_window):
	def __init__(self):
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('Elements/style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)

		# make a reference of App class
		server_app = client_window()
		server_app.resize(800, 600)
		server_app.showMaximized()
		# Close the server as soon as close buton is clicked
		sys.exit(app.exec_())



