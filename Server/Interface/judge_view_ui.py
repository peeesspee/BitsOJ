from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import submissions_management
import json, time
 

class judge_view_ui(QMainWindow):
	changed = 0
	state_type = ''
	def __init__(
			self, 
			data_changed_flags, 
			task_queue,
			log_queue,
			client_id, 
			username, 
			password, 
			state, 
			ip,
			parent=None
		):
		super(judge_view_ui, self).__init__(parent)
		
		self.data_changed_flags = data_changed_flags
		self.task_queue = task_queue
		self.log_queue = log_queue
		self.client_id = client_id
		self.username = username
		self.password = password
		self.state = state
		self.state_type = state
		self.ip = ip
		
		self.setWindowTitle('Manage Judge')
		self.setGeometry(750, 250, 550, 600)
		self.setFixedSize(550,600)
		main = self.main_self()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def log(self, text):
		self.log_queue.put(text)

	def main_self(self):
		data = submissions_management.get_judge_data(self.username)
		number_of_verdicts = data[0]
		last_verdict_time = data[1]

		heading = QLabel(' > ' + self.username)
		heading.setObjectName('main_screen_heading')

		password_label = QLabel('Password: ')
		password_content = QLabel(self.password)
		password_label.setObjectName('main_screen_sub_heading')
		password_content.setObjectName('main_screen_content')
		password_widget = self.get_horizontal_widget(password_label, password_content)

		ip_label = QLabel('Judge IP : ')
		ip_content = QLabel(self.ip)
		ip_label.setObjectName('main_screen_sub_heading')
		ip_content.setObjectName('main_screen_content')
		ip_widget = self.get_horizontal_widget(ip_label, ip_content)

		state_label = QLabel('Current State: ')
		state_content = QLabel(self.state)
		state_label.setObjectName('main_screen_sub_heading')
		state_content.setObjectName('main_screen_content')
		state_widget = self.get_horizontal_widget(state_label, state_content)

		state_entry_label = QLabel('Set State: ')
		state_entry_label.setObjectName('main_screen_sub_heading')

		state_entry = QComboBox()
		state_entry.addItem('<- SELECT ->')
		state_entry.addItem('Connected')
		state_entry.addItem('Disconnected')
		state_entry.addItem('Blocked')
		state_entry.setObjectName('account_combobox')
		state_entry.setFixedSize(200, 40)
		state_entry.activated[str].connect(self.combo_box_data_changed)

		state_entry_widget = self.get_horizontal_widget(state_entry_label, state_entry)
		
		verdict_label = QLabel('Verdict Count : ')
		verdict_label_data = QLabel(number_of_verdicts)
		verdict_label.setObjectName('main_screen_sub_heading')
		verdict_label_data.setObjectName('main_screen_content')
		verdict_widget = self.get_horizontal_widget(verdict_label, verdict_label_data)

		activity_label = QLabel('Latest Verdict : ')
		activity_label_data = QLabel(last_verdict_time + ' [ CONTEST TIME ]')
		activity_label.setObjectName('main_screen_sub_heading')
		activity_label_data.setObjectName('main_screen_content')
		activity_widget = self.get_horizontal_widget(activity_label, activity_label_data)

		inner_layout = QVBoxLayout()
		inner_layout.addWidget(password_widget)
		inner_layout.addWidget(ip_widget)
		inner_layout.addWidget(state_widget)
		inner_layout.addWidget(state_entry_widget)
		inner_layout.addWidget(activity_widget)
		inner_layout.addWidget(verdict_widget)
		inner_layout.setAlignment(heading, Qt.AlignCenter)
		
		inner_layout.addStretch(1)
		inner_widget = QWidget()
		inner_widget.setLayout(inner_layout)

		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(200, 50)
		confirm_button.clicked.connect(lambda:self.final_status())
		confirm_button.setDefault(True)
		confirm_button.setObjectName('interior_button')

		close_button = QPushButton('Close')
		close_button.setFixedSize(200, 50)
		close_button.clicked.connect(lambda:self.exit())
		close_button.setDefault(True)
		close_button.setObjectName('interior_button')

		button_widget = self.get_button_widget(confirm_button, close_button)
		
		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(inner_widget)
		main_layout.addStretch(2)
		main_layout.addWidget(button_widget)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName('account_window')
		return main

	def get_horizontal_widget(self, widget_1, widget_2):
		layout = QHBoxLayout()
		layout.addWidget(widget_1)
		layout.addWidget(widget_2)
		layout.addStretch(1)
		widget = QWidget()
		widget.setLayout(layout)
		return widget

	def get_button_widget(self, widget_1, widget_2):
		layout = QHBoxLayout()
		layout.addStretch(3)
		layout.addWidget(widget_1)
		layout.addStretch(1)
		layout.addWidget(widget_2)
		layout.addStretch(3)
		widget = QWidget()
		widget.setLayout(layout)
		return widget

	def combo_box_data_changed(self, text):
		if str(text) != '<- SELECT ->':
			self.changed = 1
			self.state_type = str(text)
		else:
			self.changed = 0

	def final_status(self):
		# If something is changed in combo box, run query 
		if self.changed == 1:
			message = {
				'Code' : 'UpJudgeStat', 
				'Username' : self.username,
				'State' : self.state_type,
				'IP' : self.ip
			}
			message = json.dumps(message)
			manage_judges.task_queue.put(message)

			print('[ JUDGE ][ ' + self.username + ' ][ UPDATE ] State changed to ' + self.state_type)
			self.log('[ JUDGE ][ ' + self.username + ' ][ UPDATE ] State changed to ' + self.state_type)

			if self.state_type == 'Blocked':
				message = {
					"Code" : "JBLOCK",
					"Receiver" : self.username
				}
				message = json.dumps(message)
				self.task_queue.put(message)

			elif self.state_type == 'Disconnected':
				message = {
					"Code" : "JDSCNT",
					"Judge" : self.username
				}
				message = json.dumps(message)
				self.task_queue.put(message)

			self.data_changed_flags[13] = 1
		self.close()

	def exit(self):
		self.data_changed_flags[14] = 0
		self.close()

