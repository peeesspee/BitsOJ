from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import user_management
import json, time

class new_accounts_ui(QMainWindow):
	pwd_type = 'Simple'
	client_no = 0
	judge_no = 0
	data_changed_flags = ''
	
	def __init__(self, data_changed_flags, parent=None):
		super(new_accounts_ui, self).__init__(parent)
		new_accounts_ui.data_changed_flags = data_changed_flags
		self.setGeometry(800, 450, 300, 200)
		self.setWindowTitle('Add new accounts')
		self.setFixedSize(300, 200)
		main = self.add_new_accounts_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def combo_box_data_changed(text):
		new_accounts_ui.pwd_type = str(text)

	def client_updater(text):
		new_accounts_ui.client_no = int(text)
		return
	def judge_updater(text):
		new_accounts_ui.judge_no = int(text)
		return

	def add_new_accounts_ui(self):
		new_accounts_ui.client_no = 0
		new_accounts_ui.judge_no = 0
		
		label1 = QLabel('Clients')

		client_entry = QSpinBox()
		client_entry.setMinimum(0)
		client_entry.setMaximum(500)
		client_entry.valueChanged.connect(new_accounts_ui.client_updater)
		
		label2 = QLabel('Judges')

		judge_entry = QSpinBox()
		judge_entry.setMinimum(0)
		judge_entry.setMaximum(10)
		judge_entry.valueChanged.connect(new_accounts_ui.judge_updater)
	
		label3 = QLabel('Password Type:')

		password_type_entry = QComboBox()
		#If you change these labels, also change lines 309, 311 in database_management.py
		password_type_entry.addItem('Simple')
		password_type_entry.addItem('Random')
		password_type_entry.activated[str].connect(new_accounts_ui.combo_box_data_changed)

		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(200, 50)
		confirm_button.clicked.connect(lambda:new_accounts_ui.final_account_status(self))
		
		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(200, 50)
		cancel_button.clicked.connect(lambda:new_accounts_ui.cancel(self))
		cancel_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)

		layout = QGridLayout()
		layout.addWidget(label1, 0, 0)
		layout.addWidget(client_entry, 0, 1)
		layout.addWidget(label2, 1, 0)
		layout.addWidget(judge_entry, 1, 1)
		layout.addWidget(label3, 2, 0)
		layout.addWidget(password_type_entry, 2, 1)

		layout.setColumnMinimumWidth(0,50)
		layout.setColumnMinimumWidth(1,50)
		layout.setColumnStretch(0, 1)
		layout.setColumnStretch(1, 1)
		layout.setRowStretch(0, 1)
		layout.setRowStretch(1, 1)
		layout.setVerticalSpacing(10)
		upper_widget = QWidget()
		upper_widget.setLayout(layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(upper_widget)
		main_layout.addWidget(button_widget)
		
		main = QWidget()
		main.setLayout(main_layout)

		label1.setObjectName('account_label')
		label2.setObjectName('account_label')
		label3.setObjectName('account_label')
		client_entry.setObjectName('account_spinbox')
		judge_entry.setObjectName('account_spinbox')
		password_type_entry.setObjectName('account_combobox')
		confirm_button.setObjectName('interior_button')
		cancel_button.setObjectName('interior_button')
		main.setObjectName('account_window')
		return main
		
	def final_account_status(self):
		print('[ ACCOUNT ] Create ' + str(new_accounts_ui.client_no) + ' Clients and ' + str(new_accounts_ui.judge_no) + ' Judge Accounts')
		user_management.generate_n_users(
			new_accounts_ui.client_no, new_accounts_ui.judge_no, 
			new_accounts_ui.pwd_type
		)
		# Reset the critical section flag
		new_accounts_ui.data_changed_flags[4] = 0
		# Indicate new insertions in accounts
		new_accounts_ui.data_changed_flags[5] = 1
		self.close()

	def cancel(self):
		# Reset the critical section flag
		new_accounts_ui.data_changed_flags[4] = 0
		self.close()

