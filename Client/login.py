from connection import manage_connection
from init_client import handle_config
import json

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
		conf = handle_config.read_config_json()
		if conf["client_id"] != 'Nul' 
		authenticate_login.client_id = conf["client_id"]
		final_data = { 
			'Code' : 'LOGIN',
			'Username' : username,
			'Password' : password, 
			'ID' : authenticate_login.client_id,
			'Type' : 'CLIENT'
			}
		final_data = json.dumps(final_data)

		# Declaring queue for the new client
		authenticate_login.channel.queue_declare(
			queue = authenticate_login.username, 
			durable = True,
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
			body = final_data
			)

		# Listening from the server whether the credentials are valid or not
		authenticate_login.channel.basic_consume(
			queue = username,
			on_message_callback = authenticate_login.server_response_handler,
			auto_ack = True
			)
		
		print("[ Listening ] @ " + authenticate_login.host)

		# authenticate_login.channel.start_consuming()
		try:
			authenticate_login.channel.start_consuming()
		except(KeyboardInterrupt, SystemExit):
			authenticate_login.channel.stop_consuming()

		

	def server_response_handler(ch,method,properties,body):
		# Decoding the data 
		json_data = str(body.decode('utf-8'))
		server_data = json.loads(json_data)

		# Extracting the status whether valid or invalid 
		status = server_data['Code']

		print("[ STATUS ] " + status)
		if (status == 'VALID'):
			print('[ ClientID ] receiving ......')
			config = handle_config.read_config_json()

			config["client_id"] = str(server_data["Client ID"])
			handle_config.write_config_json(config) 

			print("[ Status ] " + status + "\n[ ClientID ] : " + str(server_data["Client ID"]) + "\n[ Server ] : " + server_data["Message"])
			
			# Changing login status to valid
			authenticate_login.login_status = 'VALID'
			authenticate_login.client_id = server_data["Client ID"]
			authenticate_login.channel.stop_consuming()

		elif (status == 'REJCT'):
			# Changing login status to rejected
			print('[ Authentication ]  REJECTED ......')
			authenticate_login.login_status = 'LRJCT'
			authenticate_login.channel.queue_delete(
				queue = authenticate_login.username
				)
		else:
			print("Invalid Login!!!!")
			authenticate_login.login_status = 'INVLD'
			# Deleting the queue on which the client is listening
			authenticate_login.channel.queue_delete(
				queue = authenticate_login.username
				)		



	# Function to get user details
	def get_user_details():
		return authenticate_login.client_id, authenticate_login.username