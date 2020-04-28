import pika
from connection import manage_connection
from init_judge import initialize_judge
from login_request import authenticate_judge
from verdict import verdict
from file_creation import file_manager
import time, json, os

class communicate_broadcast_server():
	message = ''
	key = initialize_judge.key()
	my_ip = initialize_judge.my_ip()
	
	def listen_server(
			rabbitmq_username,
			rabbitmq_password,
			host, 
			judge_username,
			data_changed_flags,
			task_queue
		):
		print('[ JUDGE ][ BROADCAST PROCESS ] Process started')
		communicate_broadcast_server.judge_username = judge_username
		communicate_broadcast_server.data_changed_flags = data_changed_flags
		communicate_broadcast_server.task_queue = task_queue
		try:
			# Connect with host
			creds = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
			params = pika.ConnectionParameters(
				host = host, 
				credentials = creds, 
				heartbeat=0, 
				blocked_connection_timeout=0
			)
			connection = pika.BlockingConnection(params)
			channel = connection.channel()
		except Exception as error:
			communicate_broadcast_server.data_changed_flags[2] = 1
			print('[ JUDGE ][ BROADCAST PROCESS ] Connection Error: ', error)
			return

		try:
			channel.queue_declare( queue = judge_username, durable=True )
			channel.queue_bind( 
				exchange = 'judge_broadcast_manager', 
				queue = communicate_broadcast_server.judge_username
			)
			channel.queue_bind( 
				exchange = 'judge_manager', 
				queue = communicate_broadcast_server.judge_username
			)
			channel.basic_qos(prefetch_count = 1)

		except Exception as error:
			communicate_broadcast_server.data_changed_flags[2] = 1
			print('[ JUDGE ][ BROADCAST PROCESS ] Error: ', error)
			return

		except(KeyboardInterrupt, SystemExit):
			communicate_broadcast_server.data_changed_flags[1] = 1
			print('[ JUDGE ][ ERROR ] Broadcast process could not work as expected.')
			channel.stop_consuming()
			channel.close()

		print('[ JUDGE ][ BROADCAST PROCESS ] Preprocessing done...')
				
		try:
			channel.basic_consume(
				queue = communicate_broadcast_server.judge_username, 
				on_message_callback = communicate_broadcast_server.server_response_handler, 
			)
			print('[ JUDGE ][ BROADCAST PROCESS ] Started consuming')
			channel.start_consuming()

		except(KeyboardInterrupt, SystemExit):
			print('[ JUDGE ][ BROADCAST ] System Exit initiated.')
			channel.stop_consuming()
			channel.close()
			connection.close()
			communicate_broadcast_server.data_changed_flags[2] = 1
			
		except Exception as error:
			print('[ JUDGE ] Error in broadcast process', error)

		finally:
			return
	
	def server_response_handler(ch, method, properties, body):
		server_data = body.decode('utf-8')
		data = json.loads(server_data)
		code = data['Code']

		if code == 'VRDCT':
			username = data['Receiver']
			run_id = data['Run ID']
			client_id = data['Client ID']
			verdict = data['Status']
			language = data.get('Language', '-')
			problem_code = data['Problem Code']
			time_stamp = data['Timestamp']
			file_with_ext = '< Non Local >'
			judge = data['Judge']
			message = data['Message']
			
			print('\n[ JUDGE ][ BROADCAST ] Update Verdict: Run ', run_id, ' by Client: ', username)

			# Send Record Updation message to Core
			message = {
				'Code' : 'UPDATE',
				'Run ID' : run_id,
				'Client ID' : client_id,
				'Verdict' : verdict,
				'Language' : language,
				'Problem Code' : problem_code,
				'Timestamp' : time_stamp,
				'Filename' : file_with_ext
			}
			message = json.dumps(message)
			communicate_broadcast_server.task_queue.put(message)
			#############################################################################################

		elif code == 'DSCNT':
			print('[ SERVER ] Disconnected by ADMIN')
			# Send SHUT to Interface
			communicate_broadcast_server.data_changed_flags[7] = 1
			# Send SHUT to Core
			communicate_broadcast_server.data_changed_flags[5] = 1
			raise KeyboardInterrupt

		elif code == 'BLOCK':
			print('[ SERVER ] Disconnected by ADMIN')
			# Send BLOCK to Interface
			communicate_broadcast_server.data_changed_flags[8] = 1
			# Send SHUT to Core
			communicate_broadcast_server.data_changed_flags[5] = 1
			raise KeyboardInterrupt