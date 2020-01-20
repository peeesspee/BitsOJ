import json, time, os, sys, pika
from database_management import submissions_management, scoreboard_management, user_management, client_authentication
from init_server import initialize_server
updated_config = 0

class manage_judges():
	channel = ''
	data_changed_flags = ''
	task_queue = ''
	ranking_algoritm = 1
	updated_config = 0
	config = ''
	# This function continously listens for judge verdicts
	def listen_judges(superuser_username, superuser_password, host, data_changed_flags, task_queue, log_queue):
		manage_judges.data_changed_flags = data_changed_flags
		manage_judges.task_queue = task_queue
		manage_judges.log_queue = log_queue
		print('  [ START ] Judge Manager subprocess started.')
		manage_judges.log('  [ START ] Judge Manager subprocess started.')
		# Create a connection with rabbitmq and declare exchanges and queues
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
			manage_judges.channel = channel

			channel.exchange_declare(
				exchange = 'judge_manager', 
				exchange_type = 'direct', 
				durable = True
			)
			channel.exchange_declare( 
				exchange = 'judge_broadcast_manager', 
				exchange_type = 'fanout', 
				durable = True
			)
			channel.queue_declare(
				queue = 'judge_verdicts', 
				durable = True
			)
			channel.queue_bind(
				exchange = 'judge_manager', 
				queue = 'judge_verdicts'
			)
			# Read only one request at a time, and process it.
			# If the request could not be processed, it is resent to the queue
			channel.basic_qos(prefetch_count = 1)

		except Exception as error:
			print('[ CRITICAL ] Could not connect to RabbitMQ server : ' + str(error))
			manage_judges.log('[ CRITICAL ] Could not connect to RabbitMQ server : ' + str(error))
			manage_judges.data_changed_flags[26] = 1
			while manage_judges.data_changed_flags[7] !=1:
				time.sleep(0.5)
			sys.exit()

		try:
			# Read config
			manage_judges.config = initialize_server.read_config()
		except:
			print("[ ERROR ] Could not read config. Contest scores set to default values.")
			manage_judges.log("[ ERROR ] Could not read config. Contest scores set to default values.")

		try:
			# Judges send responses on judge_verdicts
			# As soon as a new message is recieved, it is sent to judge_message_handler for further processing
			print('[ LISTEN ] Started listening on judge_verdict')
			manage_judges.log('[ LISTEN ] Started listening on judge_verdict')
			channel.basic_consume(
				queue = 'judge_verdicts', 
				on_message_callback = manage_judges.judge_message_handler,
				exclusive = True 
			)
			channel.start_consuming()
		except (KeyboardInterrupt, SystemExit):
			channel.stop_consuming()
			print('[ LISTEN ] STOPPED listening to judge channel')
			manage_judges.log('[ LISTEN ] STOPPED listening to judge channel')

		except (pika.exceptions.ChannelClosedByBroker):
			print(
				'[ ERROR ] : Could not get a lock on judge_verdicts' +
				' Please check management portal and remove any consumers from the queue'
			)
			manage_judges.log(
				'[ ERROR ] : Could not get a lock on judge_verdicts' +
				'Please check management portal and remove any consumers from the queue'
			)
			
		except Exception as error:
			print('[ CRITICAL ]: ' + error)
			manage_judges.log('[ CRITICAL ]: ' + error)

		finally:
			manage_judges.data_changed_flags[7] = 1
			connection.close()
			print('[ STOP ] Judge subprocess terminated successfully!')
			manage_judges.log('[ STOP ] Judge subprocess terminated successfully!')
			return

	def log(message):
		manage_judges.log_queue.put(message)

	#This function works on judge messages and passes them on to their respective handler function
	def judge_message_handler(ch, method, properties, body):
		# Re-Read the config after contest starts to inculcate any changes
		if manage_judges.updated_config == 0:
			manage_judges.updated_config = 1
			manage_judges.config = initialize_server.read_config()

		# Decode the message sent by judge
		judge_message = str(body.decode('utf-8'))
		print('[ PING ] Recieved a new judge message.')
		manage_judges.log('[ PING ] Recieved a new judge message.')
		try:
			json_data = json.loads(judge_message)
			# Validate Judge message
			judge_key = json_data.get('Judge Key')
			if judge_key == '' or judge_key == None:
				print('[ JUDGE ][ ERROR ] Judge key not found!')
				manage_judges.log('[ JUDGE ][ ERROR ] Judge key not found!')
				ch.basic_ack(delivery_tag = method.delivery_tag)
				return

			if judge_key != manage_judges.config['Judge Key']:
				print('[ SECURITY ][ CRITICAL ] Judge Key did not match!')
				manage_judges.log('[ SECURITY ][ CRITICAL ] Judge Key did not match!')
				print('[ SECURITY ][ CRITICAL ] Full Message: ' + judge_message)
				manage_judges.log('[ SECURITY ][ CRITICAL ] Full Message: ' + judge_message)
				# Get Run ID
				if code == 'VRDCT':
					run_id = json_data['Run ID']
					# Mark the submission
					judge = json_data['Judge']
					# Send Database updation task to BitsOJCore
					message = {
						'Code' : 'UpSubStat', 
						'RunID' : run_id,
						'Verdict' : 'SECURITY',
						'Sent Status' : 'HALTED',
						'Judge' : 'CHECK' + judge
					}
					message = json.dumps(message)
					manage_judges.task_queue.put(message)

				ch.basic_ack(delivery_tag = method.delivery_tag)
				return
			# Judge has been validated.
			code = json_data["Code"] 
			if code == 'VRDCT':
				local_run_id = json_data['Local Run ID']
				client_username = json_data['Client Username']
				client_id = json_data['Client ID']
				status = json_data['Status']
				run_id = json_data['Run ID']
				message = json_data['Message']
				p_code = json_data['PCode']
				time_stamp = json_data['Time Stamp']
				judge = json_data['Judge']

				print('[ VERDICT ] ' + judge + ' :: ' + status)
				manage_judges.log('[ VERDICT ] ' + judge + ' :: ' + status)

				# Save message details to file
				filename = './Client_Submissions/' + str(run_id) + '.info'
				current_time = time.strftime("%H:%M:%S", time.localtime())
				try:
					# read file
					with open(filename) as file:
						data = file.read()
				except:
					# New file write
					data = '=========='
					pass

				try:
					# write file
					file = open(filename, 'w')
					file.write('Run Time: ' + current_time + '\n')
					file.write('Verdict from: ' + judge + ' : ' + status + '\n')
					file.write(json_data['Message'])
					file.write('\n\n')
					# Write previous run info
					# This ensures the latest run data is at top
					file.write(data)
					file.close()
					
				except Exception as error:
					print('[ ERROR ] Judge verdict could not be written in the file!' + str(error))
					manage_judges.log('[ ERROR ] Judge verdict could not be written in the file!' + str(error))

				try:
					# write file
					filename = './Client_Submissions/' + str(run_id) + '_latest.info'
					file = open(filename, 'w')
					file.write(json_data['Message'])
					file.close()
					
				except Exception as error:
					print('[ ERROR ] Judge verdict could not be written in the file!' + str(error))
					manage_judges.log('[ ERROR ] Judge verdict could not be written in the file!' + str(error))

				# Create response to send to client
				message = {
					'Code' : 'VRDCT', 
					'Receiver' : client_username,
					'Local Run ID' : local_run_id,
					'Run ID' : run_id,
					'Status' : status,
					'Message' : message,
					'Judge' : judge,
					'Client ID' : client_id,
					'Problem Code' : p_code,
					'Timestamp' : time_stamp
				}
				message = json.dumps(message)

				# Publish message to client if allowed
				if manage_judges.data_changed_flags[20] == 0:
					# Manual Review is OFF
					try:
						# Put response to task queue, to further connect to the client
						manage_judges.task_queue.put(message)
						print('[ VERDICT ] New verdict sent to ' + client_username)
						manage_judges.log('[ VERDICT ] New verdict sent to ' + client_username)
					except Exception as error:
						ch.basic_ack(delivery_tag = method.delivery_tag)
						print('[ ERROR ] Could not publish result to client : ' + str(error))
						manage_judges.log('[ ERROR ] Could not publish result to client : ' + str(error))
						return
				else:
					# Manual Review is ON
					# Send Database updation task to BitsOJCore
					message = {
						'Code' : 'UpSubStat', 
						'RunID' : run_id,
						'Verdict' : status,
						'Sent Status' : 'REVIEW',
						'Judge' : judge
					}
					message = json.dumps(message)
					manage_judges.task_queue.put(message)

				# Send Acknowldgement of message recieved and processed
				ch.basic_ack(delivery_tag = method.delivery_tag)
			elif code == 'LOGOUT':
				username = json_data['Username']
				judge_id = json_data['ID']
				judge_ip = json_data['IP']
				status = client_authentication.validate_connected_judge(username, judge_id, judge_ip)
				if status == True:
					# Valid request
					# Send Database updation task to BitsOJCore
					message = {
						'Code' : 'UpJudgeStat', 
						'Username' : username,
						'State' : 'Disconnected',
						'IP' : judge_ip
					}
					message = json.dumps(message)
					manage_judges.task_queue.put(message)

					print('[ JUDGE ][ LOGOUT ] ' + username + ' Logged Out')
					manage_judges.log('[ JUDGE ][ LOGOUT ] ' + username + ' Logged Out')
				else:
					print('[ JUDGE ][ LOGOUT ] ' + username + ' Rejected Logout')
					manage_judges.log('[ JUDGE ][ LOGOUT ] ' + username + ' Rejected Logout')
				ch.basic_ack(delivery_tag = method.delivery_tag)

			else:
				ch.basic_ack(delivery_tag = method.delivery_tag)
				print('[ ERROR ] Judge data could not be parsed. Recheck judge Authenticity.')
				manage_judges.log('[ ERROR ] Judge data could not be parsed. Recheck judge Authenticity.')
				return

		except Exception as error:
			ch.basic_ack(delivery_tag = method.delivery_tag)
			print('[ ERROR ] Could not parse judge JSON data : ' + str(error))
			manage_judges.log('[ ERROR ] Could not parse judge JSON data : ' + str(error))
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[ ERROR ] : ',exc_type, fname, exc_tb.tb_lineno)
			manage_judges.log('[ ERROR ] : ',exc_type, fname, exc_tb.tb_lineno)
			return

		finally:
			return