from database_management import submission_management
from login import authenticate_login
import pika
import json
import sys

class start_listening():
	# client_id, username = authenticate_login.get_user_details()
	channel = None
	connection = None
	cursor = None
	host = None
	login_status = False 
	data_changed_flags = ''

	def listen_server(rabbitmq_username,rabbitmq_password,cursor,host,data_changed_flags2):
		try:
			creds = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
			params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
			connection = pika.BlockingConnection(params)
			channel = connection.channel()
			start_listening.channel = channel
			start_listening.connection = connection
			start_listening.cursor = cursor
			start_listening.host = host
			start_listening.data_changed_flags = data_changed_flags2


			start_listening.channel.basic_consume(
				queue = authenticate_login.username,
				on_message_callback = start_listening.server_response_handler,
				auto_ack = True
				)
			start_listening.channel.start_consuming()
		except (KeyboardInterrupt, SystemExit):
			print('[ DELETE ] Queue ' + authenticate_login.username + ' deleted...')
			print("[ STOP ] Keyboard interrupt")
		finally:
			print('Cleanup')
			start_listening.channel.stop_consuming()
			start_listening.channel.queue_delete(authenticate_login.username)
			
	
			


	def server_response_handler(ch,method,properties,body):
		server_data = str(body.decode("utf-8"))

		json_data = json.loads(server_data)
		code = json_data["Code"]
		if code == 'VRDCT':
			status = json_data['Status']
			run_id = json_data['Run ID']
			message = json_data['Message']
			local_id = json_data["Local Run ID"]
			print("[ Status ] " + status + "\n[ Run ID ] : " + str(run_id) + "\n[ Message ] : " + message)
			start_listening.submission_verdict(json_data)
		elif code == 'SRJCT':
			print('Submission Rejected')
		elif code == "CLRFN":
			print("UNDER DEVELOPMENT")
		elif code == "SCRBD":
			print("UNDER DEVELOPMENT")
		elif code == "START" or code == "CSTOP" or code == "PAUSE":
			print("UNDER DEVELOPMENT")
		elif code == "UPDTE":
			print("UNDER DEVELOPMENT")
		else:
			print("WRONG INPUT")



	def submission_verdict(server_data):
		run_id = str(server_data["Run ID"])
		code_result = server_data["Status"]
		message = server_data["Message"]
		local_id = server_data["Local Run ID"]
		print(message)
		print('[ Run ID : ' + run_id + ' ] [ Result : ' + code_result + ' ] [ error : ' + message + ' ]')
		submission_management.update_verdict(
			local_id,
			authenticate_login.client_id,
			run_id,
			code_result,
			)
		start_listening.data_changed_flags[1] = 1