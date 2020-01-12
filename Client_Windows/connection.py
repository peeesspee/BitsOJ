import pika 
import sys

# Class to handle connection establishment requests
class manage_connection():
	channel = ''
	host = ''
	connection = ''

	# Function to establish connection
	def initialize_connection(rabbitmq_username,rabbitmq_password,host):
		try:
			# Credential for rabbitmq management
			creds = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
			params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
			connection = pika.BlockingConnection(params)
			manage_connection.connection = connection
			channel = connection.channel()
			manage_connection.channel = channel
			manage_connection.host = host
		except Exception as Error:
			print(str(Error))
			sys.exit()
		
		# binding credential manager exchange and login_request queue  which send the login request from client to server
		try:
			channel.queue_bind(
				exchange = 'connection_manager', 
				queue = 'client_requests'
			)

			return channel,connection
		except Exception as Error:
			print("Server is Not yet started Please wait")
			print(str(Error))
			connection.close()
			sys.exit()

	def terminate_connection():
		manage_connection.connection.close()

	def channel_host():
		return manage_connection.channel,manage_connection.host

