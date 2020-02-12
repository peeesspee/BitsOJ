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
	config = ''

	def init_core(data_changed_flags, task_queue, log_queue):
		core.data_changed_flags = data_changed_flags
		core.task_queue = task_queue
		core.log_queue = log_queue
		core.config = initialize_server.read_config()
		
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
		while True:
			status = core.poll(task_queue)
			if status == 1:
				break
			# Poll every second
			# time.sleep(1)

		# If we reach this point, it means the Server Shutdown has been initiated.
		
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
			params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
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

		# While there is data to process in the task_queue,
		try:
			while task_queue.empty() == False:
				size = task_queue.qsize()
				print('[ CORE ] ', size , ' operations in line.')
				# Data in the task queue is in JSON format
				data = task_queue.get()
				data = json.loads(data)
				code = data['Code']
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
					time = data['Time']
					print('[ CORE ] Contest time extended by ' + str(time) + ' minutes.')
					core.log('[ CORE ] Contest time extended by ' + str(time) + ' minutes.')
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.broadcast_exchange, 
						routing_key = '', 
						body = message
					)
					
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
						
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.unicast_exchange, 
						routing_key = username, 
						body = message
					)
					
					core.channel.basic_publish(
						exchange = core.judge_broadcast_exchange,
						routing_key = '',
						body = message
					)
					
					# Update scoreboard
					problem_max_score = core.config['AC Points']
					penalty_score = core.config['Penalty Score']
					penalty_time = core.config['Penalty Time']
					
					# Update submission Database
					submissions_management.update_submission_status(run_id, status, 'SENT', judge)
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

					# Update Submissions GUI
					core.data_changed_flags[0] = 1
					# Update scoreboard view in server
					core.data_changed_flags[16] = 1
					# Broadcast new scoreboard to clients whenever a new AC is recieved 
					# and scoreboard update is allowed.
					if core.data_changed_flags[15] == 1:
						# Get user score and broadcast it to clients
						data = scoreboard_management.get_user_score(username)
						data = str(data)
					
						message = {
							'Code' : 'SCRBD',
							'Data' : data
						}
						message = json.dumps(message)
						core.channel.basic_publish(
							exchange = core.broadcast_exchange,
							routing_key = '',
							body = message
						)
						print('[ CORE ] Scoreboard Updated for clients')
						core.log('[ CORE ] Scoreboard Updated for clients')

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
					core.data_changed_flags[0] = 1
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
					# Update Judge View
					core.data_changed_flags[13] = 1
					print('[ CORE ] Judge ' + username + ': Status changed to ' + state)
					core.log('[ CORE ] Judge ' + username + ': Status changed to ' + state)

				elif code == 'UpUserStat':
					username = data['Username']
					state = data['State']
					judge_ip = data['IP']
					user_management.update_user_state(
						username, 
						state, 
						judge_ip
					)
					# Update User Tables View
					core.data_changed_flags[1] = 1
					# Update Scoreboard View
					core.data_changed_flags[16] = 1
					print('[ CORE ] User ' + username + ': Status changed to ' + state)
					core.log('[ CORE ] User ' + username + ': Status changed to ' + state)

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
					# Update table views
					# Client accounts
					core.data_changed_flags[1] = 1
					# judge accounts
					core.data_changed_flags[13] = 1
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
					else:
						print('[ CORE ] Account generation failed!')
						core.log('[ CORE ] Account generation failed!')

					# Indicate new insertions in accounts
					core.data_changed_flags[5] = 1

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
					else:
						print('[ CORE ] Sheet accounts added!')
						core.log('[ CORE ] Sheet accounts added!')
	
					# Indicate new insertions in accounts
					core.data_changed_flags[5] = 1

				elif code == 'AddNewScore':
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
					# Update Scoreboard accounts view
					core.data_changed_flags[16] = 1
					print('[ CORE ] Added new user in scoreboard.')
					core.log('[ CORE ] Added new user in scoreboard.')

				elif code == 'AddNewSub':
					try:
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
						# Update Submissions view
						core.data_changed_flags[0] = 1
					except:
						print('Error while inserting data')

				elif code == 'UpUserPwd':
					username = data['Username']
					password = data['New Password']
					user_management.update_user_password(username, password) 
					print('[ CORE ] Updated user ' + username + '\'s Password to ' + password)
					core.log('[ CORE ] Updated user ' + username + '\'s Password to ' + password)
					# Update account views
					core.data_changed_flags[5] = 1
					core.data_changed_flags[1] = 1

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
					# Refresh GUI
					core.data_changed_flags[0] = 1
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
					core.data_changed_flags[0] = 1

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
					print('[ EVENT ][ BROADCAST ] UPDATE Contest')
					core.log('[ EVENT ][ BROADCAST ] UPDATE Contest')
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
				
				# QUERY reply to client or broadcast
				elif code == 'QUERY':
					if data['Mode'] == 'Client':
						print('[ EVENT ][ UNICAST ] New Query response to client')
						core.log('[ EVENT ][ UNICAST ] New Query response to client')
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
						print('[ EVENT ][ BROADCAST ] New Query response broadcasted')
						core.log('[ EVENT ][ BROADCAST ] New Query response broadcasted')
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
				elif code == 'AddQuery':
					query_id = data['Query ID']
					client_id = data['Client ID']
					query = data['Query']
					query_management.insert_query(
						query_id, 
						client_id, 
						query
					)
					core.data_changed_flags[9] = 1
		
				# Client has been DiSCoNnecTed
				elif code == 'DSCNT':
					if data['Mode'] == 1:
						client = data['Client']
						print('[ EVENT ] Disconnect client : ' + str(client))
						core.log('[ EVENT ] Disconnect client : ' + str(client))
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
						print('[ EVENT ] Disconnect all clients')
						core.log('[ EVENT ] Disconnect all clients')
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

				elif code == 'JDSCNT':
					judge = data['Judge']
					if judge == '__ALL__':
						# Disconnect all judges
						print('[ EVENT ] Disconnect All Judges')
						core.log('[ EVENT ] Disconnect All Judges')
						message = {
							'Code' : 'DSCNT'
						}
						message = json.dumps(message)
						core.channel.basic_publish(
							exchange = core.judge_broadcast_exchange,
							routing_key = '', 
							body = message
						)
					else:
						print('[ EVENT ] Disconnect judge : ' + judge)
						core.log('[ EVENT ] Disconnect judge : ' + judge)
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
					print('[ EVENT ] Judge Block ' + username)
					core.log('[ EVENT ] Judge Block ' + username)
					message = {
						'Code' : 'BLOCK'
					}
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.judge_unicast_exchange, 
						routing_key = username, 
						body = message
					)

				elif code == 'BLOCK':
					username = data['Receiver']
					print('[ EVENT ] Block ' + username)
					core.log('[ EVENT ] Block ' + username)
				
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.unicast_exchange, 
						routing_key = username, 
						body = message
					)
				
				elif code in ['VALID', 'INVLD', 'LRJCT', 'SRJCT']:
					# Pass the message to appropiate recipient, nothing to process in data
					receiver = data['Receiver']
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.unicast_exchange, 
						routing_key = receiver, 
						body = message
					)
					
		except Exception as error:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[ ERROR ] Data could not be transmitted : ' + str(error) + ' on line ' + str(exc_tb.tb_lineno)) 
			core.log('[ ERROR ] Data could not be transmitted : ' + str(error) + ' on line ' + str(exc_tb.tb_lineno))
		finally:
			return 0
