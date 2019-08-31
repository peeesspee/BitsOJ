import pika
from threading import *
import sqlite3

rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = '192.168.20.17'


#channel.queue_delete(queue = 'queue_name')

# establshing connection with the server
connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
channel = connection.channel()

# binding credential manager exchange and login_request queue  which send the login request from client to server 
channel.queue_bind(exchange = 'credential_manager', queue = 'login_requests')
 
# client username
global username


# receives the message from the server whether the login is successful or not
def server_response_handler(ch, method, properties, body):
	global username
	server_message = body.decode("utf-8")
	# status of the login request
	status = server_message[0:7]
	if(status == '[Valid]'):
		print("Got a message from Server: " + server_message)
	else:
		# if the login fails deleting the existing queue for the client and again asking for login
		channel.queue_delete(queue = username)
		login()
	
	
# Sends the username and password for login request to the client 
def login():
	global username
	username = input("Enter username: ") or "dummy"
	password = input("Enter Password: ") or "dummy"
	print("Validating : " + username + "@" + password)

	# sending username and password to the server
	channel.basic_publish(exchange = 'credential_manager', routing_key = 'login_requests', body = username + '+' + password)

	# Declaring queue for the new client 
	channel.queue_declare(queue = username)
	channel.queue_bind(exchange = 'credential_manager', queue = username)
	print("Listening for server input...\n")

	# Listening from the server for the login request
	channel.basic_consume(queue = username, on_message_callback = server_response_handler, auto_ack = True)
	channel.start_consuming()




def main():
	login()

main()
connection.close()
