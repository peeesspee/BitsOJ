import pika


class establish_connection():

	rabbitmq_username = 'client'
	rabbitmq_password = 'client'
	host = 'localhost'

	def make_connection():
		connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
		channel = connection.channel()


