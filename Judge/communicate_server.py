import pika
from connection import manage_connection
from verdict import verdict
from file_creation import file_manager
import time
import json

class communicate_server():
	message = ''
	key = '000000000000000'

	def listen_server():

		channel = manage_connection.connect_me()
		channel.queue_declare( queue = 'judge_requests', durable=True )
		channel.exchange_declare( exchange = 'judge_manager', exchange_type = 'direct', durable = True)
		channel.queue_bind( exchange = 'judge_manager', queue = 'judge_verdicts')


		channel.queue_declare( queue = 'judge_verdicts', durable=True )
		channel.exchange_declare( exchange = 'judge_manager', exchange_type = 'direct', durable = True)
		channel.queue_bind( exchange = 'judge_manager', queue = 'judge_verdicts')

		channel.basic_qos(prefetch_count = 1)
		
		
		channel.basic_consume(queue = 'judge_requests', on_message_callback = communicate_server.server_response_handler, auto_ack = True)
		# print("[ERROR]" + "error in consuming") 
		channel.start_consuming()


	
	def server_response_handler(ch, method, properties, body):
		server_data = body.decode('utf-8')

		print(server_data)

		#		server_data = { "Code": "JUDGE", 
		#						"Client ID": "1", 
		#						"Client Username": "team00001", 
		#						"Run ID": 1, 
		#						"Language": "CPP", 
		#						"PCode": "ABCD", 
		#						"Source": "#include<iostream>\n int main(void){ std::cout<<\"Hello\"; return 0; }"
		#						"Local Run ID": 12
		#					}

		

		message = json.loads(server_data)

		run_id = str(message["Run ID"])
		problem_code = message["PCode"]
		language = message["Language"]
		source_code = message["Source"]
		client_id = message["Client ID"]
		client_username = message["Client Username"]
		local_run_id = message["Local Run ID"]
		time_stamp = message['Time Stamp']

		file_name,file_with_ext = communicate_server.make_submission_file(run_id, problem_code, language, source_code)
		# main(file_name, file_with_ext, lang, problem_code, run_id, timelimit):
		print(language)
		print(file_name, file_with_ext, language, problem_code, run_id)
		result,error = verdict.main(file_name, file_with_ext, language, problem_code, run_id, '2')
		# result,error = verdict.main(run_id, problem_code, language, source_code, file_name, file_with_ext, '2')


		#						 message = {
		#						 	'Code' : 'VRDCT', 
		#						 	'Client Username' : username,
		#						 	'Client ID' : client_id,
		#						 	'Status' : 'AC',
		#						 	'Run ID' : run_id,
		#						 	'Message' : 'No Error',
		#						 	'Local Run ID' : local_run_id
		#						 	}
		#						 	message = json.dumps(message)

		# username = 'judge00001'

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
			'Judge' : "judge00001"
			}
		
		message = json.dumps(message)
		

		# print(message)
		# x = message[6:11]
		# print(x)
		# communicate_server.message = verdict
		# time.sleep(1)


		ch.basic_publish(
			exchange = 'judge_manager',
			routing_key = 'judge_verdicts',
			body = message
			)

	def make_submission_file(run_id, problem_code, language, source_code):

		file_name,file_with_ext = file_manager.file_name(run_id, problem_code, language, source_code)
		if file_with_ext != "INVALID FILENAME":
			file_manager.create_file(source_code, language, file_with_ext)
			return file_name,file_with_ext



	# def verdict_of_submission(run_id, problem_code, language, source_code, file_name, file_with_ext):

	# 	# file,pos,lang = verdict.find_file()
	# 	result = ''
	# 	error = ''
	# 	classfile,runfile = verdict.lang_compiler(file_name, file_with_ext, language)
	# 	try:
	# 		verdict.compile_file(classfile,language)
	# 	except Exception as error:
	# 		print("error in compiling")
	# 		result = ''
	# 		error = 'Compilation Error'
	# 	verdict.run_file(runfile, problem_code, run_id)
	# 	verdict.remove_object(file_name, file_with_ext, language)
	# 	result = verdict.compare_outputs(problem_code, run_id)
	# 	# print(file,pos,lang)
	# 	# print(classfile,runfile)
	# 	print(result)

	# 	return result,error
