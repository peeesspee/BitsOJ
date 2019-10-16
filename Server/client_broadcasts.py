import sched, time
import json
import pika
import sys

class broadcast_manager():
	data_changed_flags = ''
	channel = ''
	def init_broadcast(data_changed_flags, data_from_interface, superuser_username='guest', superuser_password = 'guest', host = 'localhost'):
		broadcast_manager.data_changed_flags = data_changed_flags
		channel = broadcast_manager.init_connection(superuser_username, superuser_password, host)
		broadcast_manager.channel = channel
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
			print('[ DATA ] Recieved a new broadcast : ' + data)
			if data == 'START':
				print('[ EVENT ] START Contest')
				message = {
				'Code' : 'START',
				'Duration' : '02:00',
				'Problem Key' : 'Papa'
				}
				message = json.dumps(message)
				broadcast_manager.channel.basic_publish(exchange = 'broadcast_manager', routing_key = '', body = message)
			
			



		
		s.enter(1, 1, broadcast_manager.poll, (s, data_from_interface, ))
		return