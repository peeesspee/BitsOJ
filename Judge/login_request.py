import pika

class authenticate_judge():
	username = ''
	password = ''
	client_id = 'Null'
	channel = ''
	login_status = ''


	def login(channel, host):
		authenticate_judge.channel = channel
		authenticate_judge.username = input("Enter Judge's Username \n") or "judge1"
		authenticate_judge.password = input("Enter Judge's Password\n") or "judge1"

		print("\n[Validating] : " + authenticate_judge.username + "@" + authenticate_judge.password )

		channel.queue_declare(
			queue = authenticate_judge.username, 
			durable=True
			)


		authenticate_judge.channel.queue_bind(
			exchange = 'connection_manager',
			queue = authenticate_judge.username
			)


		authenticate_judge.channel.basic_publish(
			exchange = 'connection_manager',
			routing_key = 'client_requests',
			body = 'LOGIN ' + authenticate_judge.username + ' ' + authenticate_judge.password + ' ' + authenticate_judge.client_id + ' ' + "JUDGE"
			)



		print("Request sent for authentication... ")
		print("[LISTENING]:" + authenticate_judge.username + '@'  + authenticate_judge.password )


		authenticate_judge.channel.basic_consume(
			queue = authenticate_judge.username,
			on_message_callback = authenticate_judge.response_handler,
			auto_ack = True
			)

		authenticate_judge.channel.start_consuming()


	def response_handler(ch, method, properties, body):
		server_data = body.decode('utf-8')

		status = server_data

		if(status == 'VALID'):
			status = server_data
			print("[status]: " + status  )
			authenticate_judge.channel.stop_consuming()
			authenticate_judge.login_status = status


			

		elif(status == 'INVLD'):
			print("\nINVALID USER !!!\n")

			authenticate_judge.channel.queue_delete(
				queue = authenticate_judge.username
				)
			authenticate_judge.login_status = status
			

		


	def get_judge_details():
		return authenticate_judge.client_id, authenticate_judge.username








