import pika
import json
from init_judge import initialize_judge

class authenticate_judge():
	username = 'Nouser'
	password = 'Nopass'
	judge_id = 'NULL'
	channel = ''
	login_status = ''
	key = initialize_judge.key() 
	my_ip = initialize_judge.my_ip()


	def login(channel, host, username, password):
		authenticate_judge.channel = channel
		authenticate_judge.username = username
		authenticate_judge.password = password
		
		username, password, judge_id = initialize_judge.get_credentials()
		if judge_id != 'NULL':
			authenticate_judge.judge_id = judge_id

		print("\n[ VALIDATNG ] : " + authenticate_judge.username + "@" + authenticate_judge.password )

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
			'ID': authenticate_judge.judge_id,
			'Type': 'JUDGE',
			'IP' : authenticate_judge.my_ip
		}

		message = json.dumps(message)


		authenticate_judge.channel.basic_publish(
			exchange = 'connection_manager',
			routing_key = 'client_requests',
			body = message
			)

		print("Request sent for authentication... ")
		print("[ LISTENING ]:" + authenticate_judge.username + '@'  + authenticate_judge.password )


		authenticate_judge.channel.basic_consume(
			queue = authenticate_judge.username,
			on_message_callback = authenticate_judge.response_handler,
			auto_ack = True
		)
		authenticate_judge.channel.start_consuming()
		return authenticate_judge.login_status

	def response_handler(ch, method, properties, body):
		server_data = body.decode('utf-8')
		json_data = json.loads(server_data)
		
		status = json_data['Code']

		if( status == 'VALID' ):
			print("[STATUS]: " + status  )
			judge_id = json_data['ID']
			authenticate_judge.channel.stop_consuming()
			authenticate_judge.login_status = status

			initialize_judge.save_details(
				authenticate_judge.username,
				authenticate_judge.password,
				judge_id
			)
			
		elif( status == 'INVLD' ):
			print("[STATUS] INVALID USER !!!")
			authenticate_judge.channel.stop_consuming()
			authenticate_judge.channel.queue_delete(
				queue = authenticate_judge.username
				)
			authenticate_judge.login_status = status

		elif( status == 'LRJCT'):
			authenticate_judge.channel.stop_consuming()
			authenticate_judge.channel.queue_delete(
				queue = authenticate_judge.username
				)
			authenticate_judge.login_status = status
		
	def get_judge_details():
		return authenticate_judge.judge_id, authenticate_judge.username, authenticate_judge.password

