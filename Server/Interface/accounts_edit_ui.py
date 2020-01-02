from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import user_management
import json, time


class account_edit_ui(QMainWindow):
	client_id = ''
	username = ''
	password = ''
	state = ''
	state_type = ''
	ip = ''
	changed = 0
	def __init__(
			self, 
			data_changed_flags, 
			task_queue,
			client_id, 
			username, 
			password, 
			state, 
			ip,
			parent=None
		):
		super(account_edit_ui, self).__init__(parent)
		
		self.data_changed_flags = data_changed_flags
		self.task_queue = task_queue
		account_edit_ui.client_id = client_id
		account_edit_ui.username = username
		account_edit_ui.password = password
		account_edit_ui.state = state
		account_edit_ui.state_type = state
		account_edit_ui.ip = ip
		
		self.setWindowTitle('Manage Client')
		self.setGeometry(750, 350, 500, 400)
		self.setFixedSize(500,400)
		main = self.main_account_edit_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_account_edit_ui(self):
		heading = QLabel('Edit user status')

		username_label = QLabel('Username: ')
		username_content = QLabel(account_edit_ui.username)

		password_label = QLabel('Password: ')
		password_content = QLabel(account_edit_ui.password)

		ip_label = QLabel('IP: ')
		ip_content = QLabel(account_edit_ui.ip)

		state_label = QLabel('Current State: ')
		current_state = QLabel(account_edit_ui.state)

		state_entry_label = QLabel('Set State: ')
		state_entry = QComboBox()
		state_entry.addItem('<- SELECT ->')
		state_entry.addItem('Connected')
		state_entry.addItem('Disconnected')
		state_entry.addItem('Blocked')
		state_entry.activated[str].connect(account_edit_ui.combo_box_data_changed)
		
		inner_layout = QGridLayout()
		inner_layout.addWidget(username_label, 0, 0)
		inner_layout.addWidget( username_content, 0, 1)
		inner_layout.addWidget(password_label, 1, 0)
		inner_layout.addWidget(password_content, 1, 1)
		inner_layout.addWidget(ip_label, 2, 0)
		inner_layout.addWidget(ip_content, 2, 1)
		inner_layout.addWidget(state_label, 3, 0)
		inner_layout.addWidget(current_state, 3, 1)
		inner_layout.addWidget(state_entry_label, 4, 0)
		inner_layout.addWidget(state_entry, 4, 1)

		inner_layout.setColumnMinimumWidth(0,50)
		inner_layout.setColumnMinimumWidth(1,50)
		inner_layout.setColumnStretch(0, 1)
		inner_layout.setColumnStretch(1, 1)
		inner_layout.setRowStretch(0, 1)
		inner_layout.setRowStretch(1, 1)
		inner_layout.setVerticalSpacing(10)
		
		# inner_layout.addStretch(1)
		inner_widget = QWidget()
		inner_widget.setLayout(inner_layout)
				
		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(200, 50)
		confirm_button.clicked.connect(lambda:account_edit_ui.final_status(self))
		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(200, 50)
		cancel_button.clicked.connect(lambda:account_edit_ui.exit(self))
		cancel_button.setDefault(True)
		button_layout = QHBoxLayout()
		button_layout.addStretch(33)
		button_layout.addWidget(confirm_button)
		button_layout.addStretch(33)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(33)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)
		button_widget.setContentsMargins(0, 20, 0, 0)

		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(inner_widget)
		main_layout.addWidget(button_widget)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)

		main.setObjectName('account_window')
		heading.setObjectName('main_screen_heading')
		confirm_button.setObjectName('interior_button')
		cancel_button.setObjectName('interior_button')
		username_label.setObjectName('main_screen_sub_heading')
		username_content.setObjectName('main_screen_content')
		password_label.setObjectName('main_screen_sub_heading')
		password_content.setObjectName('main_screen_content')
		ip_label.setObjectName('main_screen_sub_heading')
		ip_content.setObjectName('main_screen_content')
		state_label.setObjectName('main_screen_sub_heading')
		current_state.setObjectName('main_screen_content')
		state_entry_label.setObjectName('main_screen_sub_heading')
		state_entry.setObjectName('account_combobox')
		return main

	def combo_box_data_changed(text):
		if str(text) != '<- SELECT ->':
			account_edit_ui.changed = 1
			account_edit_ui.state_type = str(text)
		else:
			account_edit_ui.changed = 0

	def final_status(self):
		# If something is changed in combo box, run query 
		if account_edit_ui.changed == 1:
			user_management.update_user_state(account_edit_ui.username, account_edit_ui.state_type)
			print('[ USER ][ ' + account_edit_ui.username + ' ][ UPDATE ] State changed to ' + account_edit_ui.state_type)
			message = {
				"Code" : "BLOCK",
				"Receiver" : account_edit_ui.username
			}
			message = json.dumps(message)
			self.task_queue.put(message)
			self.data_changed_flags[1] = 1
		self.data_changed_flags[14] = 0
		self.close()

	def exit(self):
		self.data_changed_flags[14] = 0
		self.close()

