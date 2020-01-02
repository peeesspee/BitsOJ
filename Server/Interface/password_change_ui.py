from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import user_management
import json, time


class password_change_ui(QMainWindow):
	username = ''
	password = ''
	ctype = ''
	changed = 0
	def __init__(
			self, 
			data_changed_flags, 
			username, 
			password, 
			ctype, 
			parent=None
		):
		super(password_change_ui, self).__init__(parent)

		print(password_change_ui.username, password_change_ui.ctype, password_change_ui.password)
		
		self.data_changed_flags = data_changed_flags
		password_change_ui.username = str(username)
		password_change_ui.password = str(password)
		password_change_ui.ctype = str(ctype)
		
		self.setWindowTitle('Edit Account')
		self.setGeometry(750, 350, 500, 400)
		self.setFixedSize(500,400)
		try:
			main = self.main_password_change_ui()
		except Exception as error:
			print("[ ERROR ] " + str(error))
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_password_change_ui(self):
		heading = QLabel('Change Password')

		username_label = QLabel('Username: ')
		username_content = QLabel(password_change_ui.username)

		ctype_label = QLabel('Client Type: ')
		current_ctype = QLabel(password_change_ui.ctype)

		password_label = QLabel('Current Password: ')
		password_content = QLabel(password_change_ui.password)

		new_password_label = QLabel('New Password: ')
		new_password_content = QLineEdit()

		inner_layout = QVBoxLayout()
		inner_layout.addWidget(username_label)
		inner_layout.addWidget(username_content)
		inner_layout.addWidget(ctype_label)
		inner_layout.addWidget(current_ctype)
		inner_layout.addWidget(password_label)
		inner_layout.addWidget(password_content)
		inner_layout.addWidget(new_password_label)
		inner_layout.addWidget(new_password_content)
		inner_layout.addStretch(1)
		inner_widget = QWidget()
		inner_widget.setLayout(inner_layout)
				
		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(200, 50)
		confirm_button.clicked.connect(lambda:password_change_ui.final_status(self, new_password_content.text()))
		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(200, 50)
		cancel_button.clicked.connect(lambda:password_change_ui.exit(self))
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
		new_password_label.setObjectName('main_screen_sub_heading')
		new_password_content.setObjectName('main_screen_content')
		ctype_label.setObjectName('main_screen_sub_heading')
		current_ctype.setObjectName('main_screen_content')
		return main

	def final_status(self, new_password):
		if new_password != password_change_ui.password:
			user_management.update_user_password(password_change_ui.username, new_password)
			print('[ USER ][ ' + password_change_ui.username + ' ][ UPDATE ] Password changed to ' + new_password)
			self.data_changed_flags[1] = 1
			self.data_changed_flags[5] = 1
			self.data_changed_flags[14] = 0
			self.close()

	def exit(self):
		self.data_changed_flags[14] = 0
		self.close()

