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
		self.setGeometry(550, 250, 800, 700)
		self.setFixedSize(800,700)
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
		file_text_box.setFixedHeight(500)
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
				data = data.replace('\\r', '  CR\r')
				data = data.replace('\\n', '  LF\n')
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

		self.name_changed = 0
		self.code_changed = 0
		self.time_limit_changed = 0
		self.author_changed = 0
		self.statement_changed = 0
		self.input_format_changed = 0 
		self.output_format_changed = 0
		self.constraints_changed = 0
		self.example_input_format_changed = 0 
		self.example_output_format_changed = 0 

		self.setWindowTitle(self.problem)
		self.width = 1250
		self.height = 768
		self.setGeometry(300, 100, self.width, self.height)
		self.setFixedSize(self.width, self.height)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		
		self.tab1 = self.get_problem_widget()
		self.tab2 = self.get_files_ui(self.problem, self.code, self.test_files, self.time_limit)

		self.tabs = QTabWidget()
		self.tabs.setObjectName('main_tabs')
		self.tab_bar = QTabBar()
		self.tab_bar.setObjectName('problem_tabs')
		self.tabs.addTab(self.tab1, '')
		self.tabs.addTab(self.tab2, '')
		self.tab_bar.addTab('Problem')
		self.tab_bar.addTab('I/O Files')
		self.tabs.setTabBar(self.tab_bar)
		
		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(150, 30)
		confirm_button.clicked.connect(lambda:problem_edit_ui.final_status(self))
		confirm_button.setDefault(True)
		confirm_button.setObjectName('account_button')
		
		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(150, 30)
		cancel_button.clicked.connect(lambda:problem_edit_ui.exit(self))
		cancel_button.setObjectName('account_button')

		button_layout = QHBoxLayout()
		button_layout.addStretch(20)
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(23)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)
		button_widget.setContentsMargins(0, 20, 0, 0)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.tabs)
		main_layout.addStretch(1)
		main_layout.addWidget(button_widget)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName('account_window')
		self.setCentralWidget(main)

	def final_status(self):
		self.data_changed_flags[14] = 0
		self.close()

	def exit(self):
		self.data_changed_flags[14] = 0
		self.close()

	def get_problem_widget(self):
		heading = QLabel('Edit Problem')
		problem_label = QLabel('Name: ')
		problem_content = QLineEdit()
		problem_content.setText(self.problem)
		problem_content.setFixedSize(250, 28)
		code_label = QLabel('Code: ')
		code_content = QLineEdit()
		code_content.setText(self.code)
		code_content.setFixedSize(70, 28)
		time_limit_label = QLabel('Time Limit: ')
		time_limit_content = QLineEdit()
		time_limit_content.setText(str(self.time_limit))
		time_limit_content.setFixedSize(70, 28)
		author_label = QLabel('Author: ')
		author_content = QLineEdit()
		# author_content.setText(str(self.author_limit))
		author_content.setFixedSize(150, 28)
		level1_layout = QHBoxLayout()
		level1_layout.addWidget(problem_label)
		level1_layout.addWidget(problem_content)
		level1_layout.addStretch(20)
		level1_layout.addWidget(code_label)
		level1_layout.addWidget(code_content)
		level1_layout.addStretch(20)
		level1_layout.addWidget(time_limit_label)
		level1_layout.addWidget(time_limit_content)
		level1_layout.addStretch(20)
		level1_layout.addWidget(author_label)
		level1_layout.addWidget(author_content)
		level1_widget = QWidget()
		level1_widget.setLayout(level1_layout)

		statement_label = QLabel('Problem Statement: ')
		statement_content = QTextEdit()
		# statement_content.setText(self.statement)
		statement_content.setFixedHeight(500)

		input_syntax_label = QLabel('Input Format: ')
		output_syntax_label = QLabel('Output Format: ')
		input_syntax_content = QTextEdit()
		# input_syntax_content.setText(self.input_syntax)
		input_syntax_content.setFixedHeight(200)
		output_syntax_content = QTextEdit()
		# output_syntax_content.setText(self.output_syntax)
		output_syntax_content.setFixedHeight(200)

		constraints_label = QLabel('Constraints: ')
		constraints_content = QTextEdit()
		# constraints_content.setText(self.constraints)
		constraints_content.setFixedHeight(150)

		example_input_syntax_label = QLabel('Example Input: ')
		example_output_syntax_label = QLabel('Example Output: ')
		example_label_layout = QHBoxLayout()
		example_label_layout.addWidget(example_input_syntax_label)
		example_label_layout.addWidget(example_output_syntax_label)
		example_label_widget = QWidget()
		example_label_widget.setLayout(example_label_layout)

		example_input_syntax_content = QTextEdit()
		# example_input_syntax_content.setText(self.example_input_syntax)
		example_input_syntax_content.setFixedHeight(200)
		example_output_syntax_content = QTextEdit()
		# example_output_syntax_content.setText(self.example_output_syntax)
		example_output_syntax_content.setFixedHeight(200)
		example_layout = QHBoxLayout()
		example_layout.addWidget(example_input_syntax_content)
		example_layout.addWidget(example_output_syntax_content)
		example_widget = QWidget()
		example_widget.setLayout(example_layout)

		source_layout = QVBoxLayout()
		source_layout.addWidget(heading)
		source_layout.addWidget(level1_widget)
		source_layout.addWidget(statement_label)
		source_layout.addWidget(statement_content)
		source_layout.addWidget(input_syntax_label)
		source_layout.addWidget(input_syntax_content)
		source_layout.addWidget(output_syntax_label)
		source_layout.addWidget(output_syntax_content)
		source_layout.addWidget(constraints_label)
		source_layout.addWidget(constraints_content)
		source_layout.addWidget(example_label_widget)
		source_layout.addWidget(example_widget)
		# source_layout.addWidget(button_widget)
		
		source_layout.addStretch(1)
		source_widget = QWidget()
		source_widget.setLayout(source_layout)
		
		scroll_area = QScrollArea()
		scroll_area.setWidget(source_widget)
		scroll_area.setWidgetResizable(True)
		
		problem_label.setObjectName('main_screen_sub_heading')
		code_label.setObjectName('main_screen_sub_heading')
		statement_label.setObjectName('main_screen_sub_heading')
		input_syntax_label.setObjectName('main_screen_sub_heading')
		output_syntax_label.setObjectName('main_screen_sub_heading')
		constraints_label.setObjectName('main_screen_sub_heading')
		example_input_syntax_label.setObjectName('main_screen_sub_heading')
		example_output_syntax_label.setObjectName('main_screen_sub_heading')
		time_limit_label.setObjectName('main_screen_sub_heading')
		author_label.setObjectName('main_screen_sub_heading')
		heading.setObjectName('main_screen_heading')
		return scroll_area

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
		test_cases_table.setFixedHeight(560)
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
		widget.setFixedSize(self.width - 20, self.height - 80)
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
