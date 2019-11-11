import pika
import json

class authenticate_judge():
	username = ''
	password = ''
	client_id = 0
	channel = ''
	login_status = ''
	key = '000000000000000'


	def login(channel, host):
		authenticate_judge.channel = channel
		authenticate_judge.username = input("Enter Judge's Username:") or "judge00001"
		authenticate_judge.password = input("Enter Judge's Password:") or "bits1"
		client_id = 'Nul'

		print("\n[Validating] : " + authenticate_judge.username + "@" + authenticate_judge.password )

		channel.queue_declare(
			queue = authenticate_judge.username, 
			durable=True
			)


		authenticate_judge.channel.queue_bind(
			exchange = 'connection_manager',
			queue = authenticate_judge.username
			)

		message = {
			'Client Key': authenticate_judge.key,
			'Code': 'LOGIN',
			'Username': authenticate_judge.username,
			'Password': authenticate_judge.password,
			'ID': authenticate_judge.client_id,
			'Type': 'JUDGE'

		}

		message = json.dumps(message)


		authenticate_judge.channel.basic_publish(
			exchange = 'connection_manager',
			routing_key = 'client_requests',
			body = message
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
		if server_data == '':
			print("Empty!!!")
			return

		json_data = json.loads(server_data)
		
		#   json_data = {
		#					'Code': 'VALID', 
		#					'Client ID': 'Null', 
		#					'Message': 'Hello Judge!'
		#				}  


		status = json_data['Code']
		# print(status)

		if(status == 'VALID'):
		# 	status = server_data
			print("[STATUS]: " + status  )
			authenticate_judge.channel.stop_consuming()
			authenticate_judge.login_status = status
			authenticate_judge.channel.stop_consuming()


		elif(status == 'INVLD'):
			print("[STATUS] INVALID USER !!!")

			authenticate_judge.channel.queue_delete(
				queue = authenticate_judge.username
				)
			authenticate_judge.login_status = status
			

		


	def get_judge_details():
		return authenticate_judge.client_id, authenticate_judge.username

