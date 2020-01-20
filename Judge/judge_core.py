# This process handles all the requests in the queue task_queue and updates database
import json, pika, sys, time
from database_management import manage_database, submission_management
   
class core():
	data_changed_flags = ''
	task_queue = ''
	channel = ''
	file_password = ''
	unicast_exchange = 'connection_manager'
	broadcast_exchange = 'broadcast_manager'
	judge_unicast_exchange = 'judge_manager'
	judge_broadcast_exchange = 'judge_broadcast_manager'
	
	def init_core(data_changed_flags, task_queue):
		core.data_changed_flags = data_changed_flags
		core.task_queue = task_queue
		conn, cur = manage_database.initialize_database()

		print('[ JUDGE ][ CORE PROCESS ] Process started')
		# Infinite Loop to Poll the task_queue every second
		try:
			while True:
				status = core.poll(task_queue)
				if status == 1:
					break
				# Poll every second
				time.sleep(2)
			# If we reach this point, it means the Server Shutdown has been initiated.
			print('[ CORE ] Shutdown')
			core.data_changed_flags[6] = 1
			
		except KeyboardInterrupt:
			core.data_changed_flags[6] = 1
			print('[ CORE ] Force Shutdown')

		finally:
			manage_database.close_db()
			sys.exit()
		
	def poll(task_queue):
		# If sys exit is called, the following flag will be 1
		if(core.data_changed_flags[5] == 1):
			return 1

		# While there is data to process in the task_queue,
		try:
			while task_queue.empty() == False:
				# Data in the task queue is in JSON format
				data = task_queue.get()
				data = json.loads(data)
				code = data['Code']
				# Contest START signal
				if code == 'JUDGE':
					run_id = data['Run ID']
					client_id = data['Client ID']
					verdict = data['Verdict']
					language = data['Language']
					problem_code = data['Problem Code']
					time_stamp = data['Timestamp']
					file_with_ext = data['Filename']

					count = submission_management.get_count(run_id)
					if count == 0:
						# New Submission
						print('[ CORE ] Insert Record: Run', run_id)
						status = submission_management.insert_record(
							run_id, 
							client_id, 
							verdict,	
							language, 
							problem_code, 
							time_stamp, 
							file_with_ext
						)
						if status == 0:
							print('[ CORE ] Submission Processed')
						else:
							print('[ CORE ] Submission Not Processed')
						core.data_changed_flags[4] = 1
					else:
						print('[ CORE ] Update Record: Run', run_id)
						submission_management.update_record(
							run_id, 
							client_id, 
							verdict,
							language, 
							problem_code, 
							time_stamp, 
							file_with_ext
						)
						print('[ CORE ] Update successful ')
						core.data_changed_flags[4] = 1

				elif code == 'UPDATE':
					run_id = data['Run ID']
					client_id = data['Client ID']
					verdict = data['Verdict']
					language = data['Language']
					problem_code = data['Problem Code']
					time_stamp = data['Timestamp']
					file_with_ext = data['Filename']

					print('[ CORE ] Update: ', run_id)
					submission_management.update_record(
						run_id, 
						client_id, 
						verdict,
						language, 
						problem_code, 
						time_stamp, 
						file_with_ext
					)
					print('[ CORE ] Update successful ')
					core.data_changed_flags[4] = 1

		except Exception as error:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[ CORE ][ ERROR ] Data Processing error : ' + str(error) + ' on line ' + str(exc_tb.tb_lineno)) 

		finally:
			return 0
