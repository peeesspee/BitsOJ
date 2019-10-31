import pika
import sys
import json
from database_management import submissions_management, scoreboard_management
from init_server import initialize_server

class manage_judges():
	channel = ''
	data_changed_flags = ''
	ranking_algoritm = 1
	ac_score = 10
	penalty_score = 0
	penalty_time = 0
	# This function continously listens for judge verdicts
	def listen_judges(superuser_username, superuser_password, host, data_changed_flag1):
		manage_judges.data_changed_flags = data_changed_flag1
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
			
			channel.queue_declare(queue = 'judge_verdicts', durable = True)
			channel.exchange_declare(exchange = 'judge_manager', exchange_type = 'direct', durable = True)
			channel.queue_bind(exchange = 'judge_manager', queue = 'judge_verdicts')
			
		except Exception as error:
			print('[ CRITICAL ] Could not connect to RabbitMQ server : ' + str(error))
			sys.exit()

		try:
			# Read config
			config = initialize_server.read_config()
			manage_judges.ac_score = config['AC Points']
			manage_judges.penalty_score = config['Penalty Score']
			manage_judges.penalty_time = config['Penalty Time']
		except:
			print("[ ERROR ] Could not read config. Contest scores set to default values.")


		try:
			# Judges send responses on judge_verdicts
			# As soon as a new message is recieved, it is sent to judge_message_handler for further processing
			print('[ LISTEN ] Started listening on judge_verdict')
			channel.basic_consume(
				queue = 'judge_verdicts', 
				on_message_callback = manage_judges.judge_message_handler, 
				auto_ack = True
			)
			channel.start_consuming()

		except (KeyboardInterrupt, SystemExit):
			channel.stop_consuming()
			print('\n[ LISTEN ] STOPPED listening to judge channel')
			
			connection.close()
			print('\n[ STOP ] Judge subprocess terminated successfully!\n')	
			return

	#This function works on judge messages and passes them on to their respective handler function
	def judge_message_handler(ch, method, properties, body):
		# Decode the message sent by judge
		judge_message = str(body.decode('utf-8'))
		print('\n[ PING ] Recieved a new judge message : ' + judge_message)
		try:
			json_data = json.loads(judge_message)
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
			else:
				print('[ ERROR ] Judge sent garbage data. Trust me you don\'t wanna see it! ')
				return

		except Exception as error:
			print('[ ERROR ] Could not parse judge JSON data : ' + str(error))
			return

		# Create response to send to client
		message = {
		'Code' : 'VRDCT', 
		'Local Run ID' : local_run_id,
		'Run ID' : run_id,
		'Status' : status,
		'Message' : message
		}
		message = json.dumps(message)

		try:
			manage_judges.channel.basic_publish(
				exchange = 'connection_manager', 
				routing_key = client_username, 
				body = judge_message
			) 
			print('[ VERDICT ] New verdict sent to ' + client_username)
			submissions_management.update_submission_status(run_id, status)
			# Update GUI
			manage_judges.data_changed_flags[0] = 1
		except Exception as error:
			print('[ ERROR ] Could not publish result to client : ' + str(error))
			return

		# Update scoreboard
		if manage_judges.data_changed_flags[15] == 1:
			# Get score for the problem from config
			# TODO
			problem_max_score = manage_judges.ac_score
			problem_penalty = manage_judges.penalty_score
			# call scoreboard updation function
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
			manage_judges.data_changed_flags[16] = 1
		
		return