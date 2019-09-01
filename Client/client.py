import pika
from Client.connection import establish_connection
from threading import *
import sqlite3

# rabbitmq_username = 'client'
# rabbitmq_password = 'client'
# host = 'localhost'


# #channel.queue_delete(queue = 'queue_name')

# # establshing connection with the server
# connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
# channel = connection.channel()

establish_connection.make_connection()


# binding credential manager exchange and login_request queue  which send the login request from client to server 
channel.queue_bind(exchange = 'credential_manager', queue = 'login_requests')
 
# client username
global username
# Client ID
global client_id


# receives the message from the server whether the login is successful or not
def server_response_handler(ch, method, properties, body):
	global username
	server_data = body.decode("utf-8")
	# status of the login request
	status = server_data[0:5]
	if(status == 'Valid'):
		status,client_id,server_message = server_data.split('+')
		print("[ Status ] " + status + "\n[ ClientID ] : " + client_id + "\n[ Server ] : " + server_message)
	else:
		# if the login fails deleting the existing queue for the client and again asking for login
		channel.queue_delete(queue = username)
		login()
	
	
# Sends the username and password for login request to the client 
def login():
	global username
	global client_id
	username = input("Username : ") or "dummy"
	password = input("Password : ") or "dummy"
	client_id = "Null"
	print("[ Validating ] : " + username + "@" + password)

	# sending username and password to the server
	channel.basic_publish(exchange = 'credential_manager', routing_key = 'login_requests', body = username + '+' + password + '+' + client_id)

	# Declaring queue for the new client 
	channel.queue_declare(queue = username)
	channel.queue_bind(exchange = 'credential_manager', queue = username)
	print("[ Listening ] @ " + host)

	# Listening from the server for the login request
	channel.basic_consume(queue = username, on_message_callback = server_response_handler, auto_ack = True)
	channel.start_consuming()




def main():
	login()

main()
connection.close()
