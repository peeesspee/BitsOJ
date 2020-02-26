from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from init_server import initialize_server, save_status
from database_management import report_management
import json, datetime, sys, os, time

class generate_report_ui(QMainWindow):
	def __init__(
			self,
			data_changed_flags, 
			task_queue,
			log_queue,
			config,
			parent=None
		):
		super(generate_report_ui, self).__init__(parent)
		 
		self.data_changed_flags = data_changed_flags
		self.task_queue = task_queue
		self.log_queue = log_queue
		self.config = config

		self.all_checked = False
		self.account_checked = False
		self.submission_checked = False
		self.client_checked = False
		self.judge_checked = False
		self.scoreboard_checked = False
		self.query_checked = False
		self.problems_checked = False
		
		self.setWindowTitle('Generate Report')
		self.width = 800
		self.height = 600
		self.setGeometry(600, 300, self.width, self.height)
		self.setFixedSize(self.width, self.height)
		
		self.progress = QProgressBar()
		
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

		self.query_report_checkbox = QCheckBox('Query Report')
		self.query_report_checkbox.setObjectName('sub_level_checkbox')
		self.query_report_checkbox.setChecked(self.query_checked)
		self.query_report_checkbox.stateChanged.connect(self.query_state_changed)

		self.problems_report_checkbox = QCheckBox('Problems Report')
		self.problems_report_checkbox.setObjectName('sub_level_checkbox')		
		self.problems_report_checkbox.setChecked(self.problems_checked)
		self.problems_report_checkbox.stateChanged.connect(self.problems_state_changed)

		confirm_button = QPushButton('Generate')
		confirm_button.setFixedSize(150, 30)
		confirm_button.clicked.connect(lambda:generate_report_ui.final_status(self))
		confirm_button.setDefault(True)
		confirm_button.setObjectName('interior_button')
		
		button_widget = QWidget()
		button_layout = QHBoxLayout(button_widget)
		button_layout.addWidget(confirm_button)
		button_layout.setAlignment(Qt.AlignCenter)

		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addStretch(1)
		main_layout.addWidget(self.all_reports_checkbox)
		main_layout.addWidget(self.account_report_checkbox)
		main_layout.addWidget(self.submission_report_checkbox)
		main_layout.addWidget(self.client_report_checkbox)
		main_layout.addWidget(self.judge_report_checkbox)
		main_layout.addWidget(self.scoreboard_report_checkbox)
		main_layout.addWidget(self.query_report_checkbox)
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
			self.query_report_checkbox.setChecked(True)
			self.problems_report_checkbox.setChecked(True)
			self.all_checked = True
			self.account_checked = True
			self.submission_checked = True
			self.client_checked = True
			self.judge_checked = True
			self.scoreboard_checked = True
			self.query_checked = True
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

	def query_state_changed(self, state):
		if state == Qt.Checked:
			self.query_checked = True
		else:
			self.all_checked = False
			self.query_checked = False
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
			if self.account_checked == True:
				account_data = report_management.get_account_data()
				if account_data == 'NULL':
					print('[ REPORTS ][ ERROR ] No account report data found!')
				else:
					with open('./Reports/account_reports.txt', 'w+') as file:
						current_date_time = datetime.datetime.now()
						file.write(
							str(current_date_time) +
							'\n################ ' +
							'BitsOJ '+ 
							' ################' +
							'\nContest: ' + 
							self.config['Contest Name'] +
							' - ' +
							self.config['Contest Theme'] + 
							'\n'
						)
						file.write('Contest Teams:\n')
						file.write('\tTeam\t\t   Password\t\t Type\n')
						for accounts in account_data:
							username = accounts[0]
							password = accounts[1]
							account_type = accounts[2]
							file.write('\t' + username + '\t\t' + password + '\t\t' + account_type + '\n')
						file.write('\n################################################' )
			self.progress.setValue(10)
			time.sleep(0.2)

			if self.submission_checked == True:
				submission_data = report_management.get_all_submission_data()
				if submission_data == 'NULL':
					print('[ REPORTS ][ ERROR ] No submission report data found!')
				else:
					with open('./Reports/submission_reports.txt', 'w+') as file:
						current_date_time = datetime.datetime.now()
						file.write(
							str(current_date_time) +
							'\n################ ' +
							'BitsOJ '+ 
							' ################' +
							'\nContest: ' + 
							self.config['Contest Name'] +
							' - ' +
							self.config['Contest Theme'] + 
							'\n'
						)
						file.write('All Submissions:\n')
						file.write('\tRun ID\t\tClient ID\t\tProblem Code\t\tLanguage\t\tTimestamp\t\tVerdict\t\tJudge\n')
						for submissions in submission_data:
							run_id = submissions[0]
							client_id = submissions[1]
							problem_code = submissions[2]
							language = submissions[3]
							timestamp = submissions[4]
							verdict = submissions[5]
							judge = submissions[6]
														
							file.write(
								'\t' + 
								str(run_id) + 
								'\t\t\t\t' + 
								str(client_id) + 
								'\t\t\t\t' + 
								problem_code +
								'\t\t\t\t' + 
								language +
								'\t\t\t\t' + 
								timestamp +
								'\t\t\t' + 
								verdict +
								'\t\t' + 
								judge +
								'\n'
							)

						file.write(
							'\n################################################' +
							'####################################################' 
						)

						problem_codes = self.config['Problem Codes']
						file.write('\n\nSubmission data grouped by problems:\n')
						for problem in problem_codes:
							file.write('> Problem: ' + problem + '\n')
							file.write('\tRun ID\t\t\t Client ID \t\t\t Language \t\t\t Timestamp \t\t\t Verdict\n')
							grouped_data = report_management.get_grouped_problem_sub_data(problem)
							if grouped_data == 'NULL':
								print('[ REPORTS ][ ERROR ] No submission report data found!')
							elif len(grouped_data) == 0:
								file.write('\tNo Submissions for this problem.\n')
							else:
								for problem_data in grouped_data:
									run_id = problem_data[0]
									client_id = problem_data[1]
									language = problem_data[2]
									timestamp = problem_data[3]
									verdict = problem_data[4]
									file.write(
										'\t\t' + 
										str(run_id) + 
										'\t\t\t\t\t' + 
										str(client_id) +
										'\t\t\t\t' +
										language +
										'\t\t\t\t  ' +
										timestamp + 
										'\t\t\t  ' +
										verdict +
										'\n'
									)
						file.write(
							'\n################################################' +
							'####################################################' 
						)

			self.progress.setValue(30)
			time.sleep(0.4)

			if self.client_checked == True:
				client_data = report_management.get_all_client_data()
				if client_data == 'NULL':
					print('[ REPORTS ][ ERROR ] No client report data found!')
				else:
					with open('./Reports/client_reports.txt', 'w+') as file:
						current_date_time = datetime.datetime.now()
						file.write(
							str(current_date_time) +
							'\n################ ' +
							'BitsOJ '+ 
							' ################' +
							'\nContest: ' + 
							self.config['Contest Name'] +
							' - ' +
							self.config['Contest Theme'] + 
							'\n'
						)
						file.write('All Clients:\n')
						file.write('\tClient ID\t\tTeam Name\t\t  IP Address\n')
						for clients in client_data:
							client_id = clients[0]
							team_name = clients[1]
							ip_address = clients[2]
							
														
							file.write(
								'\t' + 
								str(client_id) + 
								'\t\t\t\t' + 
								team_name +
								'\t\t  ' + 
								ip_address +
								'\n'
							)

						file.write(
							'\n################################################' +
							'####################################################' 
						)
						
						file.write('\n\nSubmission data grouped by clients:\n')
						for client in client_data:
							file.write('> Client: ' + str(client[1]) + '\n')
							file.write('\tRun ID\t\t\t Problem Code \t\t\t Language \t\t\t Timestamp \t\t\t Verdict\n')
							grouped_data = report_management.get_grouped_client_sub_data(client[0])
							if grouped_data == 'NULL':
								print('[ REPORTS ][ ERROR ] No client report data found for client: ', client[1])
							elif len(grouped_data) == 0:
								file.write('\tNo Submissions by this client.\n')
							else:
								for problem_data in grouped_data:
									run_id = problem_data[0]
									problem_code = problem_data[1]
									language = problem_data[2]
									timestamp = problem_data[3]
									verdict = problem_data[4]
									file.write(
										'\t\t' + 
										str(run_id) + 
										'\t\t\t\t  ' + 
										problem_code +
										'\t\t\t\t\t' +
										language +
										'\t\t\t\t  ' +
										timestamp + 
										'\t\t\t\t' +
										verdict +
										'\n'
									)
						file.write(
							'\n################################################' +
							'####################################################' 
						)
			self.progress.setValue(50)
			time.sleep(0.6)

			if self.judge_checked == True:
				judge_data = report_management.get_all_judge_data()
				judge_data.append(('__ADMIN__', 'ADMIN', 'localhost'))
				with open('./Reports/judge_reports.txt', 'w+') as file:
					current_date_time = datetime.datetime.now()
					file.write(
						str(current_date_time) +
						'\n################ ' +
						'BitsOJ '+ 
						' ################' +
						'\nContest: ' + 
						self.config['Contest Name'] +
						' - ' +
						self.config['Contest Theme'] + 
						'\n\n'
					)
					file.write('All Judges:\n')
					file.write('\tJudge ID\t\tTeam Name\t\t  IP Address\n')
					for judge in judge_data:
						judge_id = judge[0]
						judge_name = judge[1]
						ip_address = judge[2]
											
						file.write(
							'\t' + 
							judge_id + 
							'\t\t' + 
							judge_name +
							'\t\t  ' + 
							ip_address +
							'\n'
						)

					file.write(
						'\n################################################' +
						'####################################################' 
					)
					
					file.write('\n\nSubmission data grouped by judgess:\n')
					
					for judge in judge_data:
						judgement_count = report_management.get_judgement_count(judge[1])
						file.write('\n> Judge: ' + judge[1] + ' :::: Number of verdicts: ' + str(judgement_count) + '\n')

						file.write('\tRun ID\t\t\tClient ID \t\t\t Problem Code \t\t Language \t\t\t Timestamp \t\t\t Verdict\n')
						grouped_data = report_management.get_grouped_judge_sub_data(judge[1])
						if grouped_data == 'NULL':
							print('[ REPORTS ][ ERROR ] No judge report data found for judge: ', judge[1])
						elif len(grouped_data) == 0:
							file.write('\tNo Verdicts by this judge.\n')
						else:
							for problem_data in grouped_data:
								run_id = problem_data[0]
								client_id = problem_data[1]
								problem_code = problem_data[2]
								language = problem_data[3]
								timestamp = problem_data[4]
								verdict = problem_data[5]
								file.write(
									'\t\t' + 
									str(run_id) + 
									'\t\t\t\t  ' +
									str(client_id) +
									'\t\t\t\t  ' + 
									problem_code +
									'\t\t\t\t\t' +
									language +
									'\t\t\t\t  ' +
									timestamp + 
									'\t\t\t\t' +
									verdict +
									'\n'
								)
					file.write(
						'\n################################################' +
						'####################################################' 
					)

			self.progress.setValue(70)
			time.sleep(0.1)

			if self.scoreboard_checked == True:
				winner = report_management.get_winner()
				if winner == "NULL" or len(winner) == 0:
					print('[ REPORTS ][ ERROR ] No winner report data found!')
				else:
					winner_score = winner[0]
					winner_name = winner[1]

					with open('./Reports/scoreboard_reports.txt', 'w+') as file:
						current_date_time = datetime.datetime.now()
						file.write(
							str(current_date_time) +
							'\n################ ' +
							'BitsOJ '+ 
							' ################' +
							'\nContest: ' + 
							self.config['Contest Name'] +
							' - ' +
							self.config['Contest Theme'] + 
							'\n'
						)
						file.write('Contest Winner:\n')
						file.write('\tTeam: ' + winner_name + '\n\tScore: ' + str(winner_score))
						file.write(
								'\n################################################' +
								'####################################################' 
						)

						data = report_management.get_scoreboard_data()
						if len(data) != 0 and data != "NULL":
							file.write('\nComplete Scoreboard: \n')
							file.write(
								"\t\tTeam 	\t\t\t\t Score 	\tProblems Solved\t\t\t   Total Time\n"
							)
							for scoreboard_entry in data:
								team = scoreboard_entry[0]
								score = scoreboard_entry[1]
								problems_solved = scoreboard_entry[2]
								total_time = scoreboard_entry[3]

								file.write(
									'\t\t' + 
									team + 
									'\t\t\t\t  ' +
									str(score) +
									' \t\t\t\t ' + 
									str(problems_solved) +
									'\t\t\t\t\t' +
									total_time +
									'\n'
								)
							file.write(
								'\n################################################' +
								'####################################################' 
							)
			self.progress.setValue(80)
			time.sleep(0.6)

			if self.problems_checked == True:
				problem_data = report_management.get_problem_data()
				if problem_data == 'NULL':
					print('[ REPORTS ][ ERROR ] No problem report data found!')
				else:
					with open('./Reports/problem_reports.txt', 'w+') as file:
						current_date_time = datetime.datetime.now()
						file.write(
							str(current_date_time) +
							'\n################ ' +
							'BitsOJ '+ 
							' ################' +
							'\nContest: ' + 
							self.config['Contest Name'] +
							' - ' +
							self.config['Contest Theme'] + 
							'\n'
						)
						participant_count = report_management.get_participant_count()
						pro_count = report_management.get_participant_pro_count()
						file.write('Number of participants with at least one submission: ' + str(participant_count) + '\n')
						file.write('Number of participants with at least one AC submission: ' + str(pro_count) + '\n')

						file.write('Contest Problem Details:\n')
						for problem in problem_data:
							name = problem[0]
							code = problem[1]
							test_files = problem[2]
							time_limit = problem[3]

							ac_count = report_management.get_ac_count(code)
							sub_count = report_management.get_submission_count(code)

							file.write(' > ' + name + '[ ' + code + ' ]\n')
							file.write('\t Time Limit : ' + str(time_limit) + ' Seconds\n')
							file.write('\t Number of Test files: ' + str(test_files) + '\n')
							file.write('\t Total Submissions on this problem: ' + str(sub_count) + '\n')
							file.write('\t AC Submissions on this problem: ' + str(ac_count) + '\n')
						file.write('\n################################################' )
			self.progress.setValue(90)
			time.sleep(0.4)

			if self.query_checked == True:
				query_data = report_management.get_query_data()
				if query_data == 'NULL':
					print('[ REPORTS ][ ERROR ] No query report data found!')
				else:
					with open('./Reports/query_reports.txt', 'w+') as file:
						current_date_time = datetime.datetime.now()
						file.write(
							str(current_date_time) +
							'\n################ ' +
							'BitsOJ '+ 
							' ################' +
							'\nContest: ' + 
							self.config['Contest Name'] +
							' - ' +
							self.config['Contest Theme'] + 
							'\n'
						)
						file.write('Queries and Announcements:\n')
						file.write('\tClientID\t\t\t\t\tQuery\t\t\t\t\tResponse\n')
						for query in query_data:
							client_id = query[0]
							query_text = query[1]
							response = query[2]
							file.write('\t' + str(client_id) + '\t\t' + query_text + '\t\t' + response + '\n')
						file.write('\n################################################' )

			self.progress.setValue(100)
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Done!')
			info_box.setText(
				'Reports generated in ./Reports/'
			)
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			
		except Exception as error:
			print('[ ERROR ] Could not generate reports: ' + str(error))
			self.log('[ ERROR ] Could not generate reports: ' + str(error))

			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Alert')
			info_box.setText(
				'Error while generating reports.\n' +
				'Error Message: ' + str(error) +
				' Details\nFile: ' + fname +
				'Line No.: ' + str(exc_tb.tb_lineno)
			)
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
		finally:
			self.close()

	def exit(self):
		self.close()