import pika

# Class to handle connection establishment requests
class manage_connection():
	data_changed_flags = ''
	channel = ''
	
	# Function to establish connection
	def initialize_connection(rabbitmq_username, rabbitmq_password, host, data_changed_flags):
		manage_connection.data_changed_flags = data_changed_flags
		try:
			creds = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
			params = pika.ConnectionParameters(
				host = host, 
				credentials = creds, 
				heartbeat=0, 
				blocked_connection_timeout=0
			)
			connection = pika.BlockingConnection(params)
			channel = connection.channel()
			manage_connection.channel = channel

			# binding credential manager exchange and login_request queue  which send the login request from client to server
			channel.queue_bind(
				exchange = 'connection_manager', 
				queue = 'client_requests'
			)
			print('[ LOGIN ] Connection established...')
			return connection


		except Exception as error:
			print('[CRITICAL ERROR] Error while establishing connection :', str(error))

		except(KeyboardInterrupt, SystemExit):
			manage_connection.data_changed_flags[3] = 1
			print('[ JUDGE ][ ERROR ] Keyboard Interrupt.')
			channel.stop_consuming()

	def terminate_connection(connection):
		connection.close()

	