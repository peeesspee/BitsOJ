import pika
from database_management import client_authentication

class manage_clients():
	channel = ''

	def listen_clients(channel1):
		manage_clients.channel = channel1
		#Client sends login request on login_requests
		channel1.basic_consume(queue = 'client_requests', on_message_callback = manage_clients.client_login_handler, auto_ack = True)
		channel1.start_consuming()


	def client_login_handler(ch, method, properties, body):
		# Decode the message sent by client
		client_message = body.decode("utf-8")
		# Client sends the username, password, clientID as "username+password+clientID", so we split it.
		#Default value of clientID is "Null" (String)
		client_username, client_password, client_id = client_message.split('+')
		print("[ LOGIN ] " + "[ " + client_id + " ] > " + client_username + "@" + client_password)

		# Validate the client from the database
		status = client_authentication.validate_client(client_username, client_password, client_id)

		# If login is successful:
		if status == True:
			# If client logs in for the first time:
			if client_id == "Null":
				client_id = client_authentication.generate_new_client_id()

			print("[ " + client_username + " ] : Assigned : [ " + client_id + " ]")

			# Reply to be sent to client
			server_message = "Hello buddy!!"
			message = "Valid+" +  client_id +"+" + server_message

			print("[ Sent ] " + message)

			# The client listens on its own queue, whose name = client_username (Hard-coded)
			# This queue is declared in the client.py file
			manage_clients.channel.basic_publish(exchange = 'connection_manager', routing_key = client_username, body = message)

		# If login is not successful:
		else:
			print("[ " + client_username + " ] : NOT verified.")

			# Reply Invalid credentials to client
			# Every response sent to client has 5 initial characters which specify what server is going to talk about.
			# Invld signifies an invalid login attempt.
			message = "Invld+"
			manage_clients.channel.basic_publish(exchange = 'connection_manager', routing_key = client_username, body = message)

	