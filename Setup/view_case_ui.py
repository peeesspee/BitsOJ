from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import *

class view_case_ui(QMainWindow):
	def __init__(
			self, 
			problem_path,
			parent=None
		):
		super(view_case_ui, self).__init__(parent)

		self.button_mode = 1
		self.problem_path = problem_path
		self.file_not_found = 0

		self.setWindowTitle('View Case')
		self.setGeometry(550, 250, 800, 700)
		self.setFixedSize(800,700)
		main = self.main_view_case_ui()
		self.setCentralWidget(main)
		return

	def main_view_case_ui(self):
		heading = QLabel('View Test File')
		open_label = QLabel("Open: ")
		path = QLabel(self.problem_path)
		path_layout = QHBoxLayout()
		path_layout.addWidget(open_label)
		path_layout.addWidget(path)
		path_layout.addStretch(1)
		path_widget = QWidget()
		path_widget.setLayout(path_layout)

		show_line_endings_label = QLabel('Show Line endings: ')

		show_line_endings_button = QCheckBox('')
		show_line_endings_button.setChecked(False)
		show_line_endings_button.stateChanged.connect(
			lambda:self.line_end_toggle(
				show_line_endings_button.checkState()
			)
		)

		line_end_layout = QHBoxLayout()
		line_end_layout.addWidget(show_line_endings_label)
		line_end_layout.addWidget(show_line_endings_button)
		line_end_layout.addStretch(1)
		line_end_widget = QWidget()
		line_end_widget.setLayout(line_end_layout)

		self.file_text_box = QTextEdit()
		self.file_text_box.setReadOnly(True)
		self.file_text_box.setFixedHeight(500)
		
		# Try to open file:
		try:
			file_content = ''
			# File is read line by line to maybe show line numbers in the future
			with open (self.problem_path, "r") as myfile:
				data = myfile.readlines()
			# print(data)
			for i in data:
				file_content = file_content + i
			self.backup_file_content = repr(file_content)
	
		except Exception as error:
			print("[ CRITICAL ] Could not read test file : " + str(error))
			file_content = "CRITICAL ERROR\nFile not found!"
			self.backup_file_content = " CRITICAL ERROR\nFile not found! "
			self.file_not_found = 1

		self.file_text_box.setText(file_content)
		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(path_widget)
		main_layout.addWidget(line_end_widget)
		main_layout.addWidget(self.file_text_box)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)

		heading.setObjectName('main_screen_heading')
		open_label.setObjectName('main_screen_sub_heading')
		path.setObjectName('main_screen_content')
		main.setObjectName('account_window')
		show_line_endings_label.setObjectName('main_screen_content')
		return main

	def line_end_toggle(self, state):
		try:
			if(state == Qt.Checked) and self.file_not_found == 0:
				# line endings show
				data = self.backup_file_content
				data = data.replace('\\r', '  CR\r')
				data = data.replace('\\n', '  LF\n')
				data = data[1:-1]
				
				self.line_endings_shown = 1
				self.file_text_box.setText(data)
			elif self.file_not_found == 0:
				# line endings hide
				if self.line_endings_shown == 1:
					self.line_endings_shown = 0
					# Replace current text with backup text
					self.file_text_box.setText(eval(self.backup_file_content))
		except Exception as error:
			print('[ ERROR ] Could not show line endings: ', error)	
		return