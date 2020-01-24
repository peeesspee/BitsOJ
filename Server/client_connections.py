import pika
import sys
import time
import json
import threading
import re # For RegEx : To check IP address validity
from database_management import *
from client_submissions import submission
from init_server import initialize_server

class manage_clients():
	channel = ''
	data_changed_flags = ''
	task_queue = ''
	key = ''
	judge_key = ''
	config = ''
	file_password = ''
	already_read = 0
	codes = ''
	languages = ''
		
	def prepare(data_changed_flags, task_queue, log_queue):
		manage_clients.data_changed_flags = data_changed_flags
		manage_clients.task_queue = task_queue
		manage_clients.log_queue = log_queue
		manage_clients.config = initialize_server.read_config()
		manage_clients.codes = manage_clients.config['Problem Codes']
		manage_clients.languages = manage_clients.config['Languages']
		superuser_username = manage_clients.config["Server Username"]
		superuser_password = manage_clients.config["Server Password"]
		judge_username = manage_clients.config["Judge Username"]
		judge_password = manage_clients.config["Judge Password"]
		host = manage_clients.config["Server IP"]
		manage_clients.key = manage_clients.config["Client Key"]
		manage_clients.judge_key = manage_clients.config["Judge Key"]
		manage_clients.file_password = manage_clients.config["File Password"]
		print('  [ START ] Client Manager subprocess started.')
		manage_clients.log('  [ START ] Client Manager subprocess started.')
		try:
			creds = pika.PlainCredentials(superuser_username, superuser_password)
			params = pika.ConnectionParameters(
				host = host, 
				credentials = creds, 
				heartbeat=0, 
				blocked_connection_timeout=0
			)
			connection = pika.BlockingConnection(params)

			channel = connection.channel()
			manage_clients.channel = channel
			channel.exchange_declare(
				exchange = 'connection_manager', 
				exchange_type = 'direct', 
				durable = True
			)
			channel.exchange_declare(
				exchange = 'broadcast_manager', 
				exchange_type = 'fanout', 
				durable = True
			)

			channel.queue_declare(queue = 'client_requests', durable = True)
			channel.queue_declare(queue = 'judge_requests', durable = True)

			channel.queue_bind(exchange = 'connection_manager', queue = 'client_requests')
			channel.queue_bind(exchange = 'connection_manager', queue = 'judge_requests')

			# Initialize run_id counter from database
		except Exception as error:
			print('[ CRITICAL ] Could not connect to RabbitMQ server : ' + str(error))
			manage_clients.log('[ CRITICAL ] Could not connect to RabbitMQ server : ' + str(error))
			# Wait until gui is closed!
			# Inform GUI thread
			manage_clients.data_changed_flags[26] = 1
			while manage_clients.data_changed_flags[7] !=1:
				time.sleep(0.5)
			sys.exit()

		try:
			previous_data.get_last_client_id()
		except:
			print('[ ERROR ] Could not fetch previous client_id')
			manage_clients.log('[ ERROR ] Could not fetch previous client_id')

		# Start listening to client_requests
		manage_clients.listen_clients(connection, channel, superuser_username, superuser_password, host)

	def log(message):
		manage_clients.log_queue.put(message)

	# This function continously listens for client messages 
	def listen_clients(connection, channel, superuser_username, superuser_password, host):
		try:
			# Clients send requests on client_requests
			# As soon as a new message is recieved, it is sent to client_message_handler for further processing
			print('[ LISTEN ] Started listening on client_requests')
			manage_clients.log('[ LISTEN ] Started listening on client_requests')
			channel.basic_consume(
				queue = 'client_requests', 
				on_message_callback = manage_clients.client_message_handler,
				exclusive = True, 		# Only server can listen to this queue
				auto_ack = False
			)
			channel.start_consuming()
		# Handle keyboard interrupt ctrl+c and terminate successfully
		except (KeyboardInterrupt, SystemExit):
			channel.stop_consuming()
			print('[ LISTEN ] STOPPED listening to client channel')
			manage_clients.log('[ LISTEN ] STOPPED listening to client channel')
			
		except (pika.exceptions.ChannelWrongStateError):
			print('[ ERROR ] : Channel closed by Broker. Please restart')
			manage_clients.log('[ ERROR ] : Channel closed by Broker')

		except (pika.exceptions.ChannelClosedByBroker):
			print( 
				'[ ERROR ] : Could not get a lock on client_requests.' +
				' Please check management portal and remove any consumers from the queue'
			)
			manage_clients.log(
				'[ ERROR ] : Could not get a lock on client_requests.' +
				'Please check management portal and remove any consumers from the queue'
			)
		except Exception as error: 
			print('[ CLIENT PROCESS ][ CRITICAL ]: ' + str(error))
			manage_clients.log('[ CLIENT PROCESS ][ CRITICAL ]: ' + str(error))

		finally: 
			manage_clients.data_changed_flags[7] = 1
			connection.close()
			print('[ STOP ] Client subprocess terminated successfully!')
			manage_clients.log('[ STOP ] Client subprocess terminated successfully!')
			return
		
	# This function works on client messages and passes them on to their respective handler function
	def client_message_handler(ch, method, properties, body):
		print('[ ALERT ] Recieved a new client message.')
		manage_clients.log('[ ALERT ] Recieved a new client message.')
		
		try:
			# Decode the message sent by client
			client_message = str(body.decode('utf-8'))
			# JSON Parsing here 
			json_data = json.loads(client_message)
			# Validate Client Key( Make sure client is authentic! )
			client_key = json_data.get("Client Key")
			client_code = json_data.get("Code")
			client_ip = json_data.get("IP")

			if client_key == None or client_code == None or client_ip == None:
				print('[ SECURITY ] Client data is not in the correct format.')
				manage_clients.log('[ SECURITY ] Client data is not in the correct format.')
				print('[ SECURITY ] Complete Message: ' + client_message)
				manage_clients.log('[ SECURITY ] Complete Message: ' + client_message)
				ch.basic_ack(delivery_tag = method.delivery_tag)
				return

			# Strip IP address of spaces
			client_ip = client_ip.replace(' ', '')

			if  client_key != manage_clients.key and client_key != manage_clients.judge_key :
				print('[ SECURITY ] Client Key did not match. Client ID: ' + str(json_data['ID']))
				manage_clients.log('[ SECURITY ] Client Key did not match. Client ID: ' + str(json_data['ID']))
				print('[ SECURITY ] Complete Message: ' + client_message)
				manage_clients.log('[ SECURITY ] Complete Message: ' + client_message)
				ch.basic_ack(delivery_tag = method.delivery_tag)
				return

			if client_code == 'LOGIN':
				client_username = json_data.get("Username", 'NONE')
				client_password = json_data.get("Password", 'NONE')
				client_id = json_data.get("ID", 'NONE')
				client_type = json_data.get("Type", 'NONE')
				manage_clients.client_login_handler(
					client_key,
					client_username, 
					client_password, 
					client_id, 
					client_type,
					client_ip
				)

			elif client_code == 'SUBMT':
				# recieved_client_username = json_data["Username"]
				local_run_id = json_data.get("Local Run ID", 'NONE')
				client_id = json_data.get("ID", 'NONE')
				problem_code = json_data.get("PCode", 'NONE')
				language = json_data.get("Language", 'NONE')
				time_stamp = json_data.get("Time", 'NONE')
				source_code = json_data.get("Source", 'NONE')
				username = json_data.get("Username", 'NONE')
				manage_clients.client_submission_handler(
					client_id,
					client_ip,
					username,
					local_run_id, 
					problem_code, 
					language, 
					time_stamp, 
					source_code
				)
			elif client_code == 'QUERY':
				client_id = json_data.get('ID', "NONE")
				query = json_data.get('Query', "NONE")
				username = json_data.get('Username', "NONE")
				query = query[:100]

				if client_id == 'NONE' or client_id == "Nul":
					print('[ REJECT ] Client has not logged in.')
					manage_clients.log('[ REJECT ] Client has not logged in.')
					return

				manage_clients.client_query_handler(
					client_id, 
					username,
					query
				)

			elif client_code == 'DSCNT':
				client_username = json_data.get("Username", "NONE")
				client_id = json_data.get("ID", "NONE")
				manage_clients.client_logout_handler(
					client_username, 
					client_id,
					client_ip
				)
			else:
				print('[ CODE ERROR ] Client sent wrong code. Complete Message: ' + client_message)
				manage_clients.log('[ CODE ERROR ] Client sent wrong code. Complete Message: ' + client_message)
				# Raise Security Exception maybe?
		except Exception as error:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			# print(exc_type, fname, )
			print('[ ERROR ] Client sent unparsable data. Line: ' + str(exc_tb.tb_lineno) + ' Complete Message: ' + client_message + "\nError: " + str(error))
			manage_clients.log('[ ERROR ] Client sent unparsable data. Line: ' + str(exc_tb.tb_lineno) + ' Complete Message: ' + client_message + "\nError: " + str(error))
		# Acknowledge the message
		ch.basic_ack(delivery_tag = method.delivery_tag)
		return
	
	# This function handles all client login requests
	def client_login_handler(
			client_key, 
			client_username, 
			client_password, 
			client_id, 
			client_type, 
			client_ip = '0.0.0.0'
		):
		if (
				client_type == 'CLIENT' and 
				client_key != manage_clients.key or 
				client_type == 'JUDGE' and 
				client_key != manage_clients.judge_key
			):
			# REJECT
			message = {
					'Code' : 'LRJCT',
					'Receiver' : client_username,
					'Message' : 'You are using an incompatible client.\nPlease contact ADMIN. '
				}
			message = json.dumps(message)
			manage_clients.task_queue.put(message)
			return
			
		message = ''
		print(
			'[ LOGIN REQUEST ] ::: ' + 
			str(client_id) + 
			' :::' + 
			client_username + 
			'@' + client_password + 
			'[ TYPE ] ' + 
			client_type + 
			' IP: ' + 
			client_ip
		)
		manage_clients.log(
			'[ LOGIN REQUEST ] ::: ' + 
			str(client_id) + 
			' :::' + 
			client_username + 
			'@' + 
			client_password + 
			'[ TYPE ] ' + 
			client_type + 
			' IP: ' + 
			client_ip
		)

		try:
			# Declare queue with same name as client_username
			manage_clients.channel.queue_declare(queue = client_username, durable = True)
		except Exception as error:
			print('[ ERROR ][ CRITICAL ] Could not declare queues: ' + str(error))
			manage_clients.log('[ ERROR ][ CRITICAL ] Could not declare queues: ' + str(error))
			return

		try:
			#Bind the connection_manager exchange to client queue (queue name is same as username)
			manage_clients.channel.queue_bind(exchange = 'connection_manager', queue = client_username)
			manage_clients.channel.queue_bind(exchange = 'broadcast_manager', queue = client_username)
		except Exception as error:
			print('[ ERROR ][ CRITICAL ] Could not bind queues: ' + str(error))
			manage_clients.log('[ ERROR ][ CRITICAL ] Could not bind queues: '+ str(error))
			return
		
		if client_type == 'CLIENT':
			# If client logins have been halted by the ADMIN, Send a rejection message to the client
			if(manage_clients.data_changed_flags[2] == 0):
				print('[ LOGIN ][ REJECT ] Rejected by ADMIN')
				manage_clients.log('[ LOGIN ][ REJECT ] Rejected by ADMIN')
				message = {
					'Code' : 'LRJCT',
					'Receiver' : client_username,
					'Message' : 'Logins are not allowed right now.\nPlease wait for announcement.'
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				return
			

			# The client listens on its own queue, whose name = client_username (Hard-coded)
			# This queue is declared in the ../Client/client.py file
			# Every response sent to client has 5 initial characters which specify what server is going to talk about.
			# 'VALID' signifies a VALID login.
			# 'INVLD' signifies an INVaLiD login attempt.
			# 'LRJCT' signifies a Login ReJeCTed message.

			# Validate the client from the database
			status = client_authentication.validate_client(client_username, client_password)
			stored_client_id = str(client_authentication.get_client_id(client_username))
			print('[ LOGIN ] Stored client ID: ', stored_client_id)
			if stored_client_id != client_id and stored_client_id != str(-1):
				print('[ ' + client_username + ' ] Client ID does not match.')
				manage_clients.log('[ ' + client_username + ' ] Client ID does not match.')
				status = False

			# If login is successful:
			if status != True:
				# Reply 'Invalid credentials' to client
				print('[ ' + client_username + ' ][ REJECT ] NOT verified.')
				manage_clients.log('[ ' + client_username + ' ][ REJECT ] NOT verified.')
				message = {
					'Code' : 'INVLD',
					'Receiver' : client_username
				}
				message = json.dumps(message)
				# Send response to client
				manage_clients.task_queue.put(message)
				return

			# Check if client has logged in for the first time or is already connected:
			previously_connected_state = client_authentication.check_connected_client(
				client_username, 
				'connected_clients'
			)
			# If client has NOT logged in for the first time
			# MAYBE A SECURITY EVENT?
			# Raise a confirmation box to ADMIN maybe?
			
			if previously_connected_state == 'Connected':
				print('[ LOGIN ][ ' + client_username + ' ][ REJECT ] Multiple Logins' )
				manage_clients.log('[ LOGIN ][ ' + client_username + ' ][ REJECT ] Multiple Logins' )
				# Reject client login
				message = {
					'Code' : 'LRJCT',
					'Receiver' : client_username,
					'Message' : 'Maximum Login limit is 1 per user.'
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				return

				# Raise a security event?
			elif previously_connected_state == 'Disconnected':
				if client_id == 'Null':
					# If the client has disconnected, it must have remembered its client id
					# REJECT login
					message = {
						'Code' : 'LRJCT',
						'Receiver' : client_username,
						'Message' : 'System has detected an unusual Login behavior. Please contact ADMIN.'
					}
					message = json.dumps(message)
					manage_clients.task_queue.put(message)
					return

				if manage_clients.data_changed_flags[27] == 0: 
					print('[ LOGIN ][ VALIDATION ] Checking client IP Address...')
					manage_clients.log('[ LOGIN ][ VALIDATION ] Checking client IP Address...')
					state = client_authentication.check_client_ip(client_id, client_ip)
				else:
					state  = 1

				if state == 1:
					print('[ RE-LOGIN ][ ' + client_username + ' ][ ACCEPT ] Previous Client ID : ' + str(client_id) )
					manage_clients.log('[ RE-LOGIN ][ ' + client_username + ' ][ ACCEPT ] Previous Client ID : ' + str(client_id) )
				
					message = {
						'Code' : 'VALID',
						'Receiver' : client_username,
						'Client ID' : client_id, 
						'Message' : 'Welcome back!.'
					}
					message = json.dumps(message)
					manage_clients.task_queue.put(message) 

					# Update client state from Disconnected to Connected 
					message = {
						'Code' : 'UpUserStat', 
						'Username' : client_username,
						'State' : 'Connected',
						'IP' : client_ip
					}
					message = json.dumps(message)
					manage_clients.task_queue.put(message)

					return
	
				else:
					print('[ RE-LOGIN ][ ' + client_username + ' ][ REJECT ] IP validation failed')
					manage_clients.log('[ RE-LOGIN ][ ' + client_username + ' ][ REJECT ] IP validation failed')
					message = {
						'Code' : 'LRJCT',
						'Receiver' : client_username,
						'Client ID' : client_id, 
						'Message' : 'Preliminary Validation Failed. Contact site ADMIN for more information.'
					}
					message = json.dumps(message)
					manage_clients.task_queue.put(message)
					return

			# If client has logged in for the first time
			elif previously_connected_state == 'New':
				# Check for IP address Duplicacy
				if manage_clients.data_changed_flags[14] == 1:
					status = client_authentication.check_duplicate_ip(client_ip)
					if status == 0:
						# Unique IP
						print('[ LOGIN ] IP duplicacy : None')
						manage_clients.log('[ LOGIN ] IP duplicacy : None')
						pass
					elif status == 1:
						# Duplicate IP address
						print('[ LOGIN ][ REJECT] Duplicate IP Address.')
						manage_clients.log('[ LOGIN ][ REJECT] Duplicate IP Address.')
						message = {
							'Code' : 'LRJCT',
							'Receiver' : client_username,
							'Client ID' : client_id, 
							'Message' : 'Multiple logins with same PC are not allowed.'
						}
						message = json.dumps(message)
						manage_clients.task_queue.put(message)
						return
					else:
						print('[ CLIENT ] Error while checking for client IP address.')
						manage_clients.log('[ CLIENT ] Error while checking for client IP address.')
			
				# Fetch new client ID
				client_id = client_authentication.generate_new_client_id()
				# Add client to connected users database
				message = {
					'Code' : 'AddNewUser', 
					'Username' : client_username,
					'State' : 'Connected',
					'IP' : client_ip,
					'ID' : client_id,
					'Password' : client_password,
					'Table' : 'connected_clients'
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)

				message = {
					'Code' : 'AddNewScore', 
					'Username' : client_username,
					'ID' : client_id,
					'Score' : 0,
					'Problems Solved' : 0,
					'Total Time' : '00:00:00'
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)

				print('[ LOGIN ][ ' + client_username + ' ] Assigned : ' + str(client_id) )
				manage_clients.log('[ LOGIN ][ ' + client_username + ' ] Assigned : ' + str(client_id) )

				# Reply to be sent to client
				server_message = 'BitsOJ V1.0: Validation Successful.'
				
				message = {
					'Code' : 'VALID', 
					'Receiver' : client_username,
					'Client ID' : client_id, 
					'Message' : server_message
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				print('[ LOGIN ][ RESPONSE ] VALID to ' + client_username)
				manage_clients.log('[ LOGIN ][ RESPONSE ] VALID to ' + client_username)

				# Check if contest has started, also send client the 
				# START signal for contest
				if manage_clients.data_changed_flags[10] == 1:
					# Update self config
					manage_clients.config = initialize_server.read_config()
					total_time = manage_clients.config['Contest Set Time']
					start_time = initialize_server.get_start_time()
					end_time = initialize_server.get_end_time()

					current_time = time.time()
					time_difference = total_time - current_time
					remaining_time = time.strftime('%H:%M:%S', time.gmtime(time_difference))

					message = {
						'Code' : 'START', 
						'Receiver' : client_username,
						'Duration' : remaining_time,
						'Start Time' : start_time,
						'End Time' : end_time,
						'Problem Key' : manage_clients.file_password
					}
					message = json.dumps(message)
					manage_clients.task_queue.put(message)
					print('[ LOGIN ][ RESPONSE ] Sent START to ' + client_username)
					manage_clients.log('[ LOGIN ][ RESPONSE ] Sent START to ' + client_username)

				return
					
			elif previously_connected_state == 'Blocked':
				print('[ LOGIN ][ ' + client_username + ' ][ REJECT ] Blocked LOGIN attempt')
				manage_clients.log('[ LOGIN ][ ' + client_username + ' ][ REJECT ] Blocked LOGIN attempt')
				# Reject client login
				message = {
					'Code' : 'LRJCT',
					'Receiver' : client_username,
					'Message' : 'You are blocked from the contest!\nPlease contact ADMIN.'
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				return
		########################################################################################################################
		# Judge login is handled as a client to avoid redundancy in code
		elif client_type == 'JUDGE':
			if(manage_clients.data_changed_flags[12] == 0):
				print('[ LOGIN ][ REJECT ] Rejected by ADMIN')
				manage_clients.log('[ LOGIN ][ REJECT ] Rejected by ADMIN')
				message = {
					'Code' : 'LRJCT',
					'Receiver' : client_username,
					'Message' : 'Judge Logins are not allowed right now.'
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				return

			# IN ALL REGARDS, CLIENT HERE MEANS A JUDGE
			status = client_authentication.validate_client(client_username, client_password)

			
			# If login is not successful:
			if status != True:
				print('[ LOGIN ] Judge NOT verified.')
				manage_clients.log('[ LOGIN ] Judge NOT verified.')
				message = {
					'Code' : 'INVLD',
					'Receiver' : client_username,
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				print('[ LOGIN ][ REJECT ] Sent  INVLD to ' + client_username)
				manage_clients.log('[ LOGIN ][ REJECT ] Sent  INVLD to ' + client_username)
				return

			# Check if client has logged in for the first time or is already connected:
			previously_connected_state = client_authentication.check_connected_client(client_username, 'connected_judges')

			if previously_connected_state == 'Disconnected':
				status = client_authentication.validate_connected_judge(client_username, client_id, client_ip)
				if status == False:
					print('[ LOGIN ][ ' + client_username + ' ][ RE-LOGIN ] Rejected : ID/IP mismatch')
					manage_clients.log('[ LOGIN ][ ' + client_username + ' ][ RE-LOGIN ] Rejected : ID/IP mismatch')
					message = {
						'Code' : 'LRJCT', 
						'Receiver' : client_username, 
						'ID' : client_id,
						'Message' : 'Login Rejected : IP mismatch'
					}
					message = json.dumps(message)
					manage_clients.task_queue.put(message)
					return

				# State = True here, which means a successful LOGIN
				# Update state in database ( from BitsOJCore )
				message = {
					'Code' : 'UpJudgeStat', 
					'Username' : client_username,
					'State' : 'Connected',
					'IP' : client_ip
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)

				print('[ LOGIN ][ ' + client_username + ' ][ RE-LOGIN ]')
				manage_clients.log('[ LOGIN ][ ' + client_username + ' ][ RE-LOGIN ]')
				
				server_message = 'Gotta work harder, Judge :)'
				message = {
					'Code' : 'VALID', 
					'Receiver' : client_username,
					'ID' : client_id,
					'Message' : server_message
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				return

			elif previously_connected_state == 'Connected':
				print('[ LOGIN ][ ' + client_username + ' ][ RE-LOGIN ] Rejected')
				manage_clients.log('[ LOGIN ][ ' + client_username + ' ][ RE-LOGIN ] Rejected')
				server_message = 'Rejected - Multiple logins are not allowed.'
				
				message = {
					'Code' : 'LRJCT', 
					'Receiver' : client_username, 
					'Message' : server_message
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				return

			# If client has logged in for the first time
			elif previously_connected_state == 'New':
				judge_session_key = client_authentication.generate_judge_key()
				# Add client to connected users database
				message = {
					'Code' : 'AddNewUser', 
					'Username' : client_username,
					'State' : 'Connected',
					'IP' : client_ip,
					'ID' : judge_session_key,
					'Password' : client_password,
					'Table' : 'connected_judges'
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)

				print('[ LOGIN ][ ' + client_username + ' ][ JUDGE ][ VALID ] ID: ' + str(judge_session_key))
				manage_clients.log('[ LOGIN ][ ' + client_username + ' ][ JUDGE ][ VALID ] ID: ' + str(judge_session_key))

				# Reply to be sent to judge
				server_message = 'Hello Judge!'
				
				message = {
					'Code' : 'VALID', 
					'Receiver' : client_username,
					'ID' : judge_session_key, 
					'Message' : server_message
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				return

				
			elif previously_connected_state == 'Blocked':
				print('[ LOGIN ][ ' + client_username + ' ][ REJECT ] Blocked LOGIN attempt')
				manage_clients.log('[ LOGIN ][ ' + client_username + ' ][ REJECT ] Blocked LOGIN attempt')
				# Reject client login
				message = {
					'Code' : 'LRJCT',
					'Receiver' : client_username,
					'Message' : 'You are blocked from the contest!\nPlease contact ADMIN.'
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
				return

	def validate_ip(ip):
		# This function validates wherther an ip address matches coorect pattern or not.
		# Credits: GeeksForGeeks 
		try:
			regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\\.( 
			25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\\.( 
			25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\\.( 
			25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
			if re.search(regex, ip):
				# valid IP address
				return True
			return False
		except:
			return False
		
	def client_submission_handler(
			client_id, 
			client_ip, 
			client_username, 
			local_run_id, 
			problem_code, 
			language, 
			time_stamp, 
			source_code
		):
		# This block ensures that the config read by this process is latest
		if manage_clients.already_read == 0:
			manage_clients.already_read = 1
			manage_clients.config = initialize_server.read_config()
			manage_clients.codes = manage_clients.config['Problem Codes']
			manage_clients.languages = manage_clients.config['Languages']

		text = (
			'[ SUBMISSION ] Client ID :' + 
			str(client_id) + 
			' IP:' + 
			client_ip + 
			' Username: ' + 
			client_username + 
			' Problem:' + 
			problem_code + 
			' Language :' + 
			language + 
			' Time stamp :' + 
			time_stamp
		)

		print(text)
		manage_clients.log(text)
			
		contest_start_time = manage_clients.config['Contest Start Time']

		# Validate client submisssion datatypes:
		flag = 0
		if len(str(client_id)) > 10 or len(client_username) > 20 or len(str(local_run_id)) > 5 or len(problem_code) > 10 or len(language) > 10:
			print('[ SUBMISSION ][ EXCESSIVE DATA ] Validation failed!')
			manage_clients.log('[ SUBMISSION ][ EXCESSIVE DATA ] Validation failed!')
			flag = 1
		if len(time_stamp) != len('HH:MM:SS'):
			print('[ SUBMISSION ][ EXCESSIVE DATA ] Validation failed!')
			manage_clients.log('[ SUBMISSION ][ EXCESSIVE DATA ] Validation failed!')
			flag = 1
		if initialize_server.convert_to_seconds(time_stamp) == -1:
			print('[ SUBMISSION ][ Timestamp ] Validation failed!')
			manage_clients.log('[ SUBMISSION ][ Timestamp ] Validation failed!')
			flag = 1
		if manage_clients.validate_ip(client_ip) == False:
			print('[ SUBMISSION ][ IP ] Validation failed!')
			manage_clients.log('[ SUBMISSION ][ IP ] Validation failed!')
			flag = 1
		if problem_code not in manage_clients.codes:
			print('[ SUBMISSION ][ Problem Code ] Validation failed!')
			manage_clients.log('[ SUBMISSION ][ Problem Code ] Validation failed!')
			flag = 1
		if language not in manage_clients.languages:
			print('[ SUBMISSION ][ Language ] Validation failed!')
			manage_clients.log('[ SUBMISSION ][ Language ] Validation failed!')
			flag = 1
		

		if flag == 1:
			print('[ SUBMISSION ][ FAIL ] Preliminary validation Failed.')
			manage_clients.log('[ SUBMISSION ][ FAIL ] Preliminary validation Failed.')
			message = {
				'Code' : 'SRJCT',
				'Receiver' : client_username,
				'Message' : 'Your submission could not be processed! Please contact ADMIN with your problem.',
				'Local Run ID' : local_run_id
			}
			message = json.dumps(message)
			try:
				manage_clients.task_queue.put(message)
			except Exception as error:
				print('[ ERROR ][ SECURITY ] Could not send message to client: ', str(error))
				manage_clients.log('[ ERROR ][ SECURITY ] Could not send message to client: ' + str(error))
			return

		status = client_authentication.validate_connected_client(client_username, client_id, client_ip)
		if status == False:
			print('[ SUBMISSION ][ FAIL ] Client could not be Validated.')
			manage_clients.log('[ SUBMISSION ][ FAIL ] Client could not be Validated.')
			message = {
				'Code' : 'SRJCT',
				'Receiver' : client_username,
				'Message' : 'Your submission could not be processed! Validation failed.',
				'Local Run ID' : local_run_id
			}
			message = json.dumps(message)
			try:
				manage_clients.task_queue.put(message)
			except Exception as error:
				print('[ ERROR ][ SECURITY ] Could not send message to client: ', str(error))
				manage_clients.log('[ ERROR ][ SECURITY ] Could not send message to client: ' + str(error))
			return
		
		# Validate Time
		# If the time sent by client is too far away from current time
		# then timestamp is considered to be the time server recieves the submission
		current_time = time.strftime("%H:%M:%S", time.localtime())	
		# current_time = initialize_server.get_time_difference(contest_start_time, current_time)
		time_difference = initialize_server.get_abs_time_difference(current_time, time_stamp)

		# UNCOMMENT THE FOLLOWING LINES IF YOU WISH TO GIVE A N SECONDS GRACE TIME TO CLIENTS
		# AND BELIEVE IN THEIR TIMESTAMP

		# N = 20	# Change this value for grace period time ( Seconds )
		# if time_difference > N:
		# 	print('[ SUBMISSION ][ CONFLICT ] Time difference: ', time_difference, ' Seconds ', )
		# 	print('Current Time: ' + current_time)
		# 	manage_clients.log('[ SUBMISSION ][ CONFLICT ] Time difference: ' + str( time_difference) + ' Seconds ')

		# We don't believe in clients, so timestamp is server time.
		time_stamp = initialize_server.get_time_difference(contest_start_time, current_time)
		
		# Preliminary Validation Finished

		# If contest is not in running state, reject all submissions.
		# This might reject some submissions when user sends code just before contest ends
		if manage_clients.data_changed_flags[10] != 1:
			print('[ SUBMISSION ][ REJECT ] Contest is not running.')
			manage_clients.log('[ SUBMISSION ][ REJECT ] Contest is not running.')
			# Send SRJCT : SubmissionReject
			message = {
				'Code' : 'SRJCT',
				'Receiver' : client_username,
				'Message' : 'Your submission could not be processed! Contest status: NOT RUNNING.',
				'Local Run ID' : local_run_id
			}
			message = json.dumps(message)
			try:
				manage_clients.task_queue.put(message)
			except Exception as error:
				print('[ ERROR ][ SECURITY ] Client has no username so could not send error code.')
				manage_clients.log('[ ERROR ][ SECURITY ] Client has no username so could not send error code.')
			return

		# If submissions are not allowed by ADMIN
		if(manage_clients.data_changed_flags[3] == 0):
			print('[ SUBMISSION ] Rejected by ADMIN')
			manage_clients.log('[ SUBMISSION ] Rejected by ADMIN')
			# Send SRJCT : SubmissionReject
			message = {
				'Code' : 'SRJCT',
				'Receiver' : client_username,
				'Message' : 'Your submission could not be processed!\nSubmissions are not allowed right now.',
				'Local Run ID' : local_run_id
			}
			message = json.dumps(message)
			try:
				manage_clients.task_queue.put(message)
			except Exception as error:
				print('[ ERROR ][ SECURITY ] Client has no username so could not send error code.' )
				manage_clients.log('[ ERROR ][ SECURITY ] Client has no username so could not send error code.' )
			return


		# Check client status, and accept only if it is CONNECTED and not BLOCKED or NEW
		state = client_authentication.check_connected_client(client_username, 'connected_clients')
		if state != 'Connected':
			message = {
				'Code' : 'SRJCT',
				'Receiver' : client_username,
				'Message' : 'Your submission could not be processed. Please Login to send submissions.',
				'Local Run ID' : local_run_id
			}
			message = json.dumps(message)
			try:
				manage_clients.task_queue.put(message)
			except Exception as error:
				print('[ ERROR ][ SECURITY ] Client attempted to send submission without being logged in.' )
				manage_clients.log('[ ERROR ][ SECURITY ] Client attempted to send submission without being logged in.' )
			return

		# Check if client has sent a submission in the previous 'time_minutes_limit' minutes, where 'time_minutes_limit' is set by the ADMIN
		# Reject the submission if this case is true
		prev_time = submissions_management.get_last_sub_time(client_id)
		start_time = manage_clients.config["Contest Start Time"]

		if prev_time == "NONE":
			# This is the first submission of the client
			pass
		else:
			time_minutes_limit = manage_clients.data_changed_flags[21]
			difference = initialize_server.get_time_difference(prev_time, time_stamp)
			difference_seconds = initialize_server.convert_to_seconds(difference)
			difference_minutes = int(difference_seconds / 60)
			time_seconds_limit = time_minutes_limit * 60

			if difference_minutes < time_minutes_limit:
				print('[ SUBMISSION ][ REJECT ] Client sent more than allowed submissions in the time frame.')
				manage_clients.log('[ SUBMISSION ][ REJECT ] Client sent more than allowed submissions in the time frame.')
				message = {
					'Code' : 'SRJCT',
					'Receiver' : client_username,
					'Message' : 'Your submission could not be processed. Resend after ' + str(time_seconds_limit - difference_seconds) + ' Seconds',
					'Local Run ID' : local_run_id
				}
				message = json.dumps(message)
				try:
					manage_clients.task_queue.put(message)
				except Exception as error:
					print('[ ERROR ]Could not publish message to client.' )
					manage_clients.log('[ ERROR ]Could not publish message to client.' )
				return

		# Preliminary Checks successful : Process Submission now
		try:
			run_id, source_file_name = submission.new_submission(client_id, problem_code, language, time_stamp, source_code)
			# Update database by BitsOJCore
			message = {
				'Code' : 'AddNewSub', 
				'RunID' : run_id,
				'Local ID' : local_run_id,
				'Client ID' : client_id,
				'Language' : language,
				'Source File Name' : source_file_name,
				'Problem Code' : problem_code,
				'Status' : 'RUNNING',
				'Timestamp' : time_stamp
			}
			message = json.dumps(message)
			manage_clients.task_queue.put(message)
			print('[ CLIENT ] Sent submission request to CORE')
			manage_clients.log('[ CLIENT ] Sent submission request to CORE')

			# Send this run id to the client
			message = {
				'Code' : 'RESPONSE',
				'Receiver' : client_username,
				'Run ID' : run_id,
				'Local Run ID' : local_run_id
			}
			message = json.dumps(message)
			manage_clients.task_queue.put(message)
			
			# Push the submission in judging queue
			print('[ JUDGE ] Requesting a new judgement')
			manage_clients.log('[ JUDGE ] Requesting a new judgement')
			message = {
				'Code' : 'JUDGE', 
				'Client ID' : client_id, 
				'Client Username' : client_username,
				'Run ID' : run_id,
				'Language' : language,
				'PCode' : problem_code,
				'Source' : source_code,
				'Local Run ID' : local_run_id,
				'Time Stamp' : time_stamp
			}
			message = json.dumps(message)
			manage_clients.task_queue.put(message)

			print('[ REQUEST ] New judging request sent successfully.')
			manage_clients.log('[ REQUEST ] New judging request sent successfully.')
			#######################################################################
				
		except Exception as error:
			print('[ ERROR ] Client submisssion could not be processed : ' + str(error))
			manage_clients.log('[ ERROR ] Client submisssion could not be processed : ' + str(error))
		return

	def client_query_handler(client_id, client_username, query):
		print('[ QUERY ] From ' + str(client_id) + ' : ' + query)
		manage_clients.log('[ QUERY ] From ' + str(client_id) + ' : ' + query)
		query_id = submission.generate_query_id() 
		print('[ QUERY ] Assigned Query ID: ' + str(query_id))
		manage_clients.log('[ QUERY ] Assigned Query ID: ' + str(query_id))
		# Update Database using BitsOJCore
		message = {
			'Code' : 'AddQuery',
			'Query ID' : query_id,
			'Client ID' : client_id,
			'Query' : query
		}
		message = json.dumps(message)
		manage_clients.task_queue.put(message)
		return
		

	# This function handles client logout requests
	def client_logout_handler(client_username, client_id, client_ip):
		print('[ LOGOUT ][ ', client_username, ' ] Initiated')
		# Get client username from database and validate
		database_client_username = client_authentication.get_client_username(client_id) 
		status = client_authentication.check_client_ip(client_id, client_ip)
		# If IP does not match
		if status == 0:
			print('[ LOG OUT ][ ' + client_username + ' ][ REJECT ]')
			manage_clients.log_queue.put('[ LOG OUT ][ ' + client_username + ' ][ REJECT ]')
			return

		if database_client_username == client_username:
			# ie, client_username and client_id pair matches, 
			# check if client is connected
			previously_connected_state = client_authentication.check_connected_client(client_username, 'connected_clients')
			if previously_connected_state == 'Connected':
				print('[ LOG OUT ][ ' + client_username + ' ][ ACCEPT ]')
				manage_clients.log_queue.put('[ LOG OUT ][ ' + client_username + ' ][ ACCEPT ]')
				# Disconnect client in database using BitsOJCore
				message = {
					'Code' : 'UpUserStat', 
					'Username' : client_username,
					'State' : 'Disconnected',
					'IP' : client_ip
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)

				# Update connected clients to indicate new data
				manage_clients.data_changed_flags[1] = 1
				message = {
					"Code" : "SHUTDOWN",
					"Receiver" : client_username
				}
				message = json.dumps(message)
				manage_clients.task_queue.put(message)
		else:
			print('[ LOG OUT ][ ' + client_username + ' ][ REJECT ] ClientID does not match.')
			manage_clients.log_queue.put('[ LOG OUT ][ ' + client_username + ' ][ REJECT ] ClientID does not match.')

		return

