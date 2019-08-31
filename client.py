import pika
from threading import *

rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'



connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
channel = connection.channel()
channel.queue_bind(exchange = 'credential_manager', queue = 'login_requests')



def server_response_handler(ch, method, properties, body):
	server_message = body.decode("utf-8")
	print("Got a message from Server: " + server_message)
	
	


def login():
	username = input("Enter username: ") or "dummy"
	password = input("Enter Password: ") or "dummy"
	print("Validating : " + username + "@" + password)
	channel.basic_publish(exchange = 'credential_manager', routing_key = 'login_requests', body = username + '+' + password)

	print("Listening for server input...\n")
	channel.basic_consume(queue = 'login_response', on_message_callback = server_response_handler, auto_ack = True)
	channel.start_consuming()




def main():
	login()

main()
connection.close()
