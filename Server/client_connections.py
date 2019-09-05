import pika
from database_management import client_authentication
from client_submissions import submission

class manage_clients():
	channel = ''

	# This function continously listens for client messages 
	def listen_clients(channel1):
		manage_clients.channel = channel1
		# Clients send requests on client_requests
		# As soon as a new message is recieved, it is sent to client_message_handler for further processing
		channel1.basic_consume(queue = 'client_requests', on_message_callback = manage_clients.client_message_handler, auto_ack = True)
		channel1.start_consuming()

	# This function works on client messages and passes them on to their respective handler function
	def client_message_handler(ch, method, properties, body):
		# Decode the message sent by client
		# First 5 characters contain metadata
		client_message = str(body.decode("utf-8"))
		
		print("[ PING ] Recieved a new client message ")
		client_code = client_message[0:6]
		if client_code == 'LOGIN ':
			manage_clients.client_login_handler(client_message[6:])
		elif client_code == 'SUBMT ':
			manage_clients.client_submission_handler(client_message[6:])

	# This function handles all client login requests
	def client_login_handler(client_message):
		# Client sends the username, password, clientID as "username+password+clientID", so we split it.
		# Default value of clientID is "Null" (String)
		try:
			client_username, client_password, client_id, client_type = client_message.split(' ')
		except Exception as error:
			print("[ ERROR ] Client data parsing error : " + str(error))
			print("[ DEBUG ] Client message was : " + str(client_message))

		print("[ LOGIN ] " + " > " + client_username + "@" + client_password + "[ TYPE ] " + client_type)
		# Validate the client from the database
		status = client_authentication.validate_client(client_username, client_password)

		#Bind the connection_manager exchange to client queue (que name is same as username)
		manage_clients.channel.queue_bind(exchange = "connection_manager", queue = client_username)

		# The client listens on its own queue, whose name = client_username (Hard-coded)
		# This queue is declared in the client.py file
		# Every response sent to client has 5 initial characters which specify what server is going to talk about.
		# "Valid" signifies a valid login.
		# "Invld" signifies an invalid login attempt.

		# If login is successful:
		if status == True:
			# Check if client has logged in for the first time:
			status = client_authentication.check_connected_client(client_username)
			# If client has NOT logged in for the first time
			if status == True:
				client_id = client_authentication.get_client_id(client_username)
				print("[ " + client_username + " ] Previous Client ID : " + client_id )

			# If client has logged in for the first time
			else:
				# Fetch client ID
				client_id = client_authentication.generate_new_client_id()
				# Add client to connected users list
				client_authentication.add_connected_client(client_id, client_username)
				print("[ " + client_username + " ] Assigned : " + client_id )

			# Reply to be sent to client
			server_message = "Hello buddy!!"

			message = "VALID+" +  client_id + "+" + server_message

			print("[ SENT ] " + message)

			# Send login_successful signal to client. 
			manage_clients.publish_message(client_username, message)
			
		# If login is not successful:
		elif status == False:
			print("[ " + client_username + " ] NOT verified.")
			message = "INVLD"
			# Reply "Invalid credentials" to client
			manage_clients.publish_message(client_username, message)

	def client_submission_handler(client_data):
		try:
			client_id = client_data[0:3]		# client_id is 3 characters 
			problem_code = client_data[4:8]		# problem_code is 4 characters
			language = client_data[9:12]		# language is 3 characters
			time_stamp = client_data[13:21]		# time_stamp is 8 characters: HH:MM:SS
			source_code = client_data[22:]
			print("[ DATA ] CID :" + client_id + " PCODE:" + problem_code + " Language :" + language + " Time stamp :" + time_stamp)

			print("[ SUBMIT ]")

			result, run_id, error = submission.new_submission(client_id, problem_code, language, time_stamp, source_code) 
			message = "VRDCT+" + run_id + '+' + result + '+' + error

			client_username = client_authentication.get_client_username(client_id)
			manage_clients.publish_message(client_username, message)
		except Exception as error:
			print("[ ERROR ] Client data parsing error : " + str(error))
			

	def publish_message(queue_name, message):
		print( "[ PUBLISH ] " + message + " TO " + queue_name)
		manage_clients.channel.basic_publish(exchange = 'connection_manager', routing_key = queue_name, body = message)
		return
	