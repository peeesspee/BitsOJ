from connection import manage_connection

class authenticate_login():
	username = None
	channel = None
	client_id = 'Null'
	host = ''
	login_status = 'INVLD'
 

	def login(username, password):
		authenticate_login.channel = manage_connection.channel
		authenticate_login.host = manage_connection.host
		authenticate_login.username = username
		password = password

		print("[ Validating ] : " + authenticate_login.username + "@" + password)

		# Declaring queue for the new client
		authenticate_login.channel.queue_declare(
			queue = authenticate_login.username, 
			durable = True
			)

		# Binding the queue for listening from the server 
		authenticate_login.channel.queue_bind(
			exchange = 'connection_manager', 
			queue = authenticate_login.username
			)

		# Publishing the message ( Username and Password )
		authenticate_login.channel.basic_publish(
			exchange = 'connection_manager', 
			routing_key = 'client_requests', 
			body = 'LOGIN ' + authenticate_login.username + ' ' + password + ' ' + authenticate_login.client_id + ' CLIENT'
			)

		# Listening from the server whether the credentials are valid or not
		authenticate_login.channel.basic_consume(
			queue = username,
			on_message_callback = authenticate_login.server_response_handler,
			auto_ack = True
			)
		print("[ Listening ] @ " + authenticate_login.host)
		# Started listening
		authenticate_login.channel.start_consuming()

		

	def server_response_handler(ch,method,properties,body):
		# Decoding the data 
		server_data = body.decode('utf-8')

		# Extracting the status whether valid or invalid 
		status = server_data[0:5]

		print("[ STATUS ] " + status)
		if (status == 'VALID'):
			print('[ ClientID ] receiving ......')
			status,authenticate_login.client_id,server_message = server_data.split('+')

			print("[ Status ] " + status + "\n[ ClientID ] : " + authenticate_login.client_id + "\n[ Server ] : " + server_message)
			
			# Changing login status to valid
			authenticate_login.login_status = 'VALID'
			authenticate_login.channel.stop_consuming()

		elif (status == 'REJCT'):
			# Changing login status to rejected
			print('[ Authentication ]  REJECTED ......')
			authenticate_login.login_status = 'REJCT'
			authenticate_login.channel.queue_delete(
				queue = authenticate_login.username
				)
		else:
			print("Invalid Login!!!!")
			# Deleting the queue on which the client is listening
			authenticate_login.channel.queue_delete(
				queue = authenticate_login.username
				)		


	# Function to get user details
	def get_user_details():
		return authenticate_login.client_id, authenticate_login.username