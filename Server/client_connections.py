import pika
import sys
import time
import json
import threading
from database_management import client_authentication, submissions_management, previous_data, query_management
from client_submissions import submission
from client_broadcasts import broadcast_manager
from init_server import initialize_server
 

class manage_clients():
	channel = ''
	data_changed_flags = ''

	def prepare(data_changed_flags2, data_from_interface):
		manage_clients.data_changed_flags = data_changed_flags2
		
		config = initialize_server.read_config()
		superuser_username = config["Server Username"]
		superuser_password = config["Server Password"]
		judge_username = config["Judge Username"]
		judge_password = config["Judge Password"]
		host = config["Server IP"]

		broadcast_thread = threading.Thread(target = broadcast_manager.init_broadcast, args = (data_changed_flags2, data_from_interface, superuser_username, superuser_password, host, ))
		broadcast_thread.start()

		

		try:
			creds = pika.PlainCredentials(superuser_username, superuser_password)
			params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
			connection = pika.BlockingConnection(params)


			#connection = pika.BlockingConnection(pika.URLParameters('amqp://' + superuser_username + ':' + superuser_password + '@' + host + '/%2f'))
			channel = connection.channel()
			manage_clients.channel = channel
			channel.exchange_declare(exchange = 'connection_manager', exchange_type = 'direct', durable = True)
			channel.exchange_declare(exchange = 'broadcast_manager', exchange_type = 'fanout', durable = True)

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
			previous_data.get_last_query_id()
		except:
			print('[ ERROR ] Could not fetch previous query_id')

		# Start listening to client_requests
		manage_clients.listen_clients(connection, channel, superuser_username, superuser_password, host, data_changed_flags2)
		broadcast_thread.join()

	# This function continously listens for client messages 
	def listen_clients(connection, channel, superuser_username, superuser_password, host, data_changed_flags2):
		try:
			# Clients send requests on client_requests
			# As soon as a new message is recieved, it is sent to client_message_handler for further processing
			print('[ LISTEN ] Started listening on client_requests')
			channel.basic_consume(queue = 'client_requests', on_message_callback = manage_clients.client_message_handler, auto_ack = True)
			channel.start_consuming()
		# Handle keyboard interrupt ctrl+c and terminate successfully
		except (KeyboardInterrupt, SystemExit):
			channel.stop_consuming()
			print('\n[ LISTEN ] STOPPED listening to client channel')
			connection.close()
			print('[ STOP ] Client subprocess terminated successfully!')
			manage_clients.data_changed_flags[7] = 1
			return

	# This function works on client messages and passes them on to their respective handler function
	def client_message_handler(ch, method, properties, body):
		print('\n[ PING ] Recieved a new client message...')
		# Decode the message sent by client
		client_message = str(body.decode('utf-8'))

		# JSON Parsing here
		try:
			json_data = json.loads(client_message)
			client_code = json_data["Code"]
			if client_code == 'LOGIN':
				client_username = json_data["Username"]
				client_password = json_data["Password"]
				client_id = json_data["ID"]
				client_type = json_data["Type"]

				manage_clients.client_login_handler(client_username, client_password, client_id, client_type)
			elif client_code == 'SUBMT':
				local_run_id = json_data["Local Run ID"]
				client_id = json_data["ID"]		
				problem_code = json_data["PCode"]		
				language = json_data["Language"]		
				time_stamp = json_data["Time"]		
				source_code = json_data["Source"]	

				manage_clients.client_submission_handler(client_id, local_run_id, problem_code, language, time_stamp, source_code)
			elif client_code == 'QUERY':
				client_id = json_data['Client ID']
				query = json_data['Query'][:100]

				if client_id == 'Nul':
					print('[ REJECT ] Client has not logged in.')
					return

				manage_clients.client_query_handler(client_id, query)
			else:
				print('[ ERROR ] Client sent garbage data. Trust me you don\'t wanna see it! ')
				# Raise Security Exception maybe?

		except Exception as error:
			print("[ ERROR ] Client json data could not be parsed : "  + str(error))
		return

	# This function handles all client login requests
	def client_login_handler(client_username, client_password, client_id, client_type):
		# Client sends the username, password, clientID as 'username+password+clientID', so we split it.
		# Default value of clientID is 'Null' (String)
		message = ''
		print('[ LOGIN REQUEST ] ::: ' + str(client_id) + ' :::' + client_username + '@' + client_password + '[ TYPE ] ' + client_type)

		# Declare queue with same name as client_username
		manage_clients.channel.queue_declare(queue = client_username, durable = True)
		#Bind the connection_manager exchange to client queue (que name is same as username)
		manage_clients.channel.queue_bind(exchange = 'connection_manager', queue = client_username)
		manage_clients.channel.queue_bind(exchange = 'broadcast_manager', queue = client_username)

		if client_type == 'CLIENT':
			# If client logins have been halted by the Admin, Send a rejection message to the client
			if(manage_clients.data_changed_flags[2] == 0):
				print('[ LOGIN ][ REJECT ] Rejected by ADMIN')
				message = {
				'Code' : 'LRJCT',
				'Message' : 'Logins are not allowed right now.\nPlease wait for announcement.'
				}
				message = json.dumps(message)
				response.publish_message(manage_clients.channel, client_username, message)
				return
			

			# The client listens on its own queue, whose name = client_username (Hard-coded)
			# This queue is declared in the ../Client/client.py file
			# Every response sent to client has 5 initial characters which specify what server is going to talk about.
			# 'VALID' signifies a VALID login.
			# 'INVLD' signifies an INVaLiD login attempt.
			# 'LRJCT' signifies a Login ReJeCTed message.

			# Validate the client from the database
			status = client_authentication.validate_client(client_username, client_password)
			# If login is successful:
			if status == True:
				# Check if client has logged in for the first time or is already connected:
				previously_connected_state = client_authentication.check_connected_client(client_username, 'connected_clients')
				# If client has NOT logged in for the first time
				# MAYBE A SECURITY EVENT?
				# Raise a confirmation box to ADMIN maybe?
				if previously_connected_state == 'Connected':
					client_id = client_authentication.get_client_id(client_username)
					print('[ LOGIN ][ ' + client_username + ' ][ REJECT ] Previous Client ID : ' + str(client_id) )
					# Reject client login
					message = {
					'Code' : 'LRJCT',
					'Message' : 'Maximum Login limit is 1 per user.'
					}
					message = json.dumps(message)

					# Raise a security event?


				# If client has logged in for the first time
				elif previously_connected_state == 'New':
					# Fetch new client ID
					client_id = client_authentication.generate_new_client_id()
					# Add client to connected users database
					client_authentication.add_client(client_id, client_username, client_password, 'Connected', 'connected_clients')
					print('[ LOGIN ][ ' + client_username + ' ] Assigned : ' + str(client_id) )

					# Update GUI to indicate new data
					manage_clients.data_changed_flags[1] = 1

					# Reply to be sent to client
					server_message = 'Hello_buddy!!'
					
					message = {
					'Code' : 'VALID', 
					'Client ID' : client_id, 
					'Message' : server_message
					}
					message = json.dumps(message)

					print('[ LOGIN ][ SENT ] VALID to ' + client_username)
					
					# Check if contest has started, also send client the 
					# contest START signal alog with remaining time.

				elif previously_connected_state == 'Deleted':
					print('[ LOGIN ][ ' + client_username + ' ][ REJECT ] Blocked LOGIN attempt')
					# Reject client login
					message = {
					'Code' : 'LRJCT',
					'Message' : 'You are blocked from the contest!\nPlease contact ADMIN.'
					}
					message = json.dumps(message)


			# If login is not successful:
			elif status == False:
				print('[ ' + client_username + ' ][ REJECT ] NOT verified.')
				message = {
				'Code' : 'INVLD'
				}
				message = json.dumps(message)
				# Reply 'Invalid credentials' to client


			# Send response to client

			response.publish_message(manage_clients.channel, client_username, message)


		# Judge login is handled as a client to avoid redundancy in code
		elif client_type == 'JUDGE':
			if(manage_clients.data_changed_flags[12] == 0):
				print('[ LOGIN ][ REJECT ] Rejected by ADMIN')
				message = {
				'Code' : 'LRJCT',
				'Message' : 'Judge Logins are not allowed right now.'
				}
				message = json.dumps(message)
				response.publish_message(manage_clients.channel, client_username, message)
				return
			# IN ALL REGARDS, CLIENT HERE MEANS A judge_manager
			status = client_authentication.validate_client(client_username, client_password)

			#Bind the connection_manager exchange to client queue (queue name is same as username)
			manage_clients.channel.queue_bind(exchange = 'judge_manager', queue = client_username)
			# If login is successful:
			if status == True:
				# Check if client has logged in for the first time or is already connected:
				previously_connected_state = client_authentication.check_connected_client(client_username, 'connected_judges')
				if previously_connected_state == 'Connected':
					print('[ LOGIN ][ ' + client_username + ' ][ RE-LOGIN ]')
					server_message = 'Gotta work harder, Judge :)'
					
					message = {
					'Code' : 'VALID', 
					'Client ID' : 0, 
					'Message' : server_message
					}
					message = json.dumps(message)
					# Raise a security notification?

				# If client has logged in for the first time
				elif previously_connected_state == 'New':
					# Add client to connected users database
					client_authentication.add_client('__JUDGE__', client_username, client_password, 'Connected', 'connected_judges')
					print('[ LOGIN ][ ' + client_username + ' ][ JUDGE ][ VALID ] Sending response...')

					# Update GUI to indicate new data
					#manage_clients.data_changed_flags[1] = 1

					# Reply to be sent to client
					server_message = 'Hello Judge!'
					
					message = {
					'Code' : 'VALID', 
					'Client ID' : '__JUDGE__', 
					'Message' : server_message
					}
					message = json.dumps(message)
					
				elif previously_connected_state == 'Deleted':
					print('[ LOGIN ][ ' + client_username + ' ][ REJECT ] Blocked LOGIN attempt')
					# Reject client login
					message = {
					'Code' : 'LRJCT',
					'Message' : 'You are blocked from the contest!\nPlease contact ADMIN.'
					}
					message = json.dumps(message)

				# Update JUDGE view
				manage_clients.data_changed_flags[13] = 1
				
			# If login is not successful:
			elif status == False:
				print('[ LOGIN ] Judge NOT verified.')
				message = {
				'Code' : 'INVLD'
				}
				message = json.dumps(message)
				print('[ SENT ] INVLD to' + client_username)
				# Reply 'Invalid credentials' to client

			response.publish_message(manage_clients.channel, client_username, message)
		return


	def client_submission_handler(client_id, local_run_id, problem_code, language, time_stamp, source_code):
		print('[ SUBMISSION ] Client ID :' + str(client_id) + ' Problem:' + problem_code + ' Language :' + language + ' Time stamp :' + time_stamp)

		# Get client username from database
		# TO BE OPTIMISED LATER
		client_username = client_authentication.get_client_username(client_id)
		if client_username == 'Null':
			print('[ REJECT ] Client status is NOT CONNECTED. This should not happen! Please check for malicious client.')
			return

		# If no new submissions are allowed
		if(manage_clients.data_changed_flags[3] == 0):
			print('[ SUBMISSION ] Rejected by ADMIN')
			# Send SRJCT : SubmissionReject
			message = {
				'Code' : 'SRJCT'
				}
			message = json.dumps(message)
			try:
				response.publish_message(manage_clients.channel, client_username, message)
			except Exception as error:
				print('[ ERROR ][ SECURITY ] Client has no username so could not send error code.' )
			return

		#TODO Check client status, and accept only if it is CONNECTED and not BLOCKED or NEW




		


		try:
			if client_id == 'Nul':
				print('[ REJECT ][ SECURITY ] Client has not logged in. Please check the client for ambiguity.')

			else:
				run_id, source_file_name = submission.new_submission(client_id, problem_code, language, time_stamp, source_code)
				# Update database
				status = 'Running'
				
				submissions_management.insert_submission(run_id, local_run_id, client_id, language, source_file_name, problem_code, status, time_stamp)
				manage_clients.data_changed_flags[0] = 1
				
				# Push the submission in judging queue
				print('[ JUDGE ] Requesting a new judgement')
				manage_clients.send_new_request(client_id, client_username, run_id, local_run_id, problem_code, language, source_code)
				#######################################################################
				
		except Exception as error:
			print('[ ERROR ] Client submisssion could not be processed : ' + str(error))

		return

	def client_query_handler(client_id, query):
		print('[ QUERY ] From ' + str(client_id) + ' : ' + query)
		query_id = query_management.generate_new_query_id() 
		query_management.insert_query(query_id, client_id, query)
		manage_clients.data_changed_flags[9] = 1



	def send_new_request(client_id, client_username, run_id, local_run_id, p_code, language, source_code):
		message = {
		'Code' : 'JUDGE', 
		'Client ID' : client_id, 
		'Client Username' : client_username,
		'Run ID' : run_id,
		'Language' : language,
		'PCode' : p_code,
		'Source' : source_code,
		'Local Run ID' : local_run_id
		}
	
		message = json.dumps(message)

		manage_clients.channel.basic_publish(exchange = 'connection_manager', routing_key = 'judge_requests', body = message, properties = pika.BasicProperties(delivery_mode = 2)) 
		print('[ REQUEST ] New judging request sent')
		return

class response():
	def publish_message(channel, queue_name, message):
		#message is in json format
		print( '[ PUBLISH ] new message TO ' + queue_name)
		try:
			channel.basic_publish(exchange = 'connection_manager', routing_key = queue_name, body = message)
		except Exception as error:
			print('[ CRITICAL ] Could not publish message : ' + str(error))
		return