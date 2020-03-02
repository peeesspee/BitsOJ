from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import query_management
import json, time

class query_reply_ui(QMainWindow):
	button_mode = 1
	query = ''
	query_id = ''
	client_id = ''
	def __init__(
			self, 
			data_changed_flags,
			task_queue, 
			query, 
			reply,
			client_id, 
			query_id, 
			log_queue,
			parent=None
		):
		super(query_reply_ui, self).__init__(parent)
		query_reply_ui.button_mode = 1

		self.data_changed_flags = data_changed_flags
		self.task_queue = task_queue
		self.log_queue = log_queue
		query_reply_ui.query = query
		query_reply_ui.query_id = query_id
		query_reply_ui.client_id = client_id
		query_reply_ui.reply = reply

		self.setWindowTitle('Reply')
		self.setGeometry(600, 250, 600, 550)
		self.setFixedSize(600,550)
		main = self.main_query_reply_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_query_reply_ui(self):
		if query_reply_ui.query_id != -1:
			query_heading = QLabel('New Clarification')
			query_sub_heading = QLabel('Query:')
			response_sub_heading = QLabel('Response:')
			query_text = QTextEdit()
			query_text.setText(query_reply_ui.query)
			query_text.setReadOnly(True)
		else:
			query_heading = QLabel('New Announcement')
			query_sub_heading = QLabel('Announcement Heading:')
			response_sub_heading = QLabel('Announcement Content:')
			query_text = QTextEdit()
			query_reply_ui.query = 'Announcement'
			query_text.setText(query_reply_ui.query)
		
		response_entry = QTextEdit()
		response_entry.setText(query_reply_ui.reply)
		response_entry.setPlaceholderText('Max. 500 Characters')

		broadcast_setting_label = QLabel('Reply to: ')
		send_to_client_rbutton = QRadioButton('Client')
		send_to_all_rbutton = QRadioButton('All')
		send_to_client_rbutton.setChecked(True)
		send_to_all_rbutton.setChecked(False)
		send_to_client_rbutton.toggled.connect(
			lambda: query_reply_ui.send_mode_setter(self, send_to_client_rbutton)
		)
		send_to_all_rbutton.toggled.connect(
			lambda: query_reply_ui.send_mode_setter(self, send_to_all_rbutton)
		)
		radiobutton_layout = QHBoxLayout()
		radiobutton_layout.addWidget(broadcast_setting_label)
		radiobutton_layout.addStretch(10)
		radiobutton_layout.addWidget(send_to_client_rbutton)
		radiobutton_layout.addStretch(10)
		radiobutton_layout.addWidget(send_to_all_rbutton)
		radiobutton_layout.addStretch(80)
		# radiobutton_layout.setSpacing(50)
		radiobutton_widget = QWidget()
		radiobutton_widget.setLayout(radiobutton_layout)
		# radiobutton_widget.setContentsMargins(25,0,0,0)

		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(200, 50)
		confirm_button.clicked.connect(
			lambda:query_reply_ui.final_status(self, query_text.toPlainText(), response_entry.toPlainText())
		)
		confirm_button.setDefault(True)
		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(200, 50)
		cancel_button.clicked.connect(
			lambda:query_reply_ui.cancel(self)
		)
		cancel_button.setDefault(True)
		button_layout = QHBoxLayout()
		button_layout.addStretch(33)
		button_layout.addWidget(confirm_button)
		button_layout.addStretch(33)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(33)
		#button_layout.setSpacing(5)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(query_heading)
		main_layout.addWidget(query_sub_heading)
		main_layout.addWidget(query_text)
		main_layout.addWidget(response_sub_heading)
		main_layout.addWidget(response_entry)
		if query_reply_ui.client_id != -1:
			main_layout.addWidget(radiobutton_widget)
		main_layout.addWidget(button_widget)
		main = QWidget()
		main.setLayout(main_layout)

		confirm_button.setObjectName('interior_button')
		cancel_button.setObjectName('interior_button')
		query_heading.setObjectName('main_screen_heading')
		broadcast_setting_label.setObjectName('main_screen_content')
		main.setObjectName('account_window')
		query_sub_heading.setObjectName('main_screen_sub_heading')
		response_sub_heading.setObjectName('main_screen_sub_heading')
		send_to_all_rbutton.setObjectName('interior_rbutton')
		send_to_client_rbutton.setObjectName('interior_rbutton')
		return main

	def send_mode_setter(self, rbutton):
		if rbutton.text() == 'Client':
			if rbutton.isChecked() == True:
				query_reply_ui.button_mode = 1
		else:
			if rbutton.isChecked() == True:
				query_reply_ui.button_mode = 2
		return

	def log(self, text):
		self.log_queue.put(text)

	def final_status(self, query, response):
		if query_reply_ui.client_id != -1:
			if query_reply_ui.button_mode == 2:
				send_type = 'Broadcast'
			else:
				send_type = 'Client'
			message ={
				'Code' : 'QUERY',
				'Query' : query_reply_ui.query,
				'Response' : response,
				'Mode' : send_type,
				'Query ID' : query_reply_ui.query_id,
				'Client ID' : query_reply_ui.client_id
			}
			message = json.dumps(message)
			self.task_queue.put(message)
			query_management.update_query(query_reply_ui.query_id, query, response)
			print('[ QUERY ][ RSPONSE ][ ' + send_type + ' ] New query response sent by ADMIN')
			self.log('[ QUERY ][ RSPONSE ][ ' + send_type + ' ] New query response sent by ADMIN')
		else:
			message ={
				'Code' : 'QUERY',
				'Query' : query,
				'Response' : response,
				'Mode' : 'Broadcast',
				'Query ID' : query_reply_ui.query_id,
				'Client ID' : query_reply_ui.client_id
			}
			message = json.dumps(message)
			self.task_queue.put(message)
			query_management.update_query(query_reply_ui.query_id, query, response)
			print('[ ANNOUNCEMENT ] New Announcement sent by ADMIN')
			self.log('[ ANNOUNCEMENT ] New Announcement sent by ADMIN')

		self.data_changed_flags[8] = 0
		self.data_changed_flags[9] = 1
		self.data_changed_flags[23] -= 1
		self.close()

	def cancel(self):
		self.data_changed_flags[8] = 0
		self.close()


