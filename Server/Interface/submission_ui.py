from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import submissions_management, client_authentication
import json, time

class manage_submission_ui(QMainWindow):
	data_changed_flags = ''
	task_queue = ''
	run_id = ''
	client_id = ''
	pcode = ''
	language = ''
	timestamp = ''
	verdict = ''
	sent_status = ''

	verdict_dict = {
	'AC' : 'AC - Correct Answer', 
	'WA' : 'WA - Wrong Answer', 
	'TLE' : 'TLE - Time Limit Exceeded',
	'CMPL' : 'CMPL - Compilation Error',
	'PE' : 'PE - Presentation Error',
	'RE' : 'RE - Run Time Error',
	'OLE' : 'OLE - Output Limit Exceeded',
	'NZEC' : 'NZEC - Non Zero Exit Code'
	}
	inverted_verdict_dict = { v : k for k, v in verdict_dict.items()}
	
	def __init__(
			self, 
			data_changed_flags,
			task_queue, 
			log_queue,
			run_id,
			client_id,
			problem_code,
			language ,
			timestamp,
			verdict,
			sent_status,
			parent=None
		):
		super(manage_submission_ui, self).__init__(parent)
		# query_reply_ui.button_mode = 1

		self.data_changed_flags = data_changed_flags
		self.task_queue = task_queue
		self.log_queue = log_queue
		self.run_id = run_id
		self.client_id = client_id
		self.problem_code = problem_code
		self.language = language
		self.timestamp = timestamp
		self.verdict = verdict
		self.sent_status = sent_status

		width = 800
		height = 500
		self.setGeometry(550, 300, width, height)
		self.setWindowTitle('Run ' + str(run_id) + 'From Client ' + str(client_id))
		self.setFixedSize(width, height)
		main = self.main_manage_sub_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def log(self, text):
		self.log_queue.put(text)

	def main_manage_sub_ui(self):
		submission_heading = QLabel('Manual Validation')

		submission_sub_heading = QLabel('Run Information: ')
		team_name = client_authentication.get_client_username(self.client_id)
		run_id_label = QLabel("Run ID:  " + str(self.run_id))
		client_label = QLabel("Client:  " + team_name + '( ID: ' + str(self.client_id) + ')')
		problem_label = QLabel("Problem:  " + self.problem_code)
		language_label = QLabel("Language:  " + self.language)
		time_label = QLabel("Time:  " + self.timestamp)

		if self.sent_status == 'SENT':
			sent_text = QLabel("Response has been sent to the Team")
			sent_text.setObjectName('main_screen_green_content')
		elif self.sent_status == 'HALTED':
			sent_text = QLabel("<Security Exception> Judge NOT verified.")
			sent_text.setObjectName('main_screen_red_content')
		else:
			sent_text = QLabel("Waiting for Judgement")
			sent_text.setObjectName('main_screen_content')

		run_info_layout = QGridLayout()
		run_info_layout.addWidget(run_id_label, 0, 0)
		run_info_layout.addWidget(client_label, 0, 1)
		run_info_layout.addWidget(problem_label, 1, 0)
		run_info_layout.addWidget(language_label, 1, 1)
		run_info_layout.addWidget(time_label, 2, 0)
		run_info_layout.addWidget(sent_text, 3, 0)
		run_info_widget = QWidget()
		run_info_widget.setLayout(run_info_layout)

		verdict_sub_heading = QLabel("Judgement:")
		judge = submissions_management.get_judge(self.run_id)
		judge_verdict = QLabel(judge + ' Verdict:  ')

		try:
			verdict = QLabel(self.verdict_dict[self.verdict])
		except:
			verdict = QLabel(self.verdict)

		if self.verdict == 'AC':
			verdict.setObjectName('main_screen_green_content')
		else:
			verdict.setObjectName('main_screen_red_content')

		send_button = QPushButton("Accept Verdict")
		send_button.setFixedSize(200, 50)
		send_button.clicked.connect(lambda:manage_submission_ui.accept_verdict(self))
		manual_judgement_label = QLabel("Manual Judgement: ")
		manual_judgement_entry = QComboBox()
		manual_judgement_entry.addItem('<- SELECT ->')
		manual_judgement_entry.addItem(self.verdict_dict['AC'])
		manual_judgement_entry.addItem(self.verdict_dict['WA'])
		manual_judgement_entry.addItem(self.verdict_dict['TLE'])
		manual_judgement_entry.addItem(self.verdict_dict['CMPL'])
		manual_judgement_entry.addItem(self.verdict_dict['PE'])
		manual_judgement_entry.addItem(self.verdict_dict['RE'])
		manual_judgement_entry.addItem(self.verdict_dict['OLE'])
		manual_judgement_entry.addItem(self.verdict_dict['NZEC'])
		
		accept_select_button = QPushButton("Accept Selected")
		accept_select_button.setFixedSize(200, 50)
		accept_select_button.clicked.connect(
			lambda: manage_submission_ui.manual_verdict(
				self,  
				str(manual_judgement_entry.currentText())
			)
		)
		verdict_layout = QGridLayout()
		verdict_layout.addWidget(judge_verdict, 0, 0)
		verdict_layout.addWidget(verdict, 0, 1)
		verdict_layout.addWidget(send_button, 0, 2)
		verdict_layout.addWidget(manual_judgement_label, 1, 0)
		verdict_layout.addWidget(manual_judgement_entry, 1, 1)
		verdict_layout.addWidget(accept_select_button, 1, 2)	
		verdict_layout.setRowStretch(1,60)
		verdict_widget = QWidget()
		verdict_widget.setLayout(verdict_layout)

		rejudge_button = QPushButton('Rejudge')
		rejudge_button.setFixedSize(150, 40)
		rejudge_button.clicked.connect(
			lambda:manage_submission_ui.rejudge(self)
			)
		rejudge_button.setDefault(True)

		view_output_source_button = QPushButton('Submission Source and Data')
		view_output_source_button.setFixedSize(250, 40)
		view_output_source_button.clicked.connect(
			lambda:manage_submission_ui.load_submission_data(self)
			)
		view_output_source_button.setDefault(True)
		
		close_button = QPushButton('Close')
		close_button.setFixedSize(150, 40)
		close_button.clicked.connect(
			lambda:manage_submission_ui.close(self)
			)
		close_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addWidget(rejudge_button)
		button_layout.addWidget(view_output_source_button)
		button_layout.addWidget(close_button)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)

		spacer_item = QSpacerItem(0, 50, QSizePolicy.Expanding)
		
		main_layout = QVBoxLayout()
		main_layout.addWidget(submission_heading)
		main_layout.addWidget(submission_sub_heading)
		main_layout.addWidget(run_info_widget)
		main_layout.addWidget(verdict_sub_heading)
		main_layout.addWidget(verdict_widget)
		main_layout.addSpacerItem(spacer_item)
		main_layout.addWidget(button_widget)

		main_layout.addStretch(1)

		main = QWidget()
		main.setLayout(main_layout)

		main.setObjectName('account_window')
		run_info_widget.setObjectName('content_box')
		verdict_widget.setObjectName('content_box')

		submission_heading.setObjectName('main_screen_heading')

		submission_sub_heading.setObjectName('main_screen_sub_heading')
		verdict_sub_heading.setObjectName('main_screen_sub_heading')
		
		client_label.setObjectName('main_screen_content')
		problem_label.setObjectName('main_screen_content')
		language_label.setObjectName('main_screen_content')
		time_label.setObjectName('main_screen_content')
		run_id_label.setObjectName('main_screen_content')
		judge_verdict.setObjectName('main_screen_content')
		manual_judgement_label.setObjectName('main_screen_content')
		
		manual_judgement_entry.setObjectName('account_combobox')

		send_button.setObjectName('interior_button')
		accept_select_button.setObjectName('interior_button')
		rejudge_button.setObjectName('interior_button')
		view_output_source_button.setObjectName('interior_button')
		close_button.setObjectName('interior_button')
		return main

	def rejudge(self):
		print('[ EVENT ][ REJUDGE ] Run ' + str(self.run_id) + ' by ADMIN')
		self.log('[ EVENT ][ REJUDGE ] Run ' + str(self.run_id) + ' by ADMIN')
		client_username = client_authentication.get_client_username(self.client_id)
		file_name = submissions_management.get_source_file_name(self.run_id)
		if file_name == 'NONE':
			print('[ ERROR ] Source file not found!')
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Alert')
			info_box.setText('Source file not found!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return

		try:
			file = open("Client_Submissions/" + file_name ,"r")
			source_code = file.read()
			file.close()
		except:
			print('[ ERROR ] Source file could not be accessed!')
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Alert')
			info_box.setText('Source file could not be accessed!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return

		local_run_id = submissions_management.get_local_run_id(self.run_id)
		message = {
			'Code' : 'RJUDGE', 
			'Client ID' : self.client_id, 
			'Client Username' : client_username,
			'Run ID' : self.run_id,
			'Language' : self.language,
			'PCode' : self.problem_code,
			'Source' : source_code,
			'Local Run ID' : local_run_id,
			'Time Stamp' : self.timestamp
		}
		message = json.dumps(message)
		self.task_queue.put(message)
		self.data_changed_flags[8] = 0
		self.close()

	def manual_verdict(self, manual_verdict):
		if self.verdict == 'RUNNING':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Alert')
			info_box.setText('Verdict is not yet Recieved!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		elif self.verdict == 'SECURITY':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Security Alert')
			info_box.setText('Please Rejudge.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		elif manual_verdict == '<- SELECT ->':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Alert')
			info_box.setText('Please select a verdict.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		else:
			buttonReply = QMessageBox.question(
				self, 
				'Confirm Selection', 
				'Are you sure you want to give \'' + manual_verdict + '\' verdict', 
				QMessageBox.Yes | QMessageBox.No, 	# Button Options
				QMessageBox.No 			# Default button
			)
			if buttonReply == QMessageBox.Yes:
				pass
			else:
				return

		client_username = client_authentication.get_client_username(self.client_id)
		local_run_id = submissions_management.get_local_run_id(self.run_id)
		if self.inverted_verdict_dict[manual_verdict] == 'AC':
			show_message = 'Submission Passed all test cases!'
		else:
			show_message = 'Submission Failed to pass all test cases!' 

		message = {
			'Code' : 'VRDCT', 
			'Receiver' : client_username,
			'Local Run ID' : local_run_id,
			'Run ID' : self.run_id,
			'Status' : self.inverted_verdict_dict[manual_verdict],
			'Message' : show_message,
			'Judge' : 'ADMIN',
			'Client ID' : self.client_id,
			'Problem Code' : self.problem_code,
			'Timestamp' : self.timestamp
		}
		message = json.dumps(message)
		self.task_queue.put(message)
		print('[ VERDICT ][ SENT ] Manual Verdict:' + manual_verdict + 'Sent to Client ' + client_username)
		self.log('[ VERDICT ][ SENT ] Manual Verdict:' + manual_verdict + 'Sent to Client ' + client_username)

		# Write data to file
		filename = './Client_Submissions/' + str(self.run_id) + '.info'
		current_time = time.strftime("%H:%M:%S", time.localtime())
		# Read previous data
		try:
			# read file
			with open(filename) as file:
				data = file.read()
		except:
			# New file write
			data = '=========='
			pass

		try:
			# write file
			file = open(filename, 'w')
			file.write('Run Time: ' + current_time + '\n')
			file.write('Verdict from: ' + 'ADMIN' + ' : ' + self.inverted_verdict_dict[manual_verdict] + '\n')
			file.write(show_message)
			file.write('\n\n')
			# Write previous run info
			# This ensures the latest run data is at top
			file.write(data)
			file.close()
		except Exception as error:
			print('[ ERROR ] Judge verdict could not be written in the file!' + str(error))
			# self.log('[ ERROR ] Judge verdict could not be written in the file!' + str(error))
		try:
			# write file
			filename = './Client_Submissions/' + str(self.run_id) + '_latest.info'
			file = open(filename, 'w')
			file.write(show_message)
			file.close()
		except Exception as error:
			print('[ ERROR ] Judge verdict could not be written in the file!' + str(error))
			# self.log('[ ERROR ] Judge verdict could not be written in the file!' + str(error))

		self.data_changed_flags[8] = 0
		self.data_changed_flags[18] = 1
		self.close()

	def accept_verdict(self):
		if self.verdict == 'RUNNING':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Alert')
			info_box.setText('Verdict is not yet Recieved!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		elif self.verdict == 'SECURITY':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Security Alert')
			info_box.setText('Please Rejudge.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return

		client_username = client_authentication.get_client_username(self.client_id)
		local_run_id = submissions_management.get_local_run_id(self.run_id)
		judge = submissions_management.get_judge(self.run_id)
		
		message = {
			'Code' : 'VRDCT', 
			'Receiver' : client_username,
			'Local Run ID' : local_run_id,
			'Run ID' : self.run_id,
			'Status' : self.verdict,
			'Message' : self.get_message(self.run_id),
			'Judge' : judge,
			'Client ID' : self.client_id,
			'Problem Code' : self.problem_code,
			'Timestamp' : self.timestamp
		}
		message = json.dumps(message)
		self.task_queue.put(message)
		print('[ VERDICT ][ SENT ] Judge Verdict accepted and sent to Client ' + client_username)

		self.data_changed_flags[8] = 0
		self.close()

	def get_message(self, run_id):
		try:
			filename = './Client_Submissions/' + str(self.run_id) + '_latest.info'
			with open(filename) as file:
				data = file.read()
			if data != '':
				return data
			else:
				return 'No Error data received!'
		except:
			return 'No Error data received!'

	def load_submission_data(self):
		self.submission_ui = submission_data_ui(self.data_changed_flags, self.run_id, self.log_queue)
		self.data_changed_flags[8] = 0
		self.submission_ui.show()

	def cancel(self):
		self.data_changed_flags[8] = 0
		self.close()

class submission_data_ui(QMainWindow):
	def __init__(
			self, 
			data_changed_flags, 
			run_id, 
			log_queue,
			parent = None
		):
		super(submission_data_ui, self).__init__(parent)
		
		self.data_changed_flags = data_changed_flags
		self.run_id = run_id
		self.log_queue = log_queue
		
		self.setWindowTitle('Run ' + str(self.run_id))

		width = 800
		height = 500
		self.setGeometry(550, 300, width, height)
		self.setFixedSize(width, height)
		main = self.main_submission_data_ui()
		self.setCentralWidget(main)
		return

	def main_submission_data_ui(self):
		self.tabs = QTabWidget()
		self.tabs.setObjectName('main_tabs')
		self.tab_bar = QTabBar()
		self.tab_bar.setObjectName('problem_tabs')

		self.tab1 = self.get_tab1_widget()
		self.tab2 = self.get_tab2_widget()
		
		self.tabs.addTab(self.tab1, '')
		self.tabs.addTab(self.tab2, '')
		self.tab_bar.addTab('Source Data')
		self.tab_bar.addTab('Error Data')
		self.tabs.setTabBar(self.tab_bar)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.tabs)
		main = QWidget()
		main.setLayout(main_layout)

		main.setObjectName('account_window')
		return main

	def get_tab1_widget(self):
		source_layout = QVBoxLayout()
		heading1 = QLabel('Source Data')

		# Read source file
		filename = './Client_Submissions/' + submissions_management.get_source_file_name(self.run_id)
		file_label = QLabel('File: ')
		filename_label = QLabel(filename)
		label_layout = QHBoxLayout()
		label_layout.addWidget(file_label)
		label_layout.addWidget(filename_label)
		label_layout.addStretch(1)
		label_widget = QWidget()
		label_widget.setLayout(label_layout)
		try:
			with open(filename) as file:
				data = file.read()
		except:
			data = 'Error: File not found!'

		content = QTextEdit()
		content.setText(data)

		source_layout.addWidget(heading1)
		source_layout.addWidget(label_widget)
		source_layout.addWidget(content)
		source_widget = QWidget()
		source_widget.setLayout(source_layout)

		heading1.setObjectName('main_screen_heading')
		file_label.setObjectName('main_screen_sub_heading')
		filename_label.setObjectName('main_screen_content')
		return source_widget

	def get_tab2_widget(self):
		error_layout = QVBoxLayout()
		heading1 = QLabel('Error Data')
		# Read error file
		filename = './Client_Submissions/' + str(self.run_id) + '.info'
		file_label = QLabel('File: ')
		filename_label = QLabel(filename)
		label_layout = QHBoxLayout()
		label_layout.addWidget(file_label)
		label_layout.addWidget(filename_label)
		label_layout.addStretch(1)
		label_widget = QWidget()
		label_widget.setLayout(label_layout)
		try:
			with open(filename) as file:
				data = file.read()
		except:
			data = 'Error: File not found!'

		content = QTextEdit()
		content.setText(data)

		error_layout.addWidget(heading1)
		error_layout.addWidget(label_widget)
		error_layout.addWidget(content)
		error_widget = QWidget()
		error_widget.setLayout(error_layout)

		heading1.setObjectName('main_screen_heading')
		file_label.setObjectName('main_screen_sub_heading')
		filename_label.setObjectName('main_screen_content')
		return error_widget
