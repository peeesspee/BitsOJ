import pika
from threading import *


#Variables  
rabbitmq_username = 'BitsOJ'
rabbitmq_password = 'root'
host = 'localhost'


# Establish a connection with RabbitMQ Server
# connection object is returned by the server
connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
channel = connection.channel()

#Declare queues and exchanges
try:
	channel.queue_declare(queue = 'login_requests', durable = True)
	channel.queue_declare(queue = 'login_response', durable = True)
	channel.queue_declare(queue = 'client_requests', durable = True)
	channel.queue_declare(queue = 'client_response', durable = True)
	channel.queue_declare(queue = 'judge_requests', durable = True)
	channel.queue_declare(queue = 'judge_verdicts', durable = True) 
except:
	print("Queue declaration error: Give administrator access to BitsOJ in RabbitMQ Management.")

try:
	channel.exchange_declare(exchange = 'connection_manager', exchange_type = 'topic', durable = True)
	channel.exchange_declare(exchange = 'credential_manager', exchange_type = 'topic', durable = True)
	channel.exchange_declare(exchange = 'judge_manager', exchange_type = 'direct', durable = True)
except:
	print("Exchange declaration error: Give administrator access to BitsOJ in RabbitMQ Management.")



channel.queue_bind(exchange = 'credential_manager', queue = 'login_requests')
# channel.queue_bind(exchange = 'credential_manager', queue = 'login_response')


def validate_client(username, password):
	#Validate client in database
	status = True
	return status



def client_handler(ch, method, properties, body):
	print("Got something to validate...")
	client_message = body.decode("utf-8")
	client_username, client_password = client_message.split('+')

	print("Validating " + client_username + ":" + client_password + " pair... ")

	status = validate_client(client_username, client_password)
	
	if status == True:
		print("Client Verified.")
		message = "Hello " + client_username
		channel.basic_publish(exchange='credential_manager', routing_key = 'login_requests', body = message)
	else:
		print("Client NOT Verified.")
		message = "Hello imposter"
		channel.basic_publish(exchange='credential_manager', routing_key = 'login_response', body = message)



def login_handler():
	print("Listening for client input...\n")
	channel.basic_consume(queue = 'login_requests', on_message_callback = client_handler, auto_ack = True)
	channel.start_consuming()





def main():
	login_handler()

main()
connection.close()




















#login_thread = Thread(target = login_handler)
#login_thread.start()



	


