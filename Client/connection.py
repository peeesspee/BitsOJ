import pika

# Class to handle connection establishment requests
class establish_connection():

	# Function to establish connection
	def initialize_connection(rabbitmq_username,rabbitmq_password,host):
		connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
		channel = connection.channel()

		# binding credential manager exchange and login_request queue  which send the login request from client to server
		channel.queue_bind(exchange = 'credential_manager', queue = 'login_requests')
		return channel,connection

	