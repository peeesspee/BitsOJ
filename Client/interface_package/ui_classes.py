from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase 
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, QSize, QRect


class ui_widgets():
	#############################################################################
	# Handle UI for various button presses
	def problems_ui(self):
		main_layout = QVBoxLayout() 
		heading = QLabel('Page1')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def submissions_ui(self):
		heading = QLabel('My Submissions')
		heading.setObjectName('main_screen_heading')

		submission_model = self.manage_models(self.db, 'my_submissions')

		submission_model.setHeaderData(0, Qt.Horizontal, 'Run Id')
		submission_model.setHeaderData(1, Qt.Horizontal, 'Verdict')
		submission_model.setHeaderData(2, Qt.Horizontal, 'Source File')
		submission_model.setHeaderData(3, Qt.Horizontal, 'Language')
		submission_model.setHeaderData(4, Qt.Horizontal, 'Problem Code')
		submission_model.setHeaderData(5, Qt.Horizontal, 'Time')

		submission_table = self.generate_view(submission_model)


		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(submission_table)
		main_layout.setStretch(0, 5)
		main_layout.setStretch(1, 95)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")
		main.show()
		return main, submission_model

	def submit_ui(self):
		heading = QLabel('Submit Solution')
		heading.setObjectName('main_screen_heading')

		self.language_box = QComboBox()
		self.language_box.setGeometry(QRect(10, 10, 491, 31))
		self.language_box.setFixedWidth(250)
		self.language_box.setFixedHeight(40)
		self.language_box.setObjectName(("language_box_content"))
		self.language_box.addItem("PYTHON-3")
		self.language_box.addItem("PYTHON-2")
		self.language_box.addItem("C")
		self.language_box.addItem("C++")
		self.language_box.addItem("JAVA")

		text_area = QTextEdit()
		text_area.setFixedHeight(700)
		text_area.setObjectName('text_area_content')
		text_area.setPlaceholderText('Paste your code here')

		self.horizontal_layout = QHBoxLayout()
		self.upload_file = QPushButton('Upload File', self)
		self.upload_file.setObjectName('upload_file')
		self.upload_file.clicked.connect(path_dialog.upload_call)
		print('Hello')
		self.submit_solution = QPushButton('Submit', self)
		self.submit_solution.setObjectName('submit')
		self.horizontal_layout.addWidget(self.upload_file)
		self.horizontal_layout.addWidget(self.submit_solution)

		self.horizontal_widget = QWidget()
		self.horizontal_widget.setLayout(self.horizontal_layout)



		main_layout = QVBoxLayout() 

		main_layout.addWidget(heading)
		main_layout.addWidget(self.language_box)
		main_layout.addWidget(text_area)
		main_layout.addWidget(self.horizontal_widget)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def query_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page4')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen")

		return main

	def leaderboard_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Page5')
		heading.setObjectName('main_screen_heading')

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
	###################################################################################



class path_dialog(QWidget):
	file_path = None
	def __init__(self):
		super().__init__()
		self.title = 'Upload File'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.openFileNameDialog()

	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Upload File", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			print('[ File path ]' + fileName)
			path_dialog.file_path = fileName


	def upload_call():
		ex = path_dialog()
		ex.show()