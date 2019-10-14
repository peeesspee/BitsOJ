from connection import manage_connection
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
		# while True:
		# 	if pika.exceptions.UnroutableError:
		# 		break;
		# 	else:
		# 		print('try again')
		# Started listening
		authenticate_login.channel.start_consuming()
		# while channel._consumer_infos:
			# channel.connection.process_data_events(time_limit=15) # 2 Seconds

		

	def server_response_handler(ch,method,properties,body):
		# Decoding the data 
		json_data = str(body.decode('utf-8'))
		server_data = json.loads(json_data)

		# Extracting the status whether valid or invalid 
		status = server_data['Code']

		print("[ STATUS ] " + status)
		if (status == 'VALID'):
			print('[ ClientID ] receiving ......')
			with open('config.json', 'r') as read_config:
				config = json.load(read_config)

			config["client_id"] = server_data["Client ID"]
			with open('config.json', 'w') as read_config:
				json.dump(config, read_config, indent = 4) 
			with open('client_data.json', 'w') as data:
				json.dump(server_data, data, indent=4)

			print("[ Status ] " + status + "\n[ ClientID ] : " + server_data["Client ID"] + "\n[ Server ] : " + server_data["Message"])
			
			# Changing login status to valid
			authenticate_login.login_status = 'VALID'
			authenticate_login.client_id = server_data["Client ID"]
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
			authenticate_login.login_status = 'LRJCT'
			# Deleting the queue on which the client is listening
			authenticate_login.channel.queue_delete(
				queue = authenticate_login.username
				)		


	# Function to get user details
	def get_user_details():
		return authenticate_login.client_id, authenticate_login.username