import pika
from login import authenticate_login

class listening():

	username = None
	channel = None
	client_id = None
	host = None
	login_status = None

	def initialize():
		listening.username = ''
		listening.channel = ''
		listening.client_id = 'Null'
		listening.login_status = False

	def listen_server(channel_1):
		listening.client_id, listening.username = authenticate_login.get_user_details()
		listening.channel = channel_1
		listening.channel.basic_consume(
			queue = listening.username, 
			on_message_callback = listening.server_response_handler, 
			auto_ack = True
			)

		listening.channel.start_consuming()


	def server_response_handler(ch,method,properties,body):
		server_data = body.decode('utf-8')
		# status of the login request
		status = server_data[0:5]
		if status == "VALID" or status == "INVLD":
			listening.server_login_approvals_handler(server_data)

		

	def server_login_approvals_handler(server_data):
		status = server_data[0:5]
		if(status == 'VALID'):
			status,listening.client_id,server_message = server_data.split('+')
			print("[ Status ] " + status + "\n[ ClientID ] : " + listening.client_id + "\n[ Server ] : " + server_message)
			listening.login_status = True

		elif status == "INVLD":
			print("Invalid login!!!")
			# if the login fails deleting the existing queue for the client and again asking for login
			listening.channel.queue_delete(
				queue = listening.username
				)
			listening.login_status = False
		
		
