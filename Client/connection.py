import pika

# Class to handle connection establishment requests
class establish_connection():

	# Function to establish connection
	def make_connection(rabbitmq_username,rabbitmq_password,host):
		connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
		channel = connection.channel()
		return channel,connection

	# Function for queue binding with the given exchange
	def binding_queue(channel):
		# binding credential manager exchange and login_request queue  which send the login request from client to server
		channel.queue_bind(exchange = 'credential_manager', queue = 'login_requests')

	def main_function(rabbitmq_username,rabbitmq_password,host):
		channel,connection = establish_connection.make_connection(rabbitmq_username,rabbitmq_password,host)
		establish_connection.binding_queue(channel)
		return channel,connection
