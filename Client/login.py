import pika


class authenticate_login():
	username = ''
	channel = ''
	client_id = 'Null'
	host = 'localhost'
	

	# Sends the username and password for login request to the client 
	def login(channel1,host1):
		authenticate_login.channel = channel1
		authenticate_login.host = host1
		authenticate_login.username = input('Enter your username : ') or 'dummy'
		password = input('Enter your password : ') or 'dummy'
		
		print("[ Validating ] : " + authenticate_login.username + "@" + password)

		# Declaring queue for the new client
		authenticate_login.channel.queue_declare(
			queue = authenticate_login.username, 
			durable = True
			)

		authenticate_login.channel.queue_bind(
			exchange = 'connection_manager', 
			queue = authenticate_login.username
			)

		# sending username and password to the server
		authenticate_login.channel.basic_publish(
			exchange = 'connection_manager', 
			routing_key = 'client_requests', 
			body = 'LOGIN ' + authenticate_login.username + ' ' + password + ' ' + authenticate_login.client_id
			)

		
		

		print("[ Listening ] @ " + authenticate_login.host)

		# Listening from the server for the login request

	

	def get_user_details():
		return authenticate_login.client_id, authenticate_login.username
