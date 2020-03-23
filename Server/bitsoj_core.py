# This process handles all the requests in the queue task_queue and updates database
# It also sends data to clients/judges either in unicast or in broadcast.
import json, pika, sys, time
from init_server import initialize_server
from database_management import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
 

class core():
	data_changed_flags = ''
	task_queue = ''
	channel = ''
	file_password = ''
	unicast_exchange = 'connection_manager'
	broadcast_exchange = 'broadcast_manager'
	judge_unicast_exchange = 'judge_manager'
	judge_broadcast_exchange = 'judge_broadcast_manager'
	config = {}

	def init_core(data_changed_flags, task_queue, log_queue, update_queue, lock):
		core.data_changed_flags = data_changed_flags
		core.task_queue = task_queue
		core.log_queue = log_queue
		core.update_queue = update_queue
		core.lock = lock
		core.config = initialize_server.read_config()

		db_conn = manage_database.get_core_connection()
		
		print('  [ START ] Core subprocess started.')
		core.log('  [ START ] Core subprocess started.')

		superuser_username = core.config['Server Username']
		# superuser_username = 'BitsOJcore'
		superuser_password = core.config['Server Password']
		host = core.config['Server IP']
		core.file_password = core.config["File Password"]
	
		connection, channel = core.init_connection(superuser_username, superuser_password, host)
		core.channel = channel
		core.ranking_algoritm = core.data_changed_flags[17]
		# Infinite Loop to Poll the task_queue every second
		status = 0
		while True:
			try:
				status = core.poll(task_queue)
			except Exception as error:
				# Ignore the queue is Empty message
				if 'Empty' in str(error) or str(error) == '':
					pass
				else:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					print(
						'[ CORE ][ ERROR ] Data could not be transmitted : ' + str(error)
					) 
					core.log(
						'[ CORE ][ ERROR ] Data could not be transmitted : ' + str(error)
					)
			if status == 1:
				break
		
		# Shut down connection
		print("[ STOP ] Core subprocess terminated successfully!")
		core.log("[ STOP ] Core subprocess terminated successfully!")
		channel.stop_consuming()
		connection.close()
		core.data_changed_flags[8] = 1
		sys.exit(0)

	def log(message):
		core.log_queue.put(message)

	def init_connection(superuser_username, superuser_password, host):
		try:
			creds = pika.PlainCredentials(superuser_username, superuser_password)
			params = pika.ConnectionParameters(
					host = host, 
					credentials = creds, 
					heartbeat=0, 
					blocked_connection_timeout=0
				)
			connection = pika.BlockingConnection(params)
			channel = connection.channel()

			channel.exchange_declare(exchange = 'connection_manager', exchange_type = 'direct', durable = True)
			channel.exchange_declare(exchange = 'broadcast_manager', exchange_type = 'fanout', durable = True)
			channel.exchange_declare(
				exchange = 'judge_manager', 
				exchange_type = 'direct', 
				durable = True
			)
			channel.exchange_declare(
				exchange = 'judge_broadcast_manager', 
				exchange_type = 'fanout', 
				durable = True
			)
			return connection, channel
		
		except Exception as error:
			print('[ CRITICAL ] Core could not connect to RabbitMQ server : ' + str(error))
			core.log('[ CRITICAL ] Core could not connect to RabbitMQ server : ' + str(error))
			core.data_changed_flags[26] = 1
			while core.data_changed_flags[7] != 1:
				time.sleep(0.5)
			sys.exit()
		return 

	def poll(task_queue):
		# If sys exit is called, the following flag will be 1
		if(core.data_changed_flags[7] == 1):
			return 1

		# while task_queue.empty() == False:
			# Data in the task queue is in JSON format
		data = task_queue.get(block = True, timeout = 0.5)
		data = json.loads(data)
		code = data['Code']
		# Get a lock on DB
		core.lock.acquire()

		# Contest START signal
		if code == 'START':
			receiver = data['Receiver']
			if receiver == 'All':
				print('[ EVENT ][ BROADCAST ] START Contest')
				core.log('[ EVENT ][ BROADCAST ] START Contest')
				message = {
					'Code' : 'START',
					'Duration' : data['Duration'],
					'Start Time' : data['Start Time'],
					'End Time' : data['End Time'],
					'Problem Key' : core.file_password
				}
				message = json.dumps(message)
				core.channel.basic_publish(
					exchange = core.broadcast_exchange, 
					routing_key = '', 
					body = message
				)
			else:
				print('[ EVENT ][ ' + receiver + ' ] START Contest')
				core.log('[ EVENT ][ ' + receiver + ' ] START Contest')
				message = {
					'Code' : 'START',
					'Duration' : data['Duration'],
					'Start Time' : data['Start Time'],
					'End Time' : data['End Time'],
					'Problem Key' : core.file_password
				}
				message = json.dumps(message)
				core.channel.basic_publish(
					exchange = core.unicast_exchange, 
					routing_key = receiver, 
					body = message
				)

		
		# Contest STOP signal
		elif code == 'STOP':
			# Don't allow Submissions
			print('[ CORE ][ EVENT ][ BROADCAST ] STOP Contest')
			core.log('[ CORE ][ EVENT ][ BROADCAST ] STOP Contest')
			message = {
			'Code' : 'STOP'
			}
			message = json.dumps(message)
			core.channel.basic_publish(
				exchange = core.broadcast_exchange, 
				routing_key = '', 
				body = message
			)

		# Contest EXTeND signal
		elif code == 'EXTND':
			time1 = data['Time']
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.broadcast_exchange, 
				routing_key = '', 
				body = message
			)
			print('[ CORE ] Contest time extended by ' + str(time1) + ' minutes.')
			core.log('[ CORE ] Contest time extended by ' + str(time1) + ' minutes.')
			
		elif code == 'RESPONSE':
			receiver = data['Receiver']
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.unicast_exchange, 
				routing_key = receiver, 
				body = message
			)
			print('[ CORE ][ ' + receiver + ' ] Run ID sent.')
			core.log('[ CORE ][ ' + receiver + ' ] Run ID sent.')

		elif code == 'SHUTDOWN':
			receiver = data['Receiver']
			print('[ CORE ][ ' + receiver + ' ] Shutdown.')
			core.log('[ CORE ][ ' + receiver + ' ] Shutdown.')
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.unicast_exchange,
				routing_key = receiver, 
				body = message, 
				properties = pika.BasicProperties(delivery_mode = 2)
			) 

		elif code == "EDIT":
			print('[ CORE ] Problem Edit in progress...')
			core.log('[ CORE ] Problem Edit in progress...')
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.broadcast_exchange, 
				routing_key = 'judge_requests', 
				body = message, 
				properties = pika.BasicProperties(delivery_mode = 2)
			) 

		elif code == 'JUDGE':
			run_id = data['Run ID']
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.unicast_exchange,
				routing_key = 'judge_requests', 
				body = message, 
				properties = pika.BasicProperties(delivery_mode = 2)
			) 
			print('[ CORE ] Added a new submission request.')
			core.log('[ CORE ] Added a new submission request.')

		elif code == 'RJUDGE':
			run_id = data['Run ID']
			# Update submission status
			submissions_management.update_submission_status(run_id, 'REJUDGE', 'REJUDGE')
			# Refresh GUI
			

			data['Code'] = 'JUDGE'
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.unicast_exchange, 
				routing_key = 'judge_requests',  
				body = message, 
				properties = pika.BasicProperties(delivery_mode = 2)
			) 
			print('[ CORE ] Added a new Rejudge request for RunID: ' + str(run_id))
			core.log('[ CORE ] Added a new Rejudge request for RunID: ' + str(run_id))
		
		# UPDATE client timer to match server value
		elif code == 'UPDATE':
			# Don't allow Submissions
			print('[ CORE ][ EVENT ][ BROADCAST ] UPDATE Contest')
			core.log('[ CORE ][ EVENT ][ BROADCAST ] UPDATE Contest')
			message = {
			'Code' : 'UPDATE',
			'Time' : data['Time']
			}
			message = json.dumps(message)
			core.channel.basic_publish(
				exchange = core.broadcast_exchange, 
				routing_key = '', 
				body = message
			)

		# Contest SCoReBoarD
		elif code == 'SCRBD':
			print('[ CORE ][ SCOREBOARD ][ BROADCAST ]')
			core.log('[ CORE ][ SCOREBOARD ][ BROADCAST ]')
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.broadcast_exchange, 
				routing_key = '', 
				body = message
			)

# ----------------------------------------------------------------------------------------------------

		elif code == 'AddNewUser':
			username = data['Username']
			state = data['State' ]
			client_ip = data['IP']
			client_id = data['ID']
			password = data['Password' ]
			table = data['Table']
			client_authentication.add_client(
				client_id, 
				username, 
				password, 
				client_ip, 
				state, 
				table
			)
			core.update_queue.put(data)
			print('[ CORE ] Added new user.')
			core.log('[ CORE ] Added new user.')

		elif code == 'AddNUsers':
			print('[ CORE ] Generating accounts...')
			core.log('[ CORE ] Generating accounts...')

			client_no = data['Clients' ]
			judge_no = data['Judges' ]
			pwd_type = data['Password Type' ]
			
			status = user_management.generate_n_users(
				client_no, 
				judge_no, 
				pwd_type
			)

			if status == 1:
				print('[ CORE ] All accounts generated!')
				core.log('[ CORE ] All accounts generated!')
				# Get all accounts:
				account_data = interface_sync.get_account_table()

				# Update Interface
				core.update_queue.put({'Code' : 'RefreshUsers', 'Data' : account_data})
			else:
				print('[ CORE ] Account generation failed!')
				core.log('[ CORE ] Account generation failed!')
				core.update_queue.put(
					{
						'Code' : 'ERROR', 
						'Message' : 'Accounts could not be generated!'
					}
				)
			
		elif code == 'AddSheetUsers':
			print('[ CORE ] Adding sheet accounts...')
			core.log('[ CORE ] Adding sheet accounts...')
			
			u_list = data['UserList']
			p_list = data['PassList']
			t_list = data['TypeList']
			
			status = user_management.add_sheet_accounts(
				u_list, 
				p_list, 
				t_list
			)
			if status == 0:
				# Database insertion error
				print('[ CORE ][ ERROR ] Database insertion error: Team names should be unique.')
				core.log('[ CORE ][ ERROR ] Database insertion error: Team names should be unique.')
				core.update_queue.put(
					{
						'Code' : 'ERROR', 
						'Message' : 'Accounts could not be imported [ Username should be unique ]'
					}
				)
			else:
				print('[ CORE ] Sheet accounts added!')
				core.log('[ CORE ] Sheet accounts added!')
				core.update_queue.put({'Code' : 'RefreshUsers'})

		elif code == 'DelUsr':
			username = data['Client']
			user_management.delete_user(username)
			print('[ CORE ] User deleted: ', username)
			core.log('[ CORE ] User deleted: ' + username)
			core.update_queue.put(data)

		elif code == 'UpUserPwd':
			username = data['Username']
			password = data['New Password']
			ctype = data['Type']
			user_management.update_user_password(username, password, ctype)
			core.update_queue.put(data)
			print('[ CORE ] Updated user ' + username + '\'s Password to ' + password)
			core.log('[ CORE ] Updated user ' + username + '\'s Password to ' + password)
		
		elif code == 'AddNewSub':
			print('[ CORE ] Adding new submission')
			core.log('[ CORE ] Adding new submission')
			run_id = data['RunID']
			local_run_id = data['Local ID']
			client_id = data['Client ID']
			language = data['Language']
			source_file_name = data['Source File Name']
			problem_code = data['Problem Code']
			status = data['Status']
			time_stamp = data['Timestamp']
			status = submissions_management.insert_submission(
				run_id,
				local_run_id, 
				client_id, 
				language, 
				source_file_name, 
				problem_code, 
				status, 
				time_stamp
			) 
			if status == 1:
				print('[ CORE ] Submission inserted in database.')
			else:
				print('[ CORE ][ ERROR ] Submission NOT inserted in database.')
			# Update Interface to show new submission
			message = {
				'Code' : 'AddNewSub',
				'Run ID' : run_id, 
				'Client ID' : client_id,
				'Problem Code' : problem_code,
				'Language' : language,
				'Time' : time_stamp,
				'Verdict' : 'Running',
				'Status' : 'Waiting',
				'Judge' : 'Queued'
			}
			core.update_queue.put(message)
			# Inform admin of new submission
			core.data_changed_flags[0] = 1 

		elif code == 'VRDCT':
			username = data['Receiver']
			run_id = data['Run ID']
			status = data['Status']
			client_id = data['Client ID']
			p_code = data['Problem Code']
			time_stamp = data['Timestamp']
			try:
				judge = data['Judge']
			except:
				judge = 'SECURITY ERROR'
				
			# Update scoreboard
			problem_max_score = core.config['AC Points']
			penalty_score = core.config['Penalty Score']
			penalty_time = core.config['Penalty Time']
			
			# Update submission Database
			submissions_management.update_submission_status(run_id, status, 'Sent', judge)
			# Update interface
			message = {
				'Code' : 'UpSubStat',
				'Run ID' : run_id, 
				'Verdict' : status,
				'Status' : 'Sent',
				'Judge' : judge
			}
			core.update_queue.put(message)

			print('[ CORE ][ ' + username + ' ] Verdict sent to client.')
			core.log('[ CORE ][ ' + username + ' ] Verdict sent to client.')

			# Call scoreboard updation function
			scoreboard_management.update_user_score(
				client_id,
				run_id,
				problem_max_score,
				penalty_score,
				penalty_time,
				status, 
				p_code,
				time_stamp,
				core.ranking_algoritm
			) 
			# Interface scoreboard update 
			scbd_data = scoreboard_management.get_user_score(username)
			message = {
				'Code' : 'UpSCBD',
				'Data' : scbd_data[0] 
			}
			core.update_queue.put(message)

			# Send info to client
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.unicast_exchange, 
				routing_key = username, 
				body = message
			)
			# Send infor to judges
			core.channel.basic_publish(
				exchange = core.judge_broadcast_exchange,
				routing_key = '',
				body = message
			)         

			# Broadcast new scoreboard to clients whenever a new verdict is recieved 
			# and scoreboard update is allowed.
			if core.data_changed_flags[15] == 1:
				# Get user score and broadcast it to clients
				scbd_data = str(scbd_data)
				message = {
					'Code' : 'SCRBD',
					'Data' : scbd_data
				}
				message = json.dumps(message)
				core.channel.basic_publish(
					exchange = core.broadcast_exchange,
					routing_key = '',
					body = message
				)
				print('[ CORE ] Scoreboard Updated for clients')
				core.log('[ CORE ] Scoreboard Updated for clients')

		elif code == 'AddNewScore':	
			try:
				client_username = data['Username' ]
				client_id = data['ID']
				score = data['Score']
				problems_solved = data['Problems Solved']
				total_time = data['Total Time']
				scoreboard_management.insert_new_user(
					client_id, 
					client_username, 
					score, 
					problems_solved, 
					total_time
				)
				core.update_queue.put(data)
				print('[ CORE ] Added new user in scoreboard.')
				core.log('[ CORE ] Added new user in scoreboard.')
			except Exception as e:
				print('[ CORE ][ ERROR ] Scoreboard entry could not be added: ', e)
				core.log('[ CORE ][ ERROR ] Scoreboard entry could not be added: ' +  str(e))

		elif code == 'UpSubStat':
			# Update Submission status
			run_id = data['RunID']
			verdict = data['Verdict']
			sent_status = data['Sent Status']
			judge = data['Judge']
			submissions_management.update_submission_status(
					run_id, 
					verdict, 
					sent_status, 
					judge
			)
			# Send the updated infor to interface
			message = {
				'Code' : 'UpSubStat',
				'Run ID' : run_id, 
				'Verdict' : verdict,
				'Status' : sent_status,
				'Judge' : judge
			}
			core.update_queue.put(message)
			print('[ CORE ] Run ID ' + str(run_id) + ': Status changed.')
			core.log('[ CORE ] Run ID ' + str(run_id) + ': Status changed.')

		elif code == 'UpJudgeStat':
			username = data['Username']
			state = data['State']
			judge_ip = data['IP']
			user_management.update_judge_state(
				username, 
				state, 
				judge_ip
			)
			core.update_queue.put(data)
			print('[ CORE ] Judge ' + username + ': Status changed to ' + state)
			core.log('[ CORE ] Judge ' + username + ': Status changed to ' + state)

		elif code == 'JDSCNT':
			judge = data['Judge']
			core.update_queue.put(data)
			if judge == '__ALL__':
				print('[ CORE ][ EVENT ] Disconnect All Judges')
				core.log('[ CORE ][ EVENT ] Disconnect All Judges')
				message = {
					'Code' : 'DSCNT'
				}
				message = json.dumps(message)
				core.channel.basic_publish(
					exchange = core.judge_broadcast_exchange,
					routing_key = '', 
					body = message
				)
				core.update_queue.put({'Code' : 'JDscntAll'})
			else:
				print('[ CORE ][ EVENT ] Disconnect judge : ' + judge)
				core.log('[ CORE ][ EVENT ] Disconnect judge : ' + judge)
				message = {
					'Code' : 'DSCNT'
				}
				message = json.dumps(message)
				core.channel.basic_publish(
					exchange = core.judge_unicast_exchange, 
					routing_key = judge, 
					body = message
				)

		elif code == 'JBLOCK':
			username = data['Receiver']
			core.update_queue.put(data)
			print('[ CORE ][ EVENT ] Judge Block ' + username)
			core.log('[ CORE ][ EVENT ] Judge Block ' + username)
			message = {
				'Code' : 'BLOCK'
			}
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.judge_unicast_exchange, 
				routing_key = username, 
				body = message
			)


		elif code == 'UpUserStat':
			username = data['Username']
			state = data['State']
			judge_ip = data['IP']
			core.update_queue.put(data)
			user_management.update_user_state(
				username, 
				state, 
				judge_ip
			)
			print('[ CORE ] User ' + username + ': Status changed to ' + state)
			core.log('[ CORE ] User ' + username + ': Status changed to ' + state)

		# Client has been DiSCoNnecTed
		elif code == 'DSCNT':
			core.update_queue.put(data)
			if data['Mode'] == 1:
				client = data['Client']
				print('[ CORE ][ EVENT ] Disconnect client : ' + str(client))
				core.log('[ CORE ][ EVENT ] Disconnect client : ' + str(client))
				message = {
				'Code' : 'DSCNT',
				'Client' : client
				}
				message = json.dumps(message)
				# UNICAST THIS
				core.channel.basic_publish(
					exchange = core.unicast_exchange, 
					routing_key = client, 
					body = message
				)
			elif data['Mode'] == 2:
				print('[ CORE ][ EVENT ] Disconnect all clients')
				core.log('[ CORE ][ EVENT ] Disconnect all clients')
				message = {
				'Code' : 'DSCNT',
				'Client' : 'All'
				}
				message = json.dumps(message)
				core.channel.basic_publish(
					exchange = core.broadcast_exchange, 
					routing_key = '', 
					body = message
				)

		elif code == 'BLOCK':
			core.update_queue.put(data)
			username = data['Receiver']
			print('[ CORE ][ EVENT ] Block ' + username)
			core.log('[ CORE ][ EVENT ] Block ' + username)
		
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.unicast_exchange, 
				routing_key = username, 
				body = message
			)


		# QUERY reply to client or broadcast
		elif code == 'QUERY':
			query_id = data['Query ID']
			if data['Mode'] == 'Client':
				print('[ CORE ][ EVENT ][ UNICAST ] New Query response to client')
				core.log('[ CORE ][ EVENT ][ UNICAST ] New Query response to client')
				client_username = client_authentication.get_client_username(data['Client ID'])
				message = {
					'Code' : 'QUERY',
					'Client ID' : data['Client ID'],
					'Query' : data['Query'],
					'Response' : data['Response'],
					'Type' : data['Mode']
				}
				message = json.dumps(message)
				core.channel.basic_publish(
					exchange = core.unicast_exchange, 
					routing_key = client_username, 
					body = message
				)
			else:
				print('[ CORE ][ EVENT ][ BROADCAST ] New Query response broadcasted')
				core.log('[ CORE ][ EVENT ][ BROADCAST ] New Query response broadcasted')
				message = {
					'Code' : 'QUERY',
					'Client ID' : '0',
					'Query' : data['Query'],
					'Response' : data['Response'],
					'Type' : data['Mode']
				}
				message = json.dumps(message)
				core.channel.basic_publish(
					exchange = core.broadcast_exchange, 
					routing_key = '', 
					body = message
				)
			message = {
				'Code' : 'QUERY',
				'Query ID' : query_id,
				'Response' : data['Response']
			}
			core.update_queue.put(message)

		elif code == 'Announce':
			query_id = data['Query ID']
			print('[ CORE ][ EVENT ] Announcement broadcasted')
			core.log('[ CORE ][ EVENT ] Announcement broadcasted')
			message = {
				'Code' : 'QUERY',   # Yeah, client doesn't know that its announcement :P
				'Client ID' : '0',
				'Query' : data['Query'],
				'Response' : data['Response'],
				'Type' : data['Mode']
			}
			message = json.dumps(message)
			core.channel.basic_publish(
				exchange = core.broadcast_exchange, 
				routing_key = '', 
				body = message
			)

		elif code == 'AddQuery':
			query_id = data['Query ID']
			client_id = data['Client ID']
			query = data['Query']
			query_management.insert_query(
				query_id, 
				client_id, 
				query
			)
			# Update Interface
			core.data_changed_flags[1] = 1
			message = {
				'Code' : 'AddQuery',
				'Query ID' : query_id,
				'Client ID' : client_id,
				'Query' : query,
				'Response' : 'To be answered'
			}
			core.update_queue.put(message)
			
		
		elif code in ['VALID', 'INVLD', 'LRJCT', 'SRJCT']:
			# Pass the message to appropiate recipient, nothing to process in data
			receiver = data['Receiver']
			message = json.dumps(data)
			core.channel.basic_publish(
				exchange = core.unicast_exchange, 
				routing_key = receiver, 
				body = message
			)
		core.lock.release()
		return