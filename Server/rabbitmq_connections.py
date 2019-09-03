import pika

#Class to handle incoming connections
class manage_connections():
	def initialize_connections(superuser_username, superuser_password, host):
		# Establish a connection with RabbitMQ Server
		# connection object is returned by the server
		connection = pika.BlockingConnection(pika.URLParameters("amqp://" + superuser_username + ":" + superuser_password + "@" + host + "/%2f"))
		channel = connection.channel()
		# Declare queues 
		try:
			channel.queue_declare(queue = 'login_requests', durable = True)
			channel.queue_declare(queue = 'client_requests', durable = True)
			channel.queue_declare(queue = 'judge_requests', durable = True)
			channel.queue_declare(queue = 'judge_verdicts', durable = True) 
		except:
			print("Queue declaration error: Give administrator access to BitsOJ in RabbitMQ Management.")

		#Declare exchanges
		try:
			channel.exchange_declare(exchange = 'credential_manager', exchange_type = 'direct', durable = True)
			channel.exchange_declare(exchange = 'connection_manager', exchange_type = 'direct', durable = True)
			channel.exchange_declare(exchange = 'judge_manager', exchange_type = 'direct', durable = True)
		except:
			print("Exchange declaration error: Give administrator access to BitsOJ in RabbitMQ Management.")


		# Bind the queue to exchanges
		# This tells it to listen to that particular exchange 
		channel.queue_bind(exchange = 'credential_manager', queue = 'login_requests')
		return channel, connection


	def main_function(superuser_username, superuser_password, host):
		channel, connection = manage_connections.initialize_connections(superuser_username, superuser_password, host)
		return channel, connection
		
