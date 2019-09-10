import pika


# Class to handle connection establishment requests
class manage_connection():

	# Function to establish connection
	def initialize_connection(rabbitmq_username,rabbitmq_password,host):
		connection = pika.BlockingConnection(
			pika.URLParameters(
				"amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"
				))
		channel = connection.channel()
		
		# binding credential manager exchange and login_request queue  which send the login request from client to server
		channel.queue_bind(
			exchange = 'connection_manager', 
			queue = 'client_requests'
			)
		return channel,connection

	def terminate_connection(connection):
		connection.close()