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

		self.all_checked = False
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

		self.all_reports_checkbox = QCheckBox('All Reports')
		self.all_reports_checkbox.setObjectName('top_level_checkbox')
		self.all_reports_checkbox.stateChanged.connect(self.all_state_changed)
		self.all_reports_checkbox.setChecked(self.all_checked)

		self.account_report_checkbox = QCheckBox('Accounts Report')
		self.account_report_checkbox.setObjectName('sub_level_checkbox')
		self.account_report_checkbox.setChecked(self.account_checked)
		self.account_report_checkbox.stateChanged.connect(self.account_state_changed)

		self.submission_report_checkbox = QCheckBox('Submissions Report')
		self.submission_report_checkbox.setObjectName('sub_level_checkbox')
		self.submission_report_checkbox.setChecked(self.submission_checked)
		self.submission_report_checkbox.stateChanged.connect(self.submission_state_changed)

		self.client_report_checkbox = QCheckBox('Clients Report')
		self.client_report_checkbox.setObjectName('sub_level_checkbox')
		self.client_report_checkbox.setChecked(self.client_checked)
		self.client_report_checkbox.stateChanged.connect(self.client_state_changed)

		self.judge_report_checkbox = QCheckBox('Judge Report')
		self.judge_report_checkbox.setObjectName('sub_level_checkbox')
		self.judge_report_checkbox.setChecked(self.judge_checked)
		self.judge_report_checkbox.stateChanged.connect(self.judge_state_changed)

		self.scoreboard_report_checkbox = QCheckBox('Leaderboard Report')
		self.scoreboard_report_checkbox.setObjectName('sub_level_checkbox')
		self.scoreboard_report_checkbox.setChecked(self.scoreboard_checked)
		self.scoreboard_report_checkbox.stateChanged.connect(self.scoreboard_state_changed)

		self.stats_report_checkbox = QCheckBox('Statistics Report')
		self.stats_report_checkbox.setObjectName('sub_level_checkbox')
		self.stats_report_checkbox.setChecked(self.stats_checked)
		self.stats_report_checkbox.stateChanged.connect(self.stats_state_changed)

		self.query_report_checkbox = QCheckBox('Query Report')
		self.query_report_checkbox.setObjectName('sub_level_checkbox')
		self.query_report_checkbox.setChecked(self.query_checked)
		self.query_report_checkbox.stateChanged.connect(self.query_state_changed)

		self.settings_report_checkbox = QCheckBox('Settings Report')
		self.settings_report_checkbox.setObjectName('sub_level_checkbox')
		self.settings_report_checkbox.setChecked(self.settings_checked)
		self.settings_report_checkbox.stateChanged.connect(self.settings_state_changed)

		self.problems_report_checkbox = QCheckBox('Problems Report')
		self.problems_report_checkbox.setObjectName('sub_level_checkbox')		
		self.problems_report_checkbox.setChecked(self.problems_checked)
		self.problems_report_checkbox.stateChanged.connect(self.problems_state_changed)

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
		main_layout.addWidget(self.all_reports_checkbox)
		main_layout.addWidget(self.account_report_checkbox)
		main_layout.addWidget(self.submission_report_checkbox)
		main_layout.addWidget(self.client_report_checkbox)
		main_layout.addWidget(self.judge_report_checkbox)
		main_layout.addWidget(self.scoreboard_report_checkbox)
		main_layout.addWidget(self.stats_report_checkbox)
		main_layout.addWidget(self.query_report_checkbox)
		main_layout.addWidget(self.settings_report_checkbox)
		main_layout.addWidget(self.problems_report_checkbox)
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
			self.account_report_checkbox.setChecked(True)
			self.submission_report_checkbox.setChecked(True)
			self.client_report_checkbox.setChecked(True)
			self.judge_report_checkbox.setChecked(True)
			self.scoreboard_report_checkbox.setChecked(True)
			self.stats_report_checkbox.setChecked(True)
			self.query_report_checkbox.setChecked(True)
			self.settings_report_checkbox.setChecked(True)	
			self.problems_report_checkbox.setChecked(True)
			self.all_checked = True
			self.account_checked = True
			self.submission_checked = True
			self.client_checked = True
			self.judge_checked = True
			self.scoreboard_checked = True
			self.query_checked = True
			self.settings_checked = True
			self.stats_checked = True
			self.problems_checked = True
		return

	def account_state_changed(self, state):
		if state == Qt.Checked:
			self.account_checked = True
		else:
			self.all_checked = False
			self.account_checked = False
			self.all_reports_checkbox.setChecked(False)

	def submission_state_changed(self, state):
		if state == Qt.Checked:
			self.submission_checked = True
		else:
			self.all_checked = False
			self.submission_checked = False
			self.all_reports_checkbox.setChecked(False)

	def client_state_changed(self, state):
		if state == Qt.Checked:
			self.client_checked = True
		else:
			self.all_checked = False
			self.client_checked = False
			self.all_reports_checkbox.setChecked(False)

	def judge_state_changed(self, state):
		if state == Qt.Checked:
			self.judge_checked = True
		else:
			self.all_checked = False
			self.judge_checked = False
			self.all_reports_checkbox.setChecked(False)

	def scoreboard_state_changed(self, state):
		if state == Qt.Checked:
			self.scoreboard_checked = True
		else:
			self.all_checked = False
			self.scoreboard_checked = False
			self.all_reports_checkbox.setChecked(False)

	def stats_state_changed(self, state):
		if state == Qt.Checked:
			self.stats_checked = True
		else:
			self.all_checked = False
			self.stats_checked = False
			self.all_reports_checkbox.setChecked(False)

	def query_state_changed(self, state):
		if state == Qt.Checked:
			self.query_checked = True
		else:
			self.all_checked = False
			self.query_checked = False
			self.all_reports_checkbox.setChecked(False)

	def settings_state_changed(self, state):
		if state == Qt.Checked:
			self.settings_checked = True
		else:
			self.all_checked = False
			self.settings_checked = False
			self.all_reports_checkbox.setChecked(False)

	def problems_state_changed(self, state):
		if state == Qt.Checked:
			self.problems_checked = True
		else:
			self.all_checked = False
			self.problems_checked = False
			self.all_reports_checkbox.setChecked(False)


	def log(self, text):
		self.log_queue.put(text)

	def final_status(self):
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