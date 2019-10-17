import pika
from connection import manage_connection
from compile_run import verdict
from file_creation import file_manager
import time
import json

class communicate_server():
	message = ''

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
		#					}

		

		message = json.loads(server_data)

		run_id = message["Run ID"]
		problem_code = message["PCode"]
		language = message["Language"]
		source_code = message["Source"]

		print("I am in verdict")
		communicate_server.make_submission_file(run_id, problem_code, language, source_code)
		print("verdict completed")

		file,pos,lang = verdict.find_file()
		classfile,runfile = verdict.lang_compiler(file, pos, lang)
		try:
			verdict.compile_file(classfile)
		except Exception as error:
			print("error in compiling")
		verdict.run_file(runfile)
		verdict.remove_object(file, lang, pos)
		verdict = verdict.compare_outputs()
		print(file,pos,lang)
		print(classfile,runfile)
		print(verdict)

		# print(message)
		# x = message[6:11]
		# print(x)
		communicate_server.message = verdict
		time.sleep(5)

		ch.basic_publish(
			exchange = 'judge_manager',
			routing_key = 'judge_verdicts',
			body = communicate_server.message
			)

	def make_submission_file(run_id, problem_code, language, source_code):

		file_name = file_manager.file_name(run_id, problem_code, language, source_code)
		file_manager.create_file(source_code, language, file_name)
		






		





