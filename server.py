import pika
import threading


# Variables  
rabbitmq_username = 'BitsOJ'
rabbitmq_password = 'root'
host = 'localhost'


# Establish a connection with RabbitMQ Server
# connection object is returned by the server
connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
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


# This function generates a new client ID to identify clients later.
def generate_new_client_id():
	return "123"


#This function validates the (username, password) pair in the database.
def validate_client(username, password, client_id):
	#Validate client in database
	status = True
	return status


# This function handles the client login requests
def client_login_handler(ch, method, properties, body):
	print("Got something to validate...")
	# Decode the message sent by client
	client_message = body.decode("utf-8")
	# Client sends the username, password as "username+password", so we split it.
	client_username, client_password, client_id = client_message.split('+')

	if client_id == "Null":
		pass
	else:
		pass

	print("Validating " + client_username + ":" + client_password + ":" + client_id +" pair... ")

	# Validate the client from the database
	status = validate_client(client_username, client_password, client_id)

	# If login is successful:
	if status == True:
		print("Client Verified.")

		# Generate a new client ID for our verified client
		if client_id == "Null":
			client_id = generate_new_client_id()

		server_message = "Hello buddy!!"

		# Reply to be sent to client
		message = "Valid+" +  client_id +"+" + server_message

		print("> Server sent :" + message)

		# The client listens on its own queue, whose name = client_username (Hard-coded)
		# This queue is declared in the client.py file
		channel.basic_publish(exchange = 'credential_manager', routing_key = client_username, body = message)
	# If login is not successful:
	else:
		print("Client NOT Verified.")
		message = "Invld+"
		channel.basic_publish(exchange = 'credential_manager', routing_key = client_username, body = message)


#Listens for client logins
def login_handler():
	print("Listening for client input...\n")
	#Client sends login request on login_requests
	channel.basic_consume(queue = 'login_requests', on_message_callback = client_login_handler, auto_ack = True)
	channel.start_consuming()

def client_handler():
	return

def judge_handler():
	return

def gui_handler():
	return


def thread_handler():
	#Create threads and give their targets
	login_thread = threading.Thread(target = login_handler)
	client_thread = threading.Thread(target = client_handler)
	judge_thread = threading.Thread(target = judge_handler)
	gui_thread = threading.Thread(target = gui_handler)

	#start threads
	login_thread.start()
	client_thread.start()
	judge_thread.start()
	gui_thread.start()

	#Join threads (Tell main program to wait until all these threads finish)
	login_thread.join()
	client_thread.join()
	judge_thread.join()
	gui_thread.join()


def main():
	thread_handler()
	connection.close()

main()



