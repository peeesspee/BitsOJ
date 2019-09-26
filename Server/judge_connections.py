import pika
import sys
from database_management import submissions_management

class manage_judges():
	channel = ''
	data_changed_flag = ''
	# This function works on judge messages and passes them on to their respective handler function
	def judge_message_handler(ch, method, properties, body):
		# Decode the message sent by judge
		judge_message = str(body.decode('utf-8'))
		
		print('\n[ PING ] Recieved a new judge message : ' + judge_message)
		judge_code = judge_message[0:5]
		if judge_code == 'VRDCT':

			########################################
			# Get username here
			client_username = 'team1'
			status = 'AC'
			run_id = '00001'
			message = 'No Error'
			########################################

			status = judge_message[0:5]
			run_id = judge_message[6:11]
			verdict = judge_message[12:14]
			message = judge_message[15:]

			
			# Fetch client username based on run id
			manage_judges.channel.basic_publish(exchange = 'connection_manager', routing_key = client_username, body = judge_message) 
			print('[ VERDICT ] New verdict sent to ' + client_username)
			submissions_management.update_submission_status(run_id, verdict)
			# Update GUI
			manage_judges.data_changed_flag[0] = 1

		else:
			print('[ ERROR ] Judge sent garbage data. Trust me you don\'t wanna see it! ')
			print(judge_message)
		return

	# This function continously listens for judge verdicts
	def listen_judges(superuser_username, superuser_password, host, data_changed_flag1):
		manage_judges.data_changed_flag = data_changed_flag1
		# Create a connection with rabbitmq and declare exchanges and queues
		try:
			connection = pika.BlockingConnection(pika.URLParameters('amqp://' + superuser_username + ':' + superuser_password + '@' + host + '/%2f'))
			channel = connection.channel()
			manage_judges.channel = channel
			
			channel.queue_declare(queue = 'judge_verdicts', durable = True)
			channel.exchange_declare(exchange = 'judge_manager', exchange_type = 'direct', durable = True)
			channel.queue_bind(exchange = 'judge_manager', queue = 'judge_verdicts')
			
		except Exception as error:
			print('[ CRITICAL ] Could not connect to RabbitMQ server : ' + str(error))
			sys.exit()

		try:
			# Judges send responses on judge_verdicts
			# As soon as a new message is recieved, it is sent to judge_message_handler for further processing
			print('[ LISTEN ] Started listening on judge_verdict')
			channel.basic_consume(queue = 'judge_verdicts', on_message_callback = manage_judges.judge_message_handler, auto_ack = True)
			channel.start_consuming()

		except (KeyboardInterrupt, SystemExit):
			channel.stop_consuming()
			print('[ LISTEN ] STOPPED listening to judge channel')
			connection.close()
			print('[ STOP ] Judge subprocess terminated successfully!')	
			return
			
