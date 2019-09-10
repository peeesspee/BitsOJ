import pika

class manage_judges():
	channel = ''

	def send_new_request(run_id, p_code, language, sourch_code):
		channel.basic_publish(exchange = '', routing_key = 'judge_requests', body = message, properties = pika.BasicProperties(delivery_mode = 2)) 
		return

	# This function continously listens for judge verdicts
	def listen_judges(channel1):
		print("[ EVENT ] Started listening on judge_verdict channel")
		manage_judges.channel = channel1
		# Judges send requests on judge_requests
		# As soon as a new message is recieved, it is sent to judge_message_handler for further processing
		channel1.basic_consume(queue = 'judge_verdicts', on_message_callback = manage_judges.judge_message_handler, auto_ack = True)
		channel1.start_consuming()

	# This function works on judge messages and passes them on to their respective handler function
	def judge_message_handler(ch, method, properties, body):
		# Decode the message sent by judge
		judge_message = str(body.decode("utf-8"))
		
		print("\n[ PING ] Recieved a new judge message...")
		judge_code = judge_message[0:6]
		if judge_code == 'VRDCT':
			print(judge_message)
		else:
			print("[ ERROR ] Judge sent garbage data. Trust me you don't wanna see it! ")

		return

