# This process handles all the requests in the queue task_queue and updates database
# It also sends data to clients/judges either in unicast or in broadcast.
import json, pika, sys, time
from init_server import initialize_server
from database_management import client_authentication
  
class core():
	data_changed_flags = ''
	task_queue = ''
	channel = ''
	file_password = ''
	unicast_exchange = 'connection_manager'
	broadcast_exchange = 'broadcast_manager'

	def init_core(data_changed_flags, task_queue):
		print('  [ START ] Core subprocess started.')
		core.data_changed_flags = data_changed_flags
		core.task_queue = task_queue
		config = initialize_server.read_config()

		superuser_username = config['Server Username']
		superuser_password = config['Server Password']
		host = config['Server IP']
		core.file_password = config["File Password"]
	
		channel = core.init_connection(superuser_username, superuser_password, host)
		core.channel = channel

		# Infinite Loop to Poll the task_queue every second
		while True:
			status = core.poll(task_queue)
			if status == 1:
				break
			# Poll every second
			time.sleep(1)

		# If we reach this point, it means the Server Shutdown has been initiated.
		print("[ STOP ] Core subprocess terminated successfully!")
		return

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
				
				# Contest START signal
				if data['Code'] == 'START':
					print('[ EVENT ][ BROADCAST ] START Contest')
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
				elif data['Code'] == 'STOP':
					# Don't allow Submissions
					print('[ EVENT ][ BROADCAST ] STOP Contest')
					message = {
					'Code' : 'STOP'
					}
					message = json.dumps(message)
					core.channel.basic_publish(
						exchange = core.broadcast_exchange, 
						routing_key = '', 
						body = message
					)
				
				# UPDATE client timer to match server value
				elif data['Code'] == 'UPDATE':
					# Don't allow Submissions
					print('[ EVENT ][ BROADCAST ] UPDATE Contest')
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
				
				# QUERY reply to client or broadcast
				elif data['Code'] == 'QUERY':
					if data['Mode'] == 'Client':
						print('[ EVENT ][ UNICAST ] New Query response to client')
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
				elif data['Code'] == 'DSCNT':
					if data['Mode'] == 1:
						client = data['Client']
						print('[ EVENT ] Disconnect client : ' + str(client))
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
					
				# Contest SCoReBoarD
				elif data['Code'] == 'SCRBD':
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.broadcast_exchange, 
						routing_key = '', 
						body = message
					)

				# Contest EXTeND signal
				elif data['Code'] == 'EXTND':
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.broadcast_exchange, 
						routing_key = '', 
						body = message
					)

				elif data['Code'] in ['VALID', 'INVLD', 'LRJCT', 'SRJCT', 'VRDCT']:
					# Pass the message to appropiate recipient, nothing to process in data
					receiver = data['Receiver']
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = core.unicast_exchange, 
						routing_key = receiver, 
						body = message
					)

				elif data['Code'] == 'JUDGE':
					message = json.dumps(data)
					core.channel.basic_publish(
						exchange = 'connection_manager', 
						routing_key = 'judge_requests', 
						body = message, 
						properties = pika.BasicProperties(delivery_mode = 2)
					) 

			return
		except Exception as error:
			print('[ ERROR ] Data could not be broadcasted : ' + str(error)) 
		finally:
			return 0