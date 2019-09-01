import pika


class authenticate_login():
	global username
	global channel
	global host
	host = 'localhost'
	# Sends the username and password for login request to the client 
	def login():
		global username
		global channel
		global host
		username = input('Enter your username : ') or 'dummy'
		password = input('Enter your password : ') or 'dummy'
		client_id = 'Null'
		print("[ Validating ] : " + username + "@" + password)

		# sending username and password to the server
		channel.basic_publish(exchange = 'credential_manager', routing_key = 'login_requests', body = username + '+' + password + '+' + client_id)

		# Declaring queue for the new client
		channel.queue_declare(queue = username)
		channel.queue_bind(exchange = 'credential_manager', queue = username)
		print("[ Listening ] @ " + host)

		# Listening from the server for the login request
		channel.basic_consume(queue = username, on_message_callback = authenticate_login.server_response_handler, auto_ack = True)
		channel.start_consuming()


	def server_response_handler(ch,method,properties,body):
		global channel
		global username
		global host
		server_data = body.decode('utf-8')

		# status of the login request
		status = server_data[0:5]
		if(status == 'Valid'):
			status,client_id,server_message = server_data.split('+')
			print("[ Status ] " + status + "\n[ ClientID ] : " + client_id + "\n[ Server ] : " + server_message)
		else:
			# if the login fails deleting the existing queue for the client and again asking for login
			channel.queue_delete(queue = username)
			authenticate_login.login(channel)


	def main_function(channel_1,host_1):
		global channel
		global host
		channel = channel_1
		host = host_1
		authenticate_login.login()