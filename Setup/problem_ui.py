from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import *
from shutil import copyfile
from view_case_ui import view_case_ui
import json, os

class add_problem_ui(QMainWindow):
	def __init__(
			self,
			config,
			wizard,
			problem_signal_mapper,
			problem_tests_mapper,
			parent=None
		):
		super(add_problem_ui, self).__init__(parent)
		
		self.config = config
		self.wizard = wizard
		self.problem_signal_mapper = problem_signal_mapper
		self.problem_tests_mapper = problem_tests_mapper
		self.setFocus()

		self.problem = ''
		self.code = ''
		self.time_limit = ''
		self.author = ''
		self.statement = ''
		self.input_syntax= '' 
		self.output_syntax= ''
		self.constraints= ''
		self.example_input_syntax= '' 
		self.example_output_syntax= '' 

		self.setWindowTitle("[ SETUP ] Problem")
		self.setWindowIcon(QIcon('Elements/logo.png'))
		self.width = 1200
		self.height = 750
		self.setGeometry(400, 100, self.width, self.height)
		self.setFixedSize(self.width, self.height)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		self.setWindowFlags(Qt.WindowStaysOnTopHint);

		self.add_problem_widget = self.get_problem_widget()

		self.title = QLabel("Add Problem")
		self.title.setObjectName('main_screen_heading')
		self.import_xml_file_button = QPushButton("Import XML")
		self.import_xml_file_button.setToolTip('Work in progress')
		self.import_xml_file_button.clicked.connect(self.import_xml)
		self.header_widget = QWidget()
		self.header_layout = QHBoxLayout(self.header_widget)
		self.header_layout.addWidget(self.title)
		self.header_layout.addStretch(1)
		self.header_layout.addWidget(self.import_xml_file_button)
		
		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(150, 40)
		confirm_button.clicked.connect(lambda:self.final_status())
		confirm_button.setDefault(True)
		confirm_button.setObjectName('interior_button')
		
		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(150, 40)
		cancel_button.clicked.connect(lambda:self.exit())
		cancel_button.setObjectName('interior_button')
		cancel_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addStretch(5)
		button_layout.addWidget(confirm_button)
		button_layout.addStretch(1)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(5)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)
		button_widget.setContentsMargins(0, 20, 0, 0)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.header_widget)
		main_layout.addWidget(self.add_problem_widget)
		main_layout.addWidget(button_widget)
		main_layout.setStretch(0, 10)
		main_layout.setStretch(1, 80)
		main_layout.setStretch(2, 10)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName('account_window')
		self.setCentralWidget(main)

	def import_xml(self):
		pass

	def get_problem_widget(self):
		problem_label = QLabel('Name: ')
		self.problem_content = QLineEdit()
		self.problem_content.setText(self.problem)
		self.problem_content.setFixedSize(250, 28)
			
		code_label = QLabel('Code: ')
		self.code_content = QLineEdit()
		self.code_content.setText(self.code)
		self.code_content.setFixedSize(70, 28)
		
		time_limit_label = QLabel('Time Limit: ')
		self.time_limit_content = QLineEdit()
		self.time_limit_content.setText(str(self.time_limit))
		self.time_limit_content.setFixedSize(70, 28)

		author_label = QLabel('Author: ')
		self.author_content = QLineEdit()
		self.author_content.setText(str(self.author))
		self.author_content.setFixedSize(150, 28)
		
		level1_layout = QHBoxLayout()
		level1_layout.addWidget(problem_label)
		level1_layout.addWidget(self.problem_content)
		level1_layout.addStretch(20)
		level1_layout.addWidget(code_label)
		level1_layout.addWidget(self.code_content)
		level1_layout.addStretch(20)
		level1_layout.addWidget(time_limit_label)
		level1_layout.addWidget(self.time_limit_content)
		level1_layout.addStretch(20)
		level1_layout.addWidget(author_label)
		level1_layout.addWidget(self.author_content)
		level1_widget = QWidget()
		level1_widget.setLayout(level1_layout)

		statement_label = QLabel('Problem Statement: ')
		self.statement_content = QTextEdit()
		self.statement_content.setText(self.statement)
		# self.statement_content.setFixedHeight(500)
		self.statement_content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
		
		input_syntax_label = QLabel('Input Format: ')
		self.input_syntax_content = QTextEdit()
		self.input_syntax_content.setText(self.input_syntax)
		self.input_syntax_content.setFixedHeight(200)
		
		output_syntax_label = QLabel('Output Format: ')
		self.output_syntax_content = QTextEdit()
		self.output_syntax_content.setText(self.output_syntax)
		self.output_syntax_content.setFixedHeight(200)
		
		constraints_label = QLabel('Constraints: ')
		self.constraints_content = QTextEdit()
		self.constraints_content.setText(self.constraints)
		self.constraints_content.setFixedHeight(150)
		
		example_input_syntax_label = QLabel('Example Input: ')
		example_output_syntax_label = QLabel('Example Output: ')
		example_label_layout = QHBoxLayout()
		example_label_layout.addWidget(example_input_syntax_label)
		example_label_layout.addWidget(example_output_syntax_label)
		example_label_widget = QWidget()
		example_label_widget.setLayout(example_label_layout)

		self.example_input_syntax_content = QTextEdit()
		self.example_input_syntax_content.setText(self.example_input_syntax)
		self.example_input_syntax_content.setFixedHeight(200)
		
		self.example_output_syntax_content = QTextEdit()
		self.example_output_syntax_content.setText(self.example_output_syntax)
		self.example_output_syntax_content.setFixedHeight(200)
		
		example_layout = QHBoxLayout()
		example_layout.addWidget(self.example_input_syntax_content)
		example_layout.addWidget(self.example_output_syntax_content)
		example_widget = QWidget()
		example_widget.setLayout(example_layout)

		source_layout = QVBoxLayout()
		source_layout.addWidget(level1_widget)
		source_layout.addWidget(statement_label)
		source_layout.addWidget(self.statement_content)
		source_layout.addWidget(input_syntax_label)
		source_layout.addWidget(self.input_syntax_content)
		source_layout.addWidget(output_syntax_label)
		source_layout.addWidget(self.output_syntax_content)
		source_layout.addWidget(constraints_label)
		source_layout.addWidget(self.constraints_content)
		source_layout.addWidget(example_label_widget)
		source_layout.addWidget(example_widget)
		
		source_layout.addStretch(1)
		source_widget = QWidget()
		source_widget.setLayout(source_layout)
		source_widget.setToolTip(
			'Use \'<=\', \'>=\' and \'!=\' for \'less than or equal to\', \n\'greater than or equal to\' and \'not equal to\' symbols respectively.'
		)
		
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
		return scroll_area

	def modify(self, content_data):
		try:
			content_data = content_data.replace('<=', '\u2264')
			content_data = content_data.replace('>=', '\u2265')
			content_data = content_data.replace('!=', '\u2260')
			content_data = content_data.replace('"', '\u0022')
			content_data = content_data.replace("'", '\u0027')
			return content_data
		except:
			return content_data
	
	def final_status(self):	
		if self.code_content.text() == 'NULL':
			self.code_content.setText('')

		problem_name = self.modify(self.problem_content.text())
		problem_code = self.modify(self.code_content.text())
		author = self.modify(self.author_content.text())
		time_limit = self.modify(self.time_limit_content.text())
		statement = self.modify(self.statement_content.toPlainText())
		input_data = self.modify(self.input_syntax_content.toPlainText())
		output_data = self.modify(self.output_syntax_content.toPlainText())
		constraints = self.modify(self.constraints_content.toPlainText())
		example_input = self.modify(self.example_input_syntax_content.toPlainText())
		example_output = self.modify(self.example_output_syntax_content.toPlainText())

		# Check Necessary fields
		status = self.check_problem(
			problem_name,
			problem_code,
			time_limit,
			statement,
			input_data,
			output_data,
		)

		if status == 0:
			error_box(self.wizard.available_width, self.wizard.available_height)
			return

		problem = {
			"Name" : problem_name,
			"Code" : problem_code,
			"Time Limit" : time_limit,
			"Author" : author,
			"Statement" : statement,
			"Input" : input_data,
			"Output" : output_data,
			"Constraints" : constraints,
			"Example Input" : example_input,
			"Example Output" : example_output,
			"Max Score" : 100
		}

		problem_number = self.wizard.number_of_problems + 1
		self.wizard.number_of_problems += 1
		problem_id = "Problem " + str(problem_number) 
		self.wizard.problems[problem_id] = problem

		# Make problem directory for test data
		try:
			os.mkdir('./Problems/' + problem_code)
		except FileExistsError:
			pass
		except Exception as error:
			print(
				'[ CRITICAL ] The current directory requires sudo elevation to create folders.' + 
				'\nRestart Setup with sudo privileges.'
			)
			return

		card_widget = QWidget()
		card_widget.setFixedHeight(100)
		card_widget.setObjectName('problem_card')
		card_layout = QHBoxLayout(card_widget)
		main_label = QLabel( problem_id + " : ")
		main_label.setObjectName('main_screen_content')
		problem_name_widget = QLabel(problem_name)
		problem_name_widget.setObjectName('main_screen_sub_heading')
		problem_code_widget = QLabel(" [ " + problem_code + " ] ")
		problem_code_widget.setObjectName('main_screen_sub_heading2')
		problem_open_widget = QPushButton('Open')
		problem_test_files_widget = QPushButton('Test Files')
		card_layout.addWidget(main_label)
		card_layout.addWidget(problem_name_widget)
		card_layout.addWidget(problem_code_widget)
		card_layout.addStretch(1)
		card_layout.addWidget(problem_test_files_widget)
		card_layout.addWidget(problem_open_widget)
		card_layout.setAlignment(Qt.AlignLeft)
		card_layout.setAlignment(problem_open_widget, Qt.AlignRight)
		card_layout.setAlignment(problem_test_files_widget, Qt.AlignRight)
		# OKAY this line is long :D 
		# Basically it accesses the QScrollWidget and adds out problem card to it
		# How? You ask.
		# Well, Qt Magic!!
		self.wizard.problems_page.layout().itemAt(1).widget().layout().itemAt(1).widget().widget().layout().addWidget(card_widget)
		#    wizard->WizardPage->layout-> mainWidget ----->main_layout---->scrollArea---->problems_list_layout--> Add this card
		self.problem_signal_mapper.setMapping(
				problem_open_widget, 
				problem_number
			)
		self.problem_tests_mapper.setMapping(
				problem_test_files_widget, 
				problem_number
			)
		problem_open_widget.clicked.connect(self.problem_signal_mapper.map)
		problem_test_files_widget.clicked.connect(self.problem_tests_mapper.map)

		self.wizard.setVisible(True)
		self.close()

	def check_problem(
			self,
			problem_name,
			problem_code,
			time_limit,
			statement,
			input_data,
			output_data,
		):
		try:
			time_limit = int(time_limit)
		except:
			# If non decimal time limit is written
			return 0

		if (
				problem_name == '' or 
				problem_code == '' or
				problem_code == 'NULL' or
				time_limit == '' or
				time_limit <= 0 or
				statement == '' or
				input_data == '' or
				output_data == ''
			):
			return 0
		else:
			return 1

	def exit(self):
		self.wizard.setVisible(True)
		self.close()

class error_box(QMessageBox):
	def __init__(
			self,
			screen_width,
			screen_height,
			parent=None
		):
		super(error_box, self).__init__()
		
		self.move(
			( screen_width - self.width() ) / 2,
			( screen_height - self.height() ) / 2
		)
		self.information(
			self, 
			'Alert', 
			'Some essential fields are left empty!', 
			self.Ok,
			self.NoButton 			    # Default button
		)

class remove_all_problems(QMessageBox):
	def __init__(
			self,
			wizard,
			scroll_area,
			parent=None
		):
		super(remove_all_problems, self).__init__()
		
		self.wizard = wizard
		self.scroll_area = scroll_area
		self.screen_width = self.wizard.available_width
		self.screen_height = self.wizard.available_height
		self.move(
			( self.screen_width - self.width() ) / 2,
			( self.screen_height - self.height() ) / 2
		)

		buttonReply = self.question(
			self, 
			'Reset Problems', 
			'Are you sure you want to reset all the problems?', 
			self.Yes | self.No, 	# Button Options
			self.No 			    # Default button
		)
		if buttonReply == self.No:
			print('[ DELETION ] Cancelled')
			return
		# Deletion initiated
		# Clear the problem list card_widget
		widget = self.scroll_area.widget()
		for i in range(self.wizard.number_of_problems , 0, -1):
			print('[ DELETE ] Remove problem ', i)
			problem_widget = widget.layout().itemAt(i - 1).widget()
			widget.layout().removeWidget(problem_widget)
			problem_widget.deleteLater()
			problem_widget = None

		# Clear the dict
		self.wizard.problems.clear()
		self.wizard.number_of_problems = 0

		print('[ SETUP ] Removed all problems...')


# A LOT of redundant code,
# Plan to merge this and the add problem classes together,
# Right now, this is pretty much same as the add_problem class except 
# the __init__ method.
class edit_problem_ui(QMainWindow):
	def __init__(
			self,
			problem_id,
			config,
			wizard,
			parent=None
		):
		super(edit_problem_ui, self).__init__(parent)
		
		self.config = config
		self.wizard = wizard
		self.problem_id = problem_id
		self.setFocus()

		(
			self.problem,
			self.code,
			self.time_limit,
			self.author,
			self.statement,
			self.input_syntax, 
			self.output_syntax,
			self.constraints,
			self.example_input_syntax, 
			self.example_output_syntax 
		) = self.get_problem_details(problem_id)

		self.setWindowTitle("[ SETUP ] View Problem")
		self.setWindowIcon(QIcon('Elements/logo.png'))
		self.width = 1200
		self.height = 750
		self.setGeometry(300, 100, self.width, self.height)
		self.setFixedSize(self.width, self.height)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		self.setWindowFlags(Qt.WindowStaysOnTopHint);

		self.add_problem_widget = self.get_problem_widget()

		self.title = QLabel("Edit Problem")
		self.title.setObjectName('main_screen_heading')

		self.header_widget = QWidget()
		self.header_layout = QHBoxLayout(self.header_widget)
		self.header_layout.addWidget(self.title)
		self.header_layout.addStretch(1)
		
		confirm_button = QPushButton('Update')
		confirm_button.setFixedSize(150, 40)
		confirm_button.clicked.connect(lambda:self.final_status())
		confirm_button.setDefault(True)
		confirm_button.setObjectName('interior_button')
		
		cancel_button = QPushButton('Close')
		cancel_button.setFixedSize(150, 40)
		cancel_button.clicked.connect(lambda:self.exit())
		cancel_button.setObjectName('interior_button')
		cancel_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addStretch(5)
		button_layout.addWidget(confirm_button)
		button_layout.addStretch(1)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(5)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)
		button_widget.setContentsMargins(0, 20, 0, 0)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.header_widget)
		main_layout.addWidget(self.add_problem_widget)
		main_layout.addWidget(button_widget)
		main_layout.setStretch(0, 10)
		main_layout.setStretch(1, 80)
		main_layout.setStretch(2, 10)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName('account_window')
		self.setCentralWidget(main)

	def import_xml(self):
		pass

	def get_problem_details(self, problem_id):
		problem_id = "Problem " + str(problem_id)
		problem_dict = self.wizard.problems.get(problem_id, "NONE")
		if problem_dict == "NONE":
			print('[ ERROR ] Problem not found!')
			return ('', '', '', '', '', '', '', '', '', '')

		problem = problem_dict.get('Name', '')
		code = problem_dict.get('Code', '')
		time_limit = problem_dict.get('Time Limit', '')
		author = problem_dict.get('Author', '')
		statement = problem_dict.get('Statement', '')
		input_syntax = problem_dict.get('Input', '')
		output_syntax = problem_dict.get('Output', '')
		constraints = problem_dict.get('Constraints', '')
		example_input_syntax = problem_dict.get('Example Input', '')
		example_output_syntax = problem_dict.get('Example Output', '')
		return (
			problem,
			code,
			time_limit,
			author,
			statement,
			input_syntax,
			output_syntax,
			constraints,
			example_input_syntax,
			example_output_syntax
		)

	def get_problem_widget(self):
		problem_label = QLabel('Name: ')
		self.problem_content = QLineEdit()
		self.problem_content.setReadOnly(True)
		self.problem_content.setText(self.problem)
		self.problem_content.setFixedSize(250, 28)
			
		code_label = QLabel('Code: ')
		self.code_content = QLineEdit()
		self.code_content.setReadOnly(True)
		self.code_content.setText(self.code)
		self.code_content.setFixedSize(70, 28)
		
		time_limit_label = QLabel('Time Limit: ')
		self.time_limit_content = QLineEdit()
		self.time_limit_content.setText(str(self.time_limit))
		self.time_limit_content.setFixedSize(70, 28)

		author_label = QLabel('Author: ')
		self.author_content = QLineEdit()
		self.author_content.setText(str(self.author))
		self.author_content.setFixedSize(150, 28)
		
		level1_layout = QHBoxLayout()
		level1_layout.addWidget(problem_label)
		level1_layout.addWidget(self.problem_content)
		level1_layout.addStretch(20)
		level1_layout.addWidget(code_label)
		level1_layout.addWidget(self.code_content)
		level1_layout.addStretch(20)
		level1_layout.addWidget(time_limit_label)
		level1_layout.addWidget(self.time_limit_content)
		level1_layout.addStretch(20)
		level1_layout.addWidget(author_label)
		level1_layout.addWidget(self.author_content)
		level1_widget = QWidget()
		level1_widget.setLayout(level1_layout)

		statement_label = QLabel('Problem Statement: ')
		self.statement_content = QTextEdit()
		self.statement_content.setText(self.statement)
		self.statement_content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
		
		input_syntax_label = QLabel('Input Format: ')
		self.input_syntax_content = QTextEdit()
		self.input_syntax_content.setText(self.input_syntax)
		self.input_syntax_content.setFixedHeight(200)
		
		output_syntax_label = QLabel('Output Format: ')
		self.output_syntax_content = QTextEdit()
		self.output_syntax_content.setText(self.output_syntax)
		self.output_syntax_content.setFixedHeight(200)
		
		constraints_label = QLabel('Constraints: ')
		self.constraints_content = QTextEdit()
		self.constraints_content.setText(self.constraints)
		self.constraints_content.setFixedHeight(150)
		
		example_input_syntax_label = QLabel('Example Input: ')
		example_output_syntax_label = QLabel('Example Output: ')
		example_label_layout = QHBoxLayout()
		example_label_layout.addWidget(example_input_syntax_label)
		example_label_layout.addWidget(example_output_syntax_label)
		example_label_widget = QWidget()
		example_label_widget.setLayout(example_label_layout)

		self.example_input_syntax_content = QTextEdit()
		self.example_input_syntax_content.setText(self.example_input_syntax)
		self.example_input_syntax_content.setFixedHeight(200)
		
		self.example_output_syntax_content = QTextEdit()
		self.example_output_syntax_content.setText(self.example_output_syntax)
		self.example_output_syntax_content.setFixedHeight(200)
		
		example_layout = QHBoxLayout()
		example_layout.addWidget(self.example_input_syntax_content)
		example_layout.addWidget(self.example_output_syntax_content)
		example_widget = QWidget()
		example_widget.setLayout(example_layout)

		source_layout = QVBoxLayout()
		source_layout.addWidget(level1_widget)
		source_layout.addWidget(statement_label)
		source_layout.addWidget(self.statement_content)
		source_layout.addWidget(input_syntax_label)
		source_layout.addWidget(self.input_syntax_content)
		source_layout.addWidget(output_syntax_label)
		source_layout.addWidget(self.output_syntax_content)
		source_layout.addWidget(constraints_label)
		source_layout.addWidget(self.constraints_content)
		source_layout.addWidget(example_label_widget)
		source_layout.addWidget(example_widget)
		
		source_layout.addStretch(1)
		source_widget = QWidget()
		source_widget.setLayout(source_layout)
		source_widget.setToolTip(
			'Use \'<=\', \'>=\' and \'!=\' for \'less than or equal to\', \n\'greater than or equal to\' and \'not equal to\' symbols respectively.'
		)
		
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
		return scroll_area

	def modify(self, content_data):
		try:
			content_data = content_data.replace('<=', '\u2264')
			content_data = content_data.replace('>=', '\u2265')
			content_data = content_data.replace('!=', '\u2260')
			content_data = content_data.replace('"', '\u0022')
			content_data = content_data.replace("'", '\u0027')
			
			return content_data
		except:
			print('[ ERROR ] An exception occured during editing. [ HANDLED ]')
			return content_data
	
	def final_status(self):	
		problem_name = self.modify(self.problem_content.text())
		problem_code = self.modify(self.code_content.text())
		author = self.modify(self.author_content.text())
		time_limit = self.modify(self.time_limit_content.text())
		statement = self.modify(self.statement_content.toPlainText())
		input_data = self.modify(self.input_syntax_content.toPlainText())
		output_data = self.modify(self.output_syntax_content.toPlainText())
		constraints = self.modify(self.constraints_content.toPlainText())
		example_input = self.modify(self.example_input_syntax_content.toPlainText())
		example_output = self.modify(self.example_output_syntax_content.toPlainText())

		# Check Necessary fields
		status = self.check_problem(
			time_limit,
			statement,
			input_data,
			output_data,
		)

		if status == 0:
			error_box(self.wizard.available_width, self.wizard.available_height)
			return

		problem = {
			"Name" : problem_name,
			"Code" : problem_code,
			"Time Limit" : time_limit,
			"Author" : author,
			"Statement" : statement,
			"Input" : input_data,
			"Output" : output_data,
			"Constraints" : constraints,
			"Example Input" : example_input,
			"Example Output" : example_output,
			"Max Score" : 100
		}
		problem_id = "Problem " + str(self.problem_id) 
		self.wizard.problems[problem_id] = problem
		self.wizard.setVisible(True)
		self.close()

	def check_problem(
			self,
			time_limit,
			statement,
			input_data,
			output_data,
		):
		try:
			time_limit = int(time_limit)
		except:
			return 0
		if (
				time_limit == '' or
				time_limit <= 0 or
				statement == '' or
				input_data == '' or
				output_data == ''
			):
			return 0
		else:
			return 1

	def exit(self):
		self.wizard.setVisible(True)
		self.close()

class test_files_ui(QMainWindow):
	problem_path = ''
	text_box = ''
	line_endings_shown = 0
	backup_file_content = ''
	file_not_found = 0

	def __init__(
			self,
			p_id, 
			wizard,
			parent=None
		):
		super(test_files_ui, self).__init__(parent)
		self.p_id = p_id
		self.wizard = wizard

		self.problem_id = 'Problem ' + str(self.p_id)
		self.problem = self.wizard.problems.get(self.problem_id, {"Code" : "NULL"})
		self.problem_code = self.problem.get('Code')
		
		self.setWindowTitle('Problem ' + str(p_id))
		self.setWindowIcon(QIcon('Elements/logo.png'))
		self.width = 1200
		self.height = 750
		self.setGeometry(300, 100, self.width, self.height)
		self.setFixedSize(self.width, self.height)
		main = self.main_test_files_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_test_files_ui(self):
		heading = QLabel('All Test Files')
		import_folder_button = QPushButton('Add Test Files')
		import_folder_button.clicked.connect(self.get_test_files)

		topbar_widget = QWidget()
		topbar_layout = QHBoxLayout(topbar_widget)
		topbar_layout.addWidget(heading)
		topbar_layout.addStretch(1)
		topbar_layout.addWidget(import_folder_button)

		self.test_cases_table = QTableWidget()
		self.test_cases_table.setColumnCount(2)
		self.test_cases_table.setObjectName('inner_table')
		self.test_cases_table.setHorizontalHeaderLabels(
			("Input Files", "Output Files")
		)
		self.test_cases_table.resizeColumnsToContents()
		self.test_cases_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.test_cases_table.setAlternatingRowColors(True)
		
		vertical_header = self.test_cases_table.verticalHeader()
		vertical_header.setVisible(False)
		horizontal_header = self.test_cases_table.horizontalHeader()
		horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
		# Add older files if exists
		number_of_files = self.wizard.problems['Problem ' + str(self.p_id)]['IO Files']
		self.test_cases_table.setRowCount(number_of_files)
		for i in range(number_of_files):
			dest = "{0:02}".format(i)
			for j in range(0, 2):
				if j == 0:
					self.test_cases_table.setItem(i, j, QTableWidgetItem('input' + dest + '.in'))
				else:
					self.test_cases_table.setItem(i, j, QTableWidgetItem('output' + dest + '.ans'))

		# Make test files viewable
		self.test_cases_table.cellDoubleClicked.connect(
			lambda:self.manage_io_file(
				self.problem_code,
				self.test_cases_table.selectionModel().currentIndex().row(),
				self.test_cases_table.selectionModel().currentIndex().column()
			)
		)

		close_button = QPushButton('Close')
		close_button.setFixedSize(150, 40)
		close_button.clicked.connect(lambda:self.exit())
		close_button.setObjectName('interior_button')
		close_button.setDefault(True)
		button_widget = QWidget()
		button_layout = QHBoxLayout(button_widget)
		button_layout.addWidget(close_button)
		button_layout.setAlignment(Qt.AlignCenter)
		
		main_layout = QVBoxLayout()
		main_layout.addWidget(topbar_widget)
		main_layout.addWidget(self.test_cases_table)
		main_layout.addWidget(button_widget)
		main_layout.setStretch(0, 10)
		main_layout.setStretch(1, 80)
		main_layout.setStretch(2, 10)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName('account_window')
		heading.setObjectName('main_screen_heading')
		return main

	def get_test_files(self):
		file_dialog = QFileDialog()
		file_dialog.setFileMode(QFileDialog.Directory)
		file_dialog.setOption(QFileDialog.ShowDirsOnly)
		file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
		folder_path = file_dialog.getExistingDirectory(self, 'Select Test Case Folder')
		if folder_path == '':
			# No folder selected i.e., selection cancelled or closed
			return
		
		# Number of input and output files
		input_files = 0
		output_files = 0
		# List of input and output file names
		self.input_files_list = []
		self.output_files_list = []

		for i in os.listdir(folder_path):
			if i.endswith(".in"):
				input_files += 1
				self.input_files_list.append(i)
			elif i.endswith(".ans"):
				output_files += 1
				self.output_files_list.append(i)

		if input_files != output_files:
			print('[ ERROR ] Unequal number of input and output files in the folder!')
			return
		elif input_files == 0 or output_files == 0:
			print('[ ERROR ] At least one each of Input and Output files must be there.')
			return

		if self.problem_code == 'NULL':
			print('[ ERROR ] Problem content not found!')
			return
		
		# Clear the Problem Code folder
		for any_file in os.listdir('./Problems/' + self.problem_code + '/'):
			os.remove('./Problems/' + self.problem_code + '/' + any_file)

		# Add this folder path to our configuration
		self.wizard.problems[self.problem_id]["Test File Path"] = folder_path

		# Update configuration for number of input and output files to expect
		self.wizard.problems[self.problem_id]['IO Files'] = input_files
		
		# Sort these lists to get test data in correct order
		self.input_files_list.sort()
		self.output_files_list.sort()

		try:
			for i in range(input_files):
				dest = "{0:02}".format(i)
				# Copy Input files
				copyfile(
					folder_path + '/' + self.input_files_list[i],
					'./Problems/' + self.problem_code + '/input' + dest + '.in'
				)
				self.input_files_list[i] = 'input' + dest + '.in'
				# Copy Output files
				copyfile(
					folder_path + '/' + self.output_files_list[i],
					'./Problems/' + self.problem_code + '/output' + dest + '.ans'
				)
				self.output_files_list[i] = 'output' + dest + '.ans'

			self.wizard.problems[self.problem_id]["Test File Path"] = './Problems/' + self.problem_code + '/'

			self.test_cases_table.setRowCount(input_files)
			for i in range(input_files):
				for j in range(2):
					if j == 0:
						self.test_cases_table.setItem(i,j, QTableWidgetItem(self.input_files_list[i]))
					if j == 1:
						self.test_cases_table.setItem(i,j, QTableWidgetItem(self.output_files_list[i]))

		except Exception as Error:
			QMessageBox.warning(self, 'Error', str(Error))
		finally:
			return

	def manage_io_file(self, problem_code, row, column):
		if column == 0:
			# Input file is selected
			# Get file name:
			input_file_name = self.test_cases_table.item(row, column).text()

			file_path = "./Problems/" + problem_code + "/" + input_file_name 
			self.ui = view_case_ui(
				file_path
			)
			self.ui.show()
		elif column == 1:
			# Output file is selected
			# Get file name:
			output_file_name = self.test_cases_table.item(row, column).text()
			file_path = "./Problems/" + problem_code + "/" + output_file_name 
			self.ui = view_case_ui(
				file_path
			)
			self.ui.show()
		return

	def exit(self):
		self.wizard.setVisible(True)
		self.close()