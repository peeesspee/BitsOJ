import pika
import sys
import json, time
from database_management import submissions_management, scoreboard_management
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

			manage_judges.ranking_algoritm = manage_judges.data_changed_flags[17]
			
			channel.exchange_declare(
				exchange = 'judge_manager', 
				exchange_type = 'direct', 
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
				on_message_callback = manage_judges.judge_message_handler
			)
			channel.start_consuming()
		except (KeyboardInterrupt, SystemExit):
			manage_judges.data_changed_flags[7] = 1
			channel.stop_consuming()
			print('[ LISTEN ] STOPPED listening to judge channel')
			manage_judges.log('[ LISTEN ] STOPPED listening to judge channel')
			connection.close()
			print('[ STOP ] Judge subprocess terminated successfully!')
			manage_judges.log('[ STOP ] Judge subprocess terminated successfully!')
			return

	def log(message):
		manage_judges.log_queue.put(message)

	#This function works on judge messages and passes them on to their respective handler function
	def judge_message_handler(ch, method, properties, body):
		if manage_judges.updated_config == 0:
			manage_judges.updated_config = 1
			manage_judges.config = initialize_server.read_config()

		# Decode the message sent by judge
		judge_message = str(body.decode('utf-8'))
		print('[ PING ] Recieved a new judge verdict.')
		manage_judges.log('[ PING ] Recieved a new judge verdict.')
		try:
			json_data = json.loads(judge_message)
			code = json_data["Code"]
			# Validate Judge message
			judge_key = json_data['Judge Key']
			if judge_key != manage_judges.config['Judge Key']:
				print('[ SECURITY ][ CRITICAL ] Judge Key did not match!')
				manage_judges.log('[ SECURITY ][ CRITICAL ] Judge Key did not match!')
				print('[ SECURITY ][ CRITICAL ] Full Message: ' + judge_message)
				manage_judges.log('[ SECURITY ][ CRITICAL ] Full Message: ' + judge_message)
				# Get Run ID
				if code == 'VRDCT':
					run_id = json_data['Run ID']
					# Mark the submission
					submissions_management.update_submission_status(run_id, 'SECURITY', 'HALTED', 'UNKNOWN')
				manage_judges.data_changed_flags[0] = 1
				ch.basic_ack(delivery_tag = method.delivery_tag)
				return

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
					file.write(data)
					# This ensures the latest run data is at top
					
				except Exception as error:
					print('[ ERROR ] Judge verdict could not be written in the file!' + str(error))
					manage_judges.log('[ ERROR ] Judge verdict could not be written in the file!' + str(error))

				try:
					# write file
					filename = './Client_Submissions/' + str(run_id) + '_latest.info'
					file = open(filename, 'w')
					file.write(json_data['Message'])
					
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
					'Judge' : judge
				}
				message = json.dumps(message)

				# Publish message to client if allowed
				# Update scoreboard also when manual review is ON
				if manage_judges.data_changed_flags[20] == 0:
					
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

					# Update scoreboard
					problem_max_score = manage_judges.config['AC Points']
					problem_penalty = manage_judges.config['Penalty Score']
					time_penalty = manage_judges.config['Penalty Time']
					# call scoreboard updation function		TODO MOVE TO CORE
					scoreboard_management.update_user_score(
						client_id, 
						run_id,
						problem_max_score, 
						problem_penalty,
						status, 
						p_code,
						time_stamp,
						manage_judges.ranking_algoritm # Ranking Algorithm
					)

					# Update scoreboard view in server
					manage_judges.data_changed_flags[16] = 1
					# Broadcast new scoreboard to clients whenever a new AC is recieved 
					# and scoreboard update is allowed.
					if status == 'AC' and manage_judges.data_changed_flags[15] == 1:
						# Flag 18 signals interface to update scoreboard
						manage_judges.data_changed_flags[18] = 1
				else:
					submissions_management.update_submission_status(run_id, status, 'REVIEW', judge)
					# Update submission GUI
					manage_judges.data_changed_flags[0] = 1

				# Send Acknowldgement of message recieved and processed
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
			return

		return