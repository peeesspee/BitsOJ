import pika
import sys
import time
from database_management import client_authentication, submissions_management, previous_data
from client_submissions import submission

class manage_clients():
	channel = ''
	data_changed_flags = ''
	# This function continously listens for client messages 
	def listen_clients(superuser_username, superuser_password, host, data_changed_flags2):
		manage_clients.data_changed_flags = data_changed_flags2

		try:
			connection = pika.BlockingConnection(pika.URLParameters('amqp://' + superuser_username + ':' + superuser_password + '@' + host + '/%2f'))
			channel = connection.channel()
			manage_clients.channel = channel
			channel.exchange_declare(exchange = 'connection_manager', exchange_type = 'direct', durable = True)
			#channel.exchange_declare(exchange = 'client_broadcasts', exchange_type = '')
			channel.queue_declare(queue = 'client_requests', durable = True)
			channel.queue_declare(queue = 'judge_requests', durable = True)
			channel.queue_bind(exchange = 'connection_manager', queue = 'client_requests')
			channel.queue_bind(exchange = 'connection_manager', queue = 'judge_requests')

			# Initialize run_id counter from database
		except Exception as error:
			print('[ CRITICAL ] Could not connect to RabbitMQ server : ' + str(error))
			sys.exit()

		try:
			submission.init_run_id()
		except:
			print('[ ERROR ] Could not fetch previous run_id')

		try:
			previous_data.get_last_client_id()
		except:
			print('[ ERROR ] Could not fetch previous client_id')

		try:
			# Clients send requests on client_requests
			# As soon as a new message is recieved, it is sent to client_message_handler for further processing
			print('[ LISTEN ] Started listening on client_requests')
			channel.basic_consume(queue = 'client_requests', on_message_callback = manage_clients.client_message_handler, auto_ack = True)
			channel.start_consuming()
		# Handle keyboard interrupt ctrl+c and terminate successfully
		except (KeyboardInterrupt, SystemExit):
			channel.stop_consuming()
			print('[ LISTEN ] STOPPED listening to client channel')
			connection.close()
			print('[ STOP ] Client subprocess terminated successfully!')
		
			return

	# This function works on client messages and passes them on to their respective handler function
	def client_message_handler(ch, method, properties, body):
		# Decode the message sent by client
		# First 5 characters contain metadata
		client_message = str(body.decode('utf-8'))
		
		print('\n[ PING ] Recieved a new client message...')
		client_code = client_message[0:6]
		if client_code == 'LOGIN ':
			manage_clients.client_login_handler(client_message[6:])
		elif client_code == 'SUBMT ':
			manage_clients.client_submission_handler(client_message[6:])
		else:
			print('[ ERROR ] Client sent garbage data. Trust me you don\'t wanna see it! ')

		return

	# This function handles all client login requests
	def client_login_handler(client_message):
		# Client sends the username, password, clientID as 'username+password+clientID', so we split it.
		# Default value of clientID is 'Null' (String)
		try:
			client_username, client_password, client_id, client_type = client_message.split(' ')
		except Exception as error:
			print('[ ERROR ] Client data parsing error : ' + str(error))
			print('[ DEBUG ] Client message was : ' + str(client_message))

		print('[ LOGIN ] ' + client_username + '@' + client_password + '[ TYPE ] ' + client_type)

		if client_type == 'CLIENT':
			# If client logins have been halted by the Admin, Send a rejection message to the client
			if(manage_clients.data_changed_flags[2] == 0):
				print('[ LOGIN ] Rejected by ADMIN')
				message = 'LRJCT'
				manage_clients.publish_message(client_username, message)
				return
			# Validate the client from the database
			status = client_authentication.validate_client(client_username, client_password)

			#Bind the connection_manager exchange to client queue (que name is same as username)
			manage_clients.channel.queue_bind(exchange = 'connection_manager', queue = client_username)

			# The client listens on its own queue, whose name = client_username (Hard-coded)
			# This queue is declared in the ../Client/client.py file
			# Every response sent to client has 5 initial characters which specify what server is going to talk about.
			# 'VALID' signifies a valid login.
			# 'INVLD' signifies an invalid login attempt.

			# If login is successful:
			if status == True:
				# Check if client has logged in for the first time:
				previously_connected_status = client_authentication.check_connected_client(client_username)
				# If client has NOT logged in for the first time
				if previously_connected_status == True:
					client_id = client_authentication.get_client_id(client_username)
					print('[ ' + client_username + ' ] Previous Client ID : ' + client_id )

				# If client has logged in for the first time
				else:
					# Fetch new client ID
					client_id = client_authentication.generate_new_client_id()
					# Add client to connected users list
					client_authentication.add_connected_client(client_id, client_username, client_password)
					print('[ ' + client_username + ' ] Assigned : ' + client_id )

				# Update GUI to indicate new data
				manage_clients.data_changed_flags[1] = 1

				# Reply to be sent to client
				server_message = 'Hello_buddy!!'
				message = 'VALID+' +  client_id + '+' + server_message
				print('[ SENT ] ' + message)

				# Send login_successful signal to client. 
				manage_clients.publish_message(client_username, message)
				
			# If login is not successful:
			elif status == False:
				print('[ ' + client_username + ' ] NOT verified.')
				message = 'INVLD'
				# Reply 'Invalid credentials' to client
				manage_clients.publish_message(client_username, message)


		# Judge login is handled as a client to avoid redundancy in code
		elif client_type == 'JUDGE':
			# IN ALL REGARDS, CLIENT HERE MEANS A judge_manager
			status = client_authentication.validate_client(client_username, client_password)

			#Bind the connection_manager exchange to client queue (queue name is same as username)
			manage_clients.channel.queue_bind(exchange = 'judge_manager', queue = client_username)

			# If login is successful:
			if status == True:
				print('[ LOGIN ] Judge login successful : ' + client_username )
				message = 'VALID'
				print('[ SENT ] ' + message + ' to ' + client_username)
				# Send login_successful signal to client. 
				manage_clients.publish_message(client_username, message)
				
			# If login is not successful:
			elif status == False:
				print('[ LOGIN ] Judge NOT verified.')
				message = 'INVLD'
				print('[ SENT ] ' + message + ' to ' + client_username)
				# Reply 'Invalid credentials' to client
				manage_clients.publish_message(client_username, message)

		return


	def client_submission_handler(client_data):
		try:
			client_id = client_data[0:3]		# client_id is 3 characters 
			problem_code = client_data[4:8]		# problem_code is 4 characters
			language = client_data[9:12]		# language is 3 characters
			time_stamp = client_data[13:21]		# time_stamp is 8 characters: HH:MM:SS
			source_code = client_data[22:]		# rest of the message is source code
			print('[ SUBMISSION ] Client ID :' + client_id + ' Problem:' + problem_code + ' Language :' + language + ' Time stamp :' + time_stamp)

		except Exception as error:
			print('[ ERROR ] Client data parsing error : ' + str(error))

		# Get client username from database
		# TO BE OPTIMISED LATER
		client_username = client_authentication.get_client_username(client_id)
		if client_username == '':
			return

		# If no new submissions are allowed
		if(manage_clients.data_changed_flags[3] == 0):
			print('[ SUBMISSION ] Rejected by ADMIN')
			# Send SRJCT : SubmissionReject
			message = 'SRJCT'
			try:
				manage_clients.publish_message(client_username, message)
			except Exception as error:
				print('[ ERROR ] Client has no username so could not send error code.' )
			return

		try:
			if client_id == 'Nul':
				print('[ REJECT ] Client has not logged in. This should not happen, please check the client for ambiguity.')

			else:
				run_id, source_file_name = submission.new_submission(client_id, problem_code, language, time_stamp, source_code)
				# Update database
				status = 'Running'
				submissions_management.insert_submission(run_id, client_id, language, source_file_name, problem_code, status, time_stamp)
				manage_clients.data_changed_flags[0] = 1
				
				# Push the submission in judging queue
				print('[ JUDGE ] Requesting a new judgement')
				manage_clients.send_new_request(run_id, problem_code, language, source_code)
				#######################################################################
				# Simulate a new judgement
				time.sleep(2)
				

		except Exception as error:
			print('[ ERROR ] Client submisssion could not be processed : ' + str(error))

		return


	def publish_message(queue_name, message):
		print( '[ PUBLISH ] ' + message + ' TO ' + queue_name)
		try:
			manage_clients.channel.basic_publish(exchange = 'connection_manager', routing_key = queue_name, body = message)
		except Exception as error:
			print('[ CRITICAL ] Could not publish messages : ' + str(error))
		return


	def send_new_request(run_id, p_code, language, source_code):
		message = 'JUDGE+' + run_id + '+' + p_code + '+' + language + '+' + source_code
		manage_clients.channel.basic_publish(exchange = 'connection_manager', routing_key = 'judge_requests', body = message) 
		print('[ REQUEST ] New judging request sent')
		return