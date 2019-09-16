from manage_data_sending import send_options 
from connection import manage_connection
# from interface import Login

class authenticate_login():
	username = None
	channel = None
	client_id = 'Null'
	host = ''
 

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

		authenticate_login.channel.queue_bind(
			exchange = 'connection_manager', 
			queue = authenticate_login.username
			)

		authenticate_login.channel.basic_publish(
			exchange = 'connection_manager', 
			routing_key = 'client_requests', 
			body = 'LOGIN ' + authenticate_login.username + ' ' + password + ' ' + authenticate_login.client_id + ' CLIENT'
			)
		
		# send_options.publish_data(authenticate_login.channel)

		print("[ Listening ] @ " + authenticate_login.host)
		return True


	def get_user_details():
		return authenticate_login.client_id, authenticate_login.username