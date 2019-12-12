from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler


class view_case_ui(QMainWindow):
	problem_path = ''
	text_box = ''
	line_endings_shown = 0
	backup_file_content = ''
	file_not_found = 0


	def __init__(
		self, 
		data_changed_flags,
		problem_path,
		parent=None
		):
		super(view_case_ui, self).__init__(parent)
		view_case_ui.button_mode = 1

		self.data_changed_flags = data_changed_flags
		view_case_ui.problem_path = problem_path

		self.setWindowTitle('View Case')
		self.setGeometry(550, 250, 800, 600)
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

class problem_edit_ui(QMainWindow):
	def __init__(
			self, 
			data_changed_flags, 
			problem, 
			code, 
			test_files, 
			time_limit, 
			parent=None
		):
		super(problem_edit_ui, self).__init__(parent)
		
		self.data_changed_flags = data_changed_flags
		self.problem = problem
		self.code = code
		self.test_files = test_files
		self.time_limit = time_limit	
		self.setWindowTitle(self.problem)
		width = 1366
		height = 768
		self.setGeometry(300, 100, width, height)
		self.setFixedSize(width, height)
		main = self.main_problem_edit_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_problem_edit_ui(self):
		
		self.tabs = QTabWidget()
		self.tabs.setObjectName('main_tabs')
		self.tab_bar = QTabBar()
		self.tab_bar.setObjectName('problem_tabs')

		self.tab1 = self.get_problem_widget()
		self.tab2 = self.get_files_ui(self.problem, self.code, self.test_files, self.time_limit)
		
		self.tabs.addTab(self.tab1, '')
		self.tabs.addTab(self.tab2, '')
		self.tab_bar.addTab('Problem')
		self.tab_bar.addTab('I/O Files')
		self.tabs.setTabBar(self.tab_bar)

		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(150, 30)
		confirm_button.clicked.connect(lambda:problem_edit_ui.final_status(self))
		confirm_button.setDefault(True)

		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(150, 30)
		cancel_button.clicked.connect(lambda:problem_edit_ui.exit(self))
		cancel_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(1)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)
		button_widget.setContentsMargins(0, 20, 0, 0)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.tabs)
		main_layout.addWidget(button_widget)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)

		main.setObjectName('account_window')
		confirm_button.setObjectName('account_button')
		cancel_button.setObjectName('account_button')
		
		return main

	

	def final_status(self):
		self.data_changed_flags[14] = 0
		self.close()

	def exit(self):
		self.data_changed_flags[14] = 0
		self.close()

	def get_problem_widget(self):
		heading = QLabel('Edit Problem')
		problem_label = QLabel('Name: ')
		problem_content = QLabel(self.problem)
		code_label = QLabel('Code: ')
		code_content = QLabel(self.code)
		top_labels_layout = QHBoxLayout()
		top_labels_layout.addWidget(problem_label)
		top_labels_layout.addWidget(problem_content)
		top_labels_layout.addWidget(code_label)
		top_labels_layout.addWidget(code_content)
		top_labels_layout.addStretch(1)
		top_labels_widget = QWidget()
		top_labels_widget.setLayout(top_labels_layout)
		top_labels_widget.setContentsMargins(0, 20, 0, 0)

		time_limit_label = QLabel('Time Limit: ')
		time_limit_content = QLabel(str(self.time_limit))
		time_labels_layout = QHBoxLayout()
		time_labels_layout.addWidget(time_limit_label)
		time_labels_layout.addWidget(time_limit_content)
		time_labels_layout.addStretch(1)
		time_widget = QWidget()
		time_widget.setLayout(time_labels_layout)


		source_layout = QVBoxLayout()
		source_layout.addWidget(heading)
		source_layout.addWidget(top_labels_widget)
		source_layout.addWidget(time_widget)
		source_layout.addStretch(1)
		source_widget = QWidget()
		source_widget.setLayout(source_layout)

		
		problem_label.setObjectName('main_screen_sub_heading')
		problem_content.setObjectName('main_screen_content')
		code_label.setObjectName('main_screen_sub_heading')
		code_content.setObjectName('main_screen_content')
		time_limit_label.setObjectName('main_screen_sub_heading')
		time_limit_content.setObjectName('main_screen_content')
		heading.setObjectName('main_screen_heading')
		return source_widget

	def get_files_ui(self, problem_name, problem_code, time_limit, cases):
		heading = QLabel('View Files')
		cases = int(cases)
		test_cases_table = QTableWidget()
		test_cases_table.setRowCount(cases)
		test_cases_table.setColumnCount(2)
		test_cases_table.setObjectName('inner_table')
		test_cases_table.setHorizontalHeaderLabels(
			("Input Files", "Output Files", "Status")
		)
		test_cases_table.resizeColumnsToContents()
		test_cases_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		test_cases_table.setAlternatingRowColors(True)
		vertical_header = test_cases_table.verticalHeader()
		vertical_header.setVisible(False)
		horizontal_header = test_cases_table.horizontalHeader()
		horizontal_header.setSectionResizeMode(QHeaderView.Stretch)

		test_cases_table.cellDoubleClicked.connect(
			lambda:self.manage_io_file(
				problem_code,
				test_cases_table.selectionModel().currentIndex().row(),
				test_cases_table.selectionModel().currentIndex().column()
			)
		)
		
		for i in range(0, cases):
			test_cases_table.setItem(i, 0, QTableWidgetItem("input" + str(i) + ".in"))
			test_cases_table.setItem(i, 1, QTableWidgetItem("output" + str(i) + ".ans"))
			

		problem_layout = QVBoxLayout()
		problem_layout.addWidget(heading)
		problem_layout.addWidget(test_cases_table)
		problem_layout.addStretch(1)
		widget = QWidget()
		widget.setLayout(problem_layout)
		widget.setObjectName('content_box')
		heading.setObjectName('main_screen_heading')
		return widget

	def manage_io_file(self, problem_code, row, column):
		if column == 0:
			# Input file is selected
			file_path = "Problem Data/" + problem_code +"/input" + str(row) + ".in"
			self.ui = view_case_ui(
				self.data_changed_flags,
				file_path
			)
			self.ui.show()
		elif column == 1:
			# Output file is selected
			file_path = "Problem Data/" + problem_code +"/output" + str(row) + ".ans"
			self.ui = view_case_ui(
				self.data_changed_flags,
				file_path
			)
			self.ui.show()
	
		# elif column == 2:
		# 	print("Disable File " + str(row) + " for problem " + problem_code)
		return
