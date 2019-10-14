import pika 
import sys


# Class to handle connection establishment requests
class manage_connection():
	channel = ''
	host = ''

	# Function to establish connection
	def initialize_connection(rabbitmq_username,rabbitmq_password,host):
		creds = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
		params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
		connection = pika.BlockingConnection(params)
		channel = connection.channel()
		manage_connection.channel = channel
		manage_connection.host = host
		
		# binding credential manager exchange and login_request queue  which send the login request from client to server
		try:
			channel.queue_bind(
				exchange = 'connection_manager', 
				queue = 'client_requests'
				)
			return channel,connection
		except Exception as Error:
			print("Server is Not yet started Please wait")
			connection.close()
			sys.exit()

	def terminate_connection(connection):
		connection.close()

	def channel_host():
		return manage_connection.channel,manage_connection.host

