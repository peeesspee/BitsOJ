# from login import authenticate_login
from database_management import manage_database

class start_listening():
	# client_id, username = authenticate_login.get_user_details()
	channel = None
	login_status = False 

	def listen_server(channel):
		start_listening.channel.basic_consume(
			queue = start_listening.username,
			on_message_callback = start_listening.server_response_handler,
			auto_ack = True
			)
		start_listening.start_consuming()

	def server_response_handler(ch,method,properties,body):
		server_data = body.decode('utf-8')
		status = server_data[0:5]
		if status == "VRDCT":
			start_listening.submission_verdict(server_data)
		elif status == "CLRFN":
			print("UNDER DEVELOPMENT")
		elif status == "SCRBD":
			print("UNDER DEVELOPMENT")
		elif status == "START" or status == "CSTOP" or status == "PAUSE":
			print("UNDER DEVELOPMENT")
		elif status == "UPDTE":
			print("UNDER DEVELOPMENT")
		else:
			print("WRONG INPUT")

	def login_approval_handler(ch,method,properties,server_data):
		status = server_data[0:5]
		if (status == 'VALID'):
			status,start_listening.client_id,server_message = server_data.split('+')
			authenticate_login.client_id = start_listening.client_id
			print("[ Status ] " + status + "\n[ ClientID ] : " + listening.client_id + "\n[ Server ] : " + server_message)
		else:
			print("Invalid Login!!!!")
			start_listening.channel.queue_delete(
				queue = start_listening.username
				)


	def submission_verdict(server_data):
		run_id = server_data[6:11]
		code_result = server_data[12:14]
		error = server_data[15:]
		print('[ Run ID : ' + run_id + ' ] [ Result : ' + code_result + ' ] [ error : ' + error + ' ]')
		manage_database.insert_verdict(
			start_listening.client_id,
			run_id,
			code_result,
			)