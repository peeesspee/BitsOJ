import pika


class authenticate_login():
	username = ''
	channel = ''
	client_id = 'Null'
	host = 'localhost'
		
	# Sends the username and password for login request to the client 
	def login():
		authenticate_login.username = input('Enter your username : ') or 'dummy'
		password = input('Enter your password : ') or 'dummy'
		
		print("[ Validating ] : " + authenticate_login.username + "@" + password)

		# sending username and password to the server
		authenticate_login.channel.basic_publish(exchange = 'credential_manager', routing_key = 'login_requests', body = authenticate_login.username + '+' + password + '+' + authenticate_login.client_id)

		# Declaring queue for the new client
		authenticate_login.channel.queue_declare(queue = authenticate_login.username)
		authenticate_login.channel.queue_bind(exchange = 'credential_manager', queue = authenticate_login.username)
		print("[ Listening ] @ " + authenticate_login.host)

		# Listening from the server for the login request
		authenticate_login.channel.basic_consume(queue = authenticate_login.username, on_message_callback = authenticate_login.server_response_handler, auto_ack = True)
		authenticate_login.channel.start_consuming()


	def server_response_handler(ch,method,properties,body):
		server_data = body.decode('utf-8')

		# status of the login request
		status = server_data[0:5]
		if(status == 'Valid'):
			status,authenticate_login.client_id,server_message = server_data.split('+')
			print("[ Status ] " + status + "\n[ ClientID ] : " + authenticate_login.client_id + "\n[ Server ] : " + server_message)
		else:
			# if the login fails deleting the existing queue for the client and again asking for login
			authenticate_login.channel.queue_delete(queue = authenticate_login.username)
			authenticate_login.login(authenticate_login.channel)


	def main_function(channel1,host1):
		authenticate_login.channel = channel1
		authenticate_login.host = host1
		authenticate_login.login()


