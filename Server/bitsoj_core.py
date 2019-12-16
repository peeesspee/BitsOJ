# This process handles all the requests in the queue task_queue and updates database
# It also sends data to clients/judges either in unicast or in broadcast.
import json, pika, sys, time
from init_server import initialize_server
from database_management import client_authentication, submissions_management, scoreboard_management
   
class core():
	data_changed_flags = ''
	task_queue = ''
	channel = ''
	file_password = ''
	unicast_exchange = 'connection_manager'
	broadcast_exchange = 'broadcast_manager'
	config = ''

	def init_core(data_changed_flags, task_queue, log_queue):
		core.data_changed_flags = data_changed_flags
		core.task_queue = task_queue
		core.log_queue = log_queue
		core.config = initialize_server.read_config()
		
		print('  [ START ] Core subprocess started.')
		core.log('  [ START ] Core subprocess started.')

		superuser_username = core.config['Server Username']
		superuser_password = core.config['Server Password']
		host = core.config['Server IP']
		core.file_password = core.config["File Password"]
	
		channel = core.init_connection(superuser_username, superuser_password, host)
		core.channel = channel
		core.ranking_algoritm = core.data_changed_flags[17]
		# Infinite Loop to Poll the task_queue every second
		while True:
			status = core.poll(task_queue)
			if status == 1:
				break
			# Poll every second
			time.sleep(0.5)

		# If we reach this point, it means the Server Shutdown has been initiated.
		print("[ STOP ] Core subprocess terminated successfully!")
		core.log("[ STOP ] Core subprocess terminated successfully!")
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

			return channel
		
		except Exception as error:
			print('[ CRITICAL ] Core could not connect to RabbitMQ server : ' + str(error))
			core.log('[ CRITICAL ] Core could not connect to RabbitMQ server : ' + str(error))
			core.data_changed_flags[7] = 1
			sys.exit()
		return 

	def poll(task_queue):
		# If sys exit is called, the following flag will be 1
		if(core.data_changed_flags[7] == 1):
			return 1

		# While there is data to process in the task_queue,
		try:
			while task_queue.empty() == False:
				# Data in the task queue is in JSON format
				data = task_queue.get()
				data = json.loads(data)
				code = data['Code']
				# Contest START signal
				if code == 'START':
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
				
				# Contest STOP signal
				elif code == 'STOP':
					# Don't allow Submissions
					print('[ EVENT ][ BROADCAST ] STOP Contest')
					core.log('[ EVENT ][ BROADCAST ] STOP Contest')
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
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.broadcast_exchange, 
						routing_key = '', 
						body = message
					)

				elif code == 'VRDCT':
					receiver = data['Receiver']
					run_id = data['Run ID']
					status = data['Status']
					client_id = data['Client ID']
					p_code = data['Problem Code']
					time_stamp = data['Timestamp']
					try:
						judge = data['Judge']
					except:
						print('No judge')
						judge = 'OOPS'
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.unicast_exchange, 
						routing_key = receiver, 
						body = message
					)
					# Update Database
					submissions_management.update_submission_status(run_id, status, 'SENT', judge)
					# Update Submissions GUI
					core.data_changed_flags[0] = 1

					# Update scoreboard
					problem_max_score = core.config['AC Points']
					penalty_score = core.config['Penalty Score']
					penalty_time = core.config['Penalty Time']
					# call scoreboard updation function		TODO MOVE TO CORE
					scoreboard_management.update_user_score(
						client_id, 
						run_id,
						problem_max_score, 
						penalty_score,
						penalty_time,
						status, 
						p_code,
						time_stamp,
						core.ranking_algoritm # Ranking Algorithm
					)
					# Update scoreboard view in server
					core.data_changed_flags[16] = 1
					# Broadcast new scoreboard to clients whenever a new AC is recieved 
					# and scoreboard update is allowed.
					if status == 'AC' and core.data_changed_flags[15] == 1:
						# Flag 18 signals interface to send scoreboard to all clients if allowed
						core.data_changed_flags[18] = 1 

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
							'Client ID' : data['Client ID'],
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
							exchange = core.broadcast_exchange, 
							routing_key = '', 
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
					
				elif code in ['VALID', 'INVLD', 'LRJCT', 'SRJCT']:
					# Pass the message to appropiate recipient, nothing to process in data
					receiver = data['Receiver']
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.unicast_exchange, 
						routing_key = receiver, 
						body = message
					)
			return
		except Exception as error:
			print('[ ERROR ] Data could not be broadcasted : ' + str(error)) 
			core.log('[ ERROR ] Data could not be broadcasted : ' + str(error))
		finally:
			return 0