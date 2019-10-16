import sched, time
import json
import pika
import sys
from init_server import initialize_server

class broadcast_manager():
	data_changed_flags = ''
	channel = ''
	file_password = ''
	def init_broadcast(data_changed_flags, data_from_interface, superuser_username='guest', superuser_password = 'guest', host = 'localhost'):
		broadcast_manager.data_changed_flags = data_changed_flags
		channel = broadcast_manager.init_connection(superuser_username, superuser_password, host)
		broadcast_manager.channel = channel

		#initialize_server.read_config()
		broadcast_manager.file_password = initialize_server.get_password()
		
		s = sched.scheduler(time.time, time.sleep)
		s.enter(0.5, 1, broadcast_manager.poll, (s, data_from_interface, ))
		s.run()
		print("[ STOPPED ] Broadcast Thread")
		return

	def init_connection(superuser_username, superuser_password, host):
		try:
			creds = pika.PlainCredentials(superuser_username, superuser_password)
			params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
			connection = pika.BlockingConnection(params)
			channel = connection.channel()
			channel.exchange_declare(exchange = 'broadcast_manager', exchange_type = 'fanout', durable = True)
			return channel
		
		except Exception as error:
			print('[ CRITICAL ] Broadcast Manager could not connect to RabbitMQ server : ' + str(error))
			sys.exit()


		return 
	def poll(s, data_from_interface):
		# If sys exit is called
		if(broadcast_manager.data_changed_flags[7] == 1):
			return

		# While there is data to process,
		while data_from_interface.empty() == False:
			data = data_from_interface.get()
			data = json.loads(data)
			print('[ DATA ] Recieved a new broadcast')
			if data['Code'] == 'START':
				print('[ EVENT ] START Contest')
				message = {
				'Code' : 'START',
				'Duration' : data['Time'],
				'Problem Key' : broadcast_manager.file_password
				}
				message = json.dumps(message)
				broadcast_manager.channel.basic_publish(exchange = 'broadcast_manager', routing_key = '', body = message)
			elif data['Code'] == 'STOP':
				# Don't allow Submissions
				print('[ EVENT ] STOP Contest')
				message = {
				'Code' : 'STOP'
				}
				message = json.dumps(message)
				broadcast_manager.channel.basic_publish(exchange = 'broadcast_manager', routing_key = '', body = message)
			elif data['Code'] == 'UPDATE':
				# Don't allow Submissions
				print('[ EVENT ] UPDATE Contest')
				message = {
				'Code' : 'UPDATE',
				'Time' : data['Time']
				}
				message = json.dumps(message)
				broadcast_manager.channel.basic_publish(exchange = 'broadcast_manager', routing_key = '', body = message)
			
			
			



		
		s.enter(1, 1, broadcast_manager.poll, (s, data_from_interface, ))
		return