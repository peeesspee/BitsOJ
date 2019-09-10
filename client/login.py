from manage_data_sending import send_options 

class authenticate_login():
	username = None
	channel = None
	client_id = 'Null'
	host = ''


	def login(channel, host):
		authenticate_login.channel = channel
		authenticate_login.host = host
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

		send_options.publish_data(channel)

		print("[ Listening ] @ " + authenticate_login.host)


	def get_user_details():
		return authenticate_login.client_id, authenticate_login.username