from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import submissions_management, client_authentication
import json, time

class rejudge_problem_ui(QMainWindow):
	select_text = '<- SELECT ->'
	data_changed_flags = ''
	task_queue = ''
	problem_codes = ''
	selected_code = select_text
	client_list = ''
	selected_client = select_text
	
	def __init__(
			self, 
			data_changed_flags, 
			task_queue,
			log_queue,
			codes = [], 
			client_list = [], 
			parent=None
		):
		super(rejudge_problem_ui, self).__init__(parent)
		rejudge_problem_ui.data_changed_flags = data_changed_flags
		rejudge_problem_ui.task_queue = task_queue
		self.log_queue = log_queue
		try:
			rejudge_problem_ui.problem_codes = eval(codes)
		except:
			rejudge_problem_ui.problem_codes = codes
		try:
			rejudge_problem_ui.client_list = eval(client_list)
		except:
			rejudge_problem_ui.client_list = client_list

		self.setGeometry(700, 350, 300, 200)
		self.setWindowTitle('Rejudge Problems')
		self.setFixedSize(500, 300)
		main = self.add_rejudge_problem_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def log(self, text):
		self.log_queue.put(text)

	def code_combo_box_data_changed(text):
		if text != rejudge_problem_ui.select_text:
			rejudge_problem_ui.selected_code = str(text)
		
	def client_combo_box_data_changed(text):
		if text != rejudge_problem_ui.select_text:
			rejudge_problem_ui.selected_client = str(text)
		
	def add_rejudge_problem_ui(self):
		label1 = QLabel('Problem Code:')
		code_entry = QComboBox()
		code_entry.addItem(rejudge_problem_ui.select_text)
		code_entry.addItem('All')
		for entry in rejudge_problem_ui.problem_codes:
			code_entry.addItem(entry)
		code_entry.activated[str].connect(rejudge_problem_ui.code_combo_box_data_changed)

		label2 = QLabel('Client:')
		client_entry = QComboBox()
		client_entry.addItem(rejudge_problem_ui.select_text)
		client_entry.addItem('All')
		rejudge_problem_ui.client_list.sort()
		for entry in rejudge_problem_ui.client_list:
			client_entry.addItem(entry)
		client_entry.activated[str].connect(rejudge_problem_ui.client_combo_box_data_changed)

		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(200, 50)
		confirm_button.clicked.connect(lambda:rejudge_problem_ui.final_account_status(self))
		confirm_button.setDefault(True)
		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(200, 50)
		cancel_button.clicked.connect(lambda:rejudge_problem_ui.cancel(self))
		cancel_button.setDefault(True)
		button_layout = QHBoxLayout()
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(label1)
		main_layout.addWidget(code_entry)
		main_layout.addWidget(label2)
		main_layout.addWidget(client_entry)
		main_layout.addWidget(button_widget)
		main = QWidget()
		main.setLayout(main_layout)

		label1.setObjectName('account_label')
		label2.setObjectName('account_label')
		confirm_button.setObjectName('interior_button')
		cancel_button.setObjectName('interior_button')
		main.setObjectName('account_window')
		code_entry.setObjectName('account_combobox')
		client_entry.setObjectName('account_combobox')
		return main
		
	def final_account_status(self):
		selected_code_ = rejudge_problem_ui.selected_code
		selected_client_ = rejudge_problem_ui.selected_client
		if selected_client_ == rejudge_problem_ui.select_text or selected_code_ == rejudge_problem_ui.select_text:
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Alert')
			info_box.setText('Select a valid option.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return

		print('[ REJUDGE ][ ' + selected_code_ + ' ][ ' + selected_client_ + ' ]')
		self.log('[ REJUDGE ][ ' + selected_code_ + ' ][ ' + selected_client_ + ' ]')

		if selected_code_ == 'All':
			selected_code_ = '*'

		if selected_client_ == 'All':
			selected_client_ = '*'
		else:
			# Get client id
			selected_client_ = str(client_authentication.get_client_id(selected_client_))

		data = submissions_management.get_submission_data(selected_code_, selected_client_)
		if data == 'NONE':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Alert')
			info_box.setText('Rejudge Failed.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			
		elif data == 'NF':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Alert')
			info_box.setText('There are no such submissions yet!')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
		else:
			for items in data:
				# Get source code from file
				try:
					file = open("Client_Submissions/" + items[4] ,"r")
					source_code = file.read()
					file.close()
				except:
					print('[ ERROR ] Source file could not be accessed!')
					info_box = QMessageBox()
					info_box.setIcon(QMessageBox.Critical)
					info_box.setWindowTitle('Alert')
					info_box.setText(items[4] + ': Source file could not be accessed!')
					info_box.setStandardButtons(QMessageBox.Ok)
					info_box.exec_()
					continue

				message = {
					'Code' : 'RJUDGE', 
					'Client ID' : items[0], 
					'Client Username' : selected_client_,
					'Run ID' : items[1],
					'Language' : items[2],
					'PCode' : items[3],
					'Source' : source_code,
					'Local Run ID' : items[5],
					'Time Stamp' : items[6]
				}
				message = json.dumps(message)
				rejudge_problem_ui.task_queue.put(message)
		self.close()

	def cancel(self):
		self.close()

