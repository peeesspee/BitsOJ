import pika
from connection import manage_connection
from init_judge import initialize_judge
from login_request import authenticate_judge
from verdict import verdict
from file_creation import file_manager
 
import time, json, os
 
class communicate_server():
	message = ''
	key = initialize_judge.key()
	my_ip = initialize_judge.my_ip()
	data_changed_flags = ''
	username = ''
	judge_id = ''
	channel = ''

	def listen_server(
			rabbitmq_username,
			rabbitmq_password,
			host, 
			username,
			judge_id,
			data_changed_flags,
			task_queue
		):
		print('[ JUDGE ][ UNICAST PROCESS ] Process started')
		communicate_server.data_changed_flags = data_changed_flags
		communicate_server.username = username
		communicate_server.judge_id = judge_id
		communicate_server.task_queue = task_queue

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
			communicate_server.channel = channel

		except Exception as error:
			communicate_broadcast_server.data_changed_flags[1] = 1
			print('[ JUDGE ][ UNICAST PROCESS ] Connection Error: ', error)
			return

		try:
			channel.basic_qos( 
				prefetch_count = 1
			)

		except Exception as error:
			communicate_server.data_changed_flags[1] = 1
			print('[ ERROR ] Could not listen to Server Judgement Requests: ', error)
			return

		except(KeyboardInterrupt, SystemExit):
			communicate_server.data_changed_flags[1] = 1
			print('[ JUDGE ][ ERROR ] Unicast process could not work as expected.')
			channel.stop_consuming()
			channel.close()

		print('[ JUDGE ][ UNICAST PROCESS ] Preprocessing done...')

		try:
			channel.basic_consume(
				queue = 'judge_requests', 
				on_message_callback = communicate_server.server_response_handler, 
				auto_ack = True
			)
			print('[ JUDGE ][ UNICAST PROCESS ] Started consuming')
			channel.start_consuming()

		except(KeyboardInterrupt, SystemExit):
			print('[ JUDGE ][ UNICAST ] System Exit initiated.')
			communicate_server.logout()
			channel.stop_consuming()
			channel.close()
			connection.close()
			communicate_server.data_changed_flags[1] = 1

		except Exception as error:
			communicate_server.data_changed_flags[1] = 1
			print('[ JUDGE ] Error in unicast process', error)

		finally:
			return

	def server_response_handler(ch, method, properties, body):
		server_data = body.decode('utf-8')
		message = json.loads(server_data)
		code = message['Code']
		if code == 'JUDGE':
			run_id = str(message["Run ID"])
			problem_code = message["PCode"]
			language = message["Language"]
			source_code = message["Source"]
			client_id = message["Client ID"]
			client_username = message["Client Username"]
			local_run_id = message["Local Run ID"]
			time_stamp = message['Time Stamp']

			print('\n[ JUDGE ] New Submission-> Run ', run_id, ' by Client: ', client_username)

			file_name, file_with_ext = communicate_server.make_submission_file(
				run_id, 
				problem_code, 
				language, 
				source_code
			)

			#############################################################################################
			# Send Record insertion/Updation message to Core
			message = {
				'Code' : 'JUDGE',
				'Run ID' : run_id,
				'Client ID' : client_id,
				'Verdict' : 'RUNNING',
				'Language' : language,
				'Problem Code' : problem_code,
				'Timestamp' : time_stamp,
				'Filename' : file_with_ext
			}
			message = json.dumps(message)
			communicate_server.task_queue.put(message)

			#############################################################################################
			# Actual Judging process
			result, error = verdict.main(file_name, file_with_ext, language, problem_code, run_id, '1')
			#############################################################################################
			try:
				if language == "JAVA":
					os.remove('bitsoj.java')
			except Exception as error:
				print("[ ERROR ] JAVA file deletion error :",error)

			judge_cred = authenticate_judge.get_judge_details()
			message = {
				'Judge Key' : communicate_server.key,
				'Code' : 'VRDCT', 
				'Client Username' : client_username,
				'Client ID' : client_id,
				'Status' : result,
				'Run ID' : run_id,
				'Message' : error,
				'Local Run ID' : local_run_id,
				'PCode': problem_code,
				'Time Stamp' : time_stamp,
				'Judge' : judge_cred[1],
				'IP': communicate_server.my_ip
			}
			message = json.dumps(message)
			ch.basic_publish(
				exchange = 'judge_manager',
				routing_key = 'judge_verdicts',
				body = message
			)
			#############################################################################################
			# Update table
			time.sleep(1)
			# Send Record insertion/Updation message to Core
			message = {
				'Code' : 'UPDATE',
				'Run ID' : run_id,
				'Client ID' : client_id,
				'Verdict' : result,
				'Language' : language,
				'Problem Code' : problem_code,
				'Timestamp' : time_stamp,
				'Filename' : file_with_ext
			}
			message = json.dumps(message)
			communicate_server.task_queue.put(message)
			# Ack the message manually
			# ch.basic_ack(delivery_tag = method.delivery_tag)

	def make_submission_file(run_id, problem_code, language, source_code):
		print('[ JUDGE ] Making submission files...')
		try:
			file_name,file_with_ext = file_manager.file_name(run_id, problem_code, language, source_code)
			if file_with_ext != "INVALID FILENAME":
				file_manager.create_file(source_code, language, file_with_ext)
				return file_name, file_with_ext
		except:
			print('[ JUDGE ] Error while making submission files...')

	def logout():
		if communicate_server.data_changed_flags[7] == 1:
			# Disconnected by SERVER
			# No Logout necessary
			return
			
		try:
			print('[ JUDGE ]Sending LOGOUT message...')
			message = {
				'Judge Key' : communicate_server.key,
				'Code' : 'LOGOUT',
				'Username' : communicate_server.username,
				'ID' : communicate_server.judge_id,
				'IP' : communicate_server.my_ip
			}
			message = json.dumps(message)
			communicate_server.channel.basic_publish(
				exchange = 'judge_manager',
				routing_key = 'judge_verdicts',
				body = message
			)
		except Exception as error:
			print('[ JUDGE ][ UNICAST ] ERROR WHILE LOGGING OUT : ', error)
		return