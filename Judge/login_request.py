import pika

class authenticate_judge():
	username = ''
	password = ''
	client_id = 'Null'
	channel = ''

	def login(channel, host):
		authenticate_judge.channel = channel
		authenticate_judge.username = input("Enter Judge's Username \n")
		authenticate_judge.password = input("Enter Judge's Password\n")

		print("[Validating] : " + authenticate_judge.username " @ " + authenticate_judge.password "... \n ")


		authenticate_judge.channel.basic_publish(
			exchange = 'connection_manager',
			queue = 'client_requests',
			body = 'LOGIN' + authenticate_judge.username + ' ' + password
			)

		channel.queue_declare(
			queue = authenticate_judge.username, 
			durable=True
			)

		authenticate_judge.channel.bind(
			exchange = 'connection_manager',
			queue = authenticate_judge.username
			)

		print("Request sent for authentication...\n ")
		print("[LISTENING] @" + authenticate_judge.username + ' ' + '@' + ' ' + authenticate_judge.password "\n")


		authenticate_judge.channel.basic_consume(
			queue = authenticate_judge.username,
			on_mesage_callback = authenticate_judge.response_handler,
			auto_ack = True
			)

		authenticate_judge.channel.start_consume()


	def response_handler(ch, method, properties, body):
		server_data = body.decode('utf-8')

		status = server_data[0:5]

		if(status == 'VALID'):
			status,authenticate_judge.client_id,server_message = server_data.split('+')
			print("[ status ] " + status + "\n[ ClientID ] : " + authenticate_judge.client_id + "\n[ Server ] : " + server_message )
			return status

		elif(status == 'INVLD'):
			print("INVALID USER !!!\n")

			authenticate_judge.channel.queue_delete(
				queue = authenticate_judge.username
				)
			return status

	def get_judge_details():
		return authenticate_judge.client_id, authenticate_judge.username








