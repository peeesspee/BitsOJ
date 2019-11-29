# import sched, time
import json
import pika
import sys
import time
from init_server import initialize_server
  
class core():
	data_changed_flags = ''
	channel = ''
	file_password = ''
	def init_core(data_changed_flags, data_from_interface):
		core.data_changed_flags = data_changed_flags
		config = initialize_server.read_config()

		superuser_username = config['Server Username']
		superuser_password = config['Server Password']
		host = config['Server IP']

		channel = core.init_connection(superuser_username, superuser_password, host)
		core.channel = channel

		
		core.file_password = config["File Password"]
		
		# s = sched.scheduler(time.time, time.sleep)
		# s.enter(0.5, 1, core.poll, (s, data_from_interface, ))
		# s.run()
		while True:
			status = core.poll(data_from_interface)
			if status == 1:
				break
			# Poll every second
			time.sleep(1)

		print("[ STOP ] Core subprocess terminated successfully!")
		return

	def init_connection(superuser_username, superuser_password, host):
		try:
			creds = pika.PlainCredentials(superuser_username, superuser_password)
			params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
			connection = pika.BlockingConnection(params)
			channel = connection.channel()
			channel.exchange_declare(exchange = 'core', exchange_type = 'fanout', durable = True)
			return channel
		
		except Exception as error:
			print('[ CRITICAL ] Broadcast Manager could not connect to RabbitMQ server : ' + str(error))
			sys.exit()


		return 
	def poll(data_from_interface):
		# If sys exit is called
		if(core.data_changed_flags[7] == 1):
			return 1

		# While there is data to process,
		try:
			while data_from_interface.empty() == False:
				data = data_from_interface.get()
				data = json.loads(data)
				print('\n[ DATA ] Recieved a new broadcast')
				# Contest START signal
				if data['Code'] == 'START':
					print('[ EVENT ] START Contest')
					message = {
					'Code' : 'START',
					'Duration' : data['Duration'],
					'Start Time' : data['Start Time'],
					'End Time' : data['End Time'],
					'Problem Key' : core.file_password
					}
					message = json.dumps(message)
				
				# Contest STOP signal
				elif data['Code'] == 'STOP':
					# Don't allow Submissions
					print('[ EVENT ] STOP Contest')
					message = {
					'Code' : 'STOP'
					}
					message = json.dumps(message)
				
				# UPDATE client timer to match server value
				elif data['Code'] == 'UPDATE':
					# Don't allow Submissions
					print('[ EVENT ] UPDATE Contest')
					message = {
					'Code' : 'UPDATE',
					'Time' : data['Time']
					}
					message = json.dumps(message)
				
				# QUERY reply to client or broadcast
				elif data['Code'] == 'QUERY':
					if data['Mode'] == 1:
						print('[ EVENT ] New Query response to client')
					else:
						print('[ EVENT ] New Query response broadcast')
					message = {
					'Code' : 'QUERY',
					'Client ID' : data['Client ID'],
					'Query' : data['Query'],
					'Response' : data['Response'],
					'Type' : data['Mode']
					}
					message = json.dumps(message)

				# Client has been DiSCoNnecTed
				elif data['Code'] == 'DSCNT':
					if data['Mode'] == 1:
						client = data['Client']
						print('[ EVENT ] Disconnect client : ' + str(client))
						message = {
						'Code' : 'DSCNT',
						'Client' : client
						}
					elif data['Mode'] == 2:
						print('[ EVENT ] Disconnect all clients')
						message = {
						'Code' : 'DSCNT',
						'Client' : 'All'
						}
					message = json.dumps(message)

				# Contest SCoReBoarD
				elif data['Code'] == 'SCRBD':
					message = json.dumps(data)

				# Contest EXTeND signal
				elif data['Code'] == 'EXTND':
					message = json.dumps(data)

				core.channel.basic_publish(exchange = 'broadcast_manager', routing_key = '', body = message)
			return
		except Exception as error:
			print('[ ERROR ] Data could not be broadcasted : ' + str(error)) 
		finally:
			return 0