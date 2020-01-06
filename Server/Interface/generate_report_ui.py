from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from init_server import initialize_server, save_status
from database_management import problem_management
import json

class generate_report_ui(QMainWindow):
	def __init__(
			self,
			data_changed_flags, 
			task_queue,
			log_queue,
			parent=None
		):
		super(generate_report_ui, self).__init__(parent)
		
		self.data_changed_flags = data_changed_flags
		self.task_queue = task_queue
		self.log_queue = log_queue

		self.all_checked = True
		self.account_checked = False
		self.submission_checked = False
		self.client_checked = False
		self.judge_checked = False
		self.scoreboard_checked = False
		self.query_checked = False
		self.settings_checked = False
		self.stats_checked = False
		self.problems_checked = False
		
		self.setWindowTitle('Generate Report')
		self.width = 800
		self.height = 600
		self.setGeometry(500, 300, self.width, self.height)
		self.setFixedSize(self.width, self.height)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)

		self.progress = QProgressBar()
		self.progress.setGeometry(200, 80, 250, 10)

		heading = QLabel('Select Reports')
		heading.setObjectName('main_screen_heading')

		all_reports_checkbox = QCheckBox('All Reports')
		all_reports_checkbox.setObjectName('top_level_checkbox')
		all_reports_checkbox.stateChanged.connect(self.all_state_changed)
		all_reports_checkbox.setChecked(self.all_checked)

		account_report_checkbox = QCheckBox('Accounts Report')
		account_report_checkbox.setObjectName('sub_level_checkbox')
		account_report_checkbox.setChecked(self.account_checked)

		submission_report_checkbox = QCheckBox('Submissions Report')
		submission_report_checkbox.setObjectName('sub_level_checkbox')
		submission_report_checkbox.setChecked(self.submission_checked)

		client_report_checkbox = QCheckBox('Clients Report')
		client_report_checkbox.setObjectName('sub_level_checkbox')
		client_report_checkbox.setChecked(self.client_checked)

		judge_report_checkbox = QCheckBox('Judge Report')
		judge_report_checkbox.setObjectName('sub_level_checkbox')
		judge_report_checkbox.setChecked(self.judge_checked)

		scoreboard_report_checkbox = QCheckBox('Leaderboard Report')
		scoreboard_report_checkbox.setObjectName('sub_level_checkbox')
		scoreboard_report_checkbox.setChecked(self.scoreboard_checked)

		stats_report_checkbox = QCheckBox('Statistics Report')
		stats_report_checkbox.setObjectName('sub_level_checkbox')
		stats_report_checkbox.setChecked(self.stats_checked)

		query_report_checkbox = QCheckBox('Query Report')
		query_report_checkbox.setObjectName('sub_level_checkbox')
		query_report_checkbox.setChecked(self.query_checked)

		settings_report_checkbox = QCheckBox('Settings Report')
		settings_report_checkbox.setObjectName('sub_level_checkbox')
		settings_report_checkbox.setChecked(self.settings_checked)

		problems_report_checkbox = QCheckBox('Problems Report')
		problems_report_checkbox.setObjectName('sub_level_checkbox')		
		problems_report_checkbox.setChecked(self.problems_checked)

		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(150, 30)
		confirm_button.clicked.connect(lambda:generate_report_ui.final_status(self))
		confirm_button.setDefault(True)
		confirm_button.setObjectName('account_button')
		
		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(150, 30)
		cancel_button.clicked.connect(lambda:generate_report_ui.exit(self))
		cancel_button.setObjectName('account_button')
		cancel_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addStretch(20)
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(23)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)
		button_widget.setContentsMargins(0, 20, 0, 0)

		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addStretch(1)
		main_layout.addWidget(all_reports_checkbox)
		main_layout.addWidget(account_report_checkbox)
		main_layout.addWidget(submission_report_checkbox)
		main_layout.addWidget(client_report_checkbox)
		main_layout.addWidget(judge_report_checkbox)
		main_layout.addWidget(scoreboard_report_checkbox)
		main_layout.addWidget(stats_report_checkbox)
		main_layout.addWidget(query_report_checkbox)
		main_layout.addWidget(settings_report_checkbox)
		main_layout.addWidget(problems_report_checkbox)
		main_layout.addStretch(1)
		main_layout.addWidget(self.progress)
		main_layout.addStretch(1)
		main_layout.addWidget(button_widget)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName('account_window')
		self.setCentralWidget(main)

	def all_state_changed(self, state):
		if(state == Qt.Checked):
			print('set')
		return

	def log(self, text):
		self.log_queue.put(text)

	def final_status(self):
		# Ask for confirmation TODO
		try:
			self.completed = 0
			while self.completed < 100:
				self.completed += 0.00001
				self.progress.setValue(self.completed)
		except Exception as error:
			print('[ ERROR ] Could not generate reports: ' + str(error))
			self.log('[ ERROR ] Could not generate reports: ' + str(error))
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Alert')
			info_box.setText(
				'Error while generating reports.\n' +
				'Error Message: ' + str(error)
			)
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
		finally:
			self.close()

	def exit(self):
		self.close()