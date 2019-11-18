from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler



class view_case_ui(QMainWindow):
	problem_path = ''
	text_box = ''
	line_endings_shown = 0
	backup_file_content = ''
	file_not_found = 0


	def __init__(
		self, 
		problem_path,
		parent=None
		):
		super(view_case_ui, self).__init__(parent)
		view_case_ui.button_mode = 1

		view_case_ui.problem_path = problem_path

		self.setWindowTitle('View Case')
		self.setFixedSize(800,600)
		main = self.main_view_case_ui()
		self.setCentralWidget(main)
		# self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_view_case_ui(self):
		heading = QLabel('View Test File')
		open_label = QLabel("Open: ")
		path = QLabel(view_case_ui.problem_path)
		path_layout = QHBoxLayout()
		path_layout.addWidget(open_label)
		path_layout.addWidget(path)
		path_layout.addStretch(1)
		path_widget = QWidget()
		path_widget.setLayout(path_layout)

		show_line_endings_label = QLabel('Show Line endings: ')

		show_line_endings_button = QCheckBox('')
		show_line_endings_button.setFixedSize(30, 30)
		show_line_endings_button.setChecked(False)
		show_line_endings_button.stateChanged.connect(view_case_ui.line_end_toggle)

		line_end_layout = QHBoxLayout()
		line_end_layout.addWidget(show_line_endings_label)
		line_end_layout.addWidget(show_line_endings_button)
		line_end_layout.addStretch(1)
		line_end_widget = QWidget()
		line_end_widget.setLayout(line_end_layout)

		file_text_box = QTextEdit()
		file_text_box.setReadOnly(True)
		view_case_ui.text_box = file_text_box

		# Try to open file:
		try:
			file_content = ''
			with open (view_case_ui.problem_path, "r") as myfile:
				data=myfile.readlines()
			# print(data)
			for i in data:
				file_content = file_content + i

			view_case_ui.backup_file_content = repr(file_content)
			file_not_found = 0
			# print(data)
		except Exception as error:
			print("[ CRITICAL ] Could not read test file : " + str(error))
			file_content = "CRITICAL ERROR\nFile not found!"
			view_case_ui.backup_file_content = " CRITICAL ERROR\nFile not found! "
			file_not_found = 1

		file_text_box.setText(file_content)
		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(path_widget)
		main_layout.addWidget(line_end_widget)
		main_layout.addWidget(view_case_ui.text_box)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)

		heading.setObjectName('main_screen_heading')
		open_label.setObjectName('main_screen_sub_heading')
		path.setObjectName('main_screen_content')
		main.setObjectName('account_window')
		show_line_endings_label.setObjectName('main_screen_content')
		
		return main

	def line_end_toggle(state):
		try:
			if(state == Qt.Checked) and view_case_ui.file_not_found == 0:
				# line endings show
				data = view_case_ui.backup_file_content
				data = data.replace('\\r', 'CR\r')
				data = data.replace('\\n', 'LF\n')
				data = data[1:-1]
				
				view_case_ui.line_endings_shown = 1
				view_case_ui.text_box.setText(data)
			elif view_case_ui.file_not_found == 0:
				# line endings hide
				if view_case_ui.line_endings_shown == 1:
					view_case_ui.line_endings_shown = 0
					# Replace current text with backup text
					view_case_ui.text_box.setText(eval(view_case_ui.backup_file_content))
		except:
			print('[ ERROR ] Could not show line endings. File Size might be too big.')
				
		return