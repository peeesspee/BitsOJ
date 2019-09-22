import pika
import sys

class manage_judges():
	channel = ''

	# This function works on judge messages and passes them on to their respective handler function
	def judge_message_handler(ch, method, properties, body):
		# Decode the message sent by judge
		judge_message = str(body.decode("utf-8"))
		
		print("\n[ PING ] Recieved a new judge message...")
		judge_code = judge_message[0:5]
		if judge_code == 'VRDCT':
			print(judge_message)
		else:
			print("[ ERROR ] Judge sent garbage data. Trust me you don't wanna see it! ")
		return

	# This function continously listens for judge verdicts
	def listen_judges(superuser_username, superuser_password, host, data_changed_flag):
		
		# Create a connection with rabbitmq and declare exchanges and queues
		try:
			connection = pika.BlockingConnection(pika.URLParameters("amqp://" + superuser_username + ":" + superuser_password + "@" + host + "/%2f"))
			channel = connection.channel()
			manage_judges.channel = channel
			
			channel.queue_declare(queue = 'judge_verdicts', durable = True)
			channel.exchange_declare(exchange = 'judge_manager', exchange_type = 'direct', durable = True)
			channel.queue_bind(exchange = 'judge_manager', queue = 'judge_verdicts')
			
		except Exception as error:
			print("[ CRITICAL ] Could not connect to RabbitMQ server : " + str(error))
			sys.exit()

		try:
			# Judges send responses on judge_verdicts
			# As soon as a new message is recieved, it is sent to judge_message_handler for further processing
			print("[ LISTEN ] Started listening on judge_verdict")
			channel.basic_consume(queue = 'judge_verdicts', on_message_callback = manage_judges.judge_message_handler, auto_ack = True)
			channel.start_consuming()

		except (KeyboardInterrupt, SystemExit):
			channel.stop_consuming()
			print("[ LISTEN ] STOPPED listening to judge channel")
			connection.close()
			print("[ STOP ] Judge subprocess terminated successfully!")	
			return
			
