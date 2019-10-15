import time
import os
import json
from login import authenticate_login
from connection import manage_connection
 
class send_code():
	client_id, username = authenticate_login.get_user_details()
	channel,host = manage_connection.channel_host()
	extention = None

	def solution_request(problem_Code,selected_language,time_stamp,code,local_run_id):
		if(selected_language == 'C'):
			send_code.extention = '.c'
			language_code = 'GCC'
		elif(selected_language == 'C++'):
			send_code.extention = '.cpp'
			language_code = 'CPP'
		elif(selected_language == 'JAVA'):
			send_code.extention = '.java'
			language_code = 'JVA'
		elif(selected_language == 'PYTHON-3'):
			send_code.extention = '.py'
			language_code = 'PY3'
		else:
			send_code.extention = '.py'
			language_code = 'PY2'
		final_data = {
			'Code' : 'SUBMT',
			'Local Run ID' : local_run_id,
			'ID' : authenticate_login.client_id,
			'PCode' : problem_Code,
			'Language' : language_code,
			'Time' : time_stamp,
			'Source' : code
		}
		final_data = json.dumps(final_data)
		print("[ Sending CODE ] " + problem_Code + ' ' + language_code + ' ' + time_stamp)
		try:
			authenticate_login.channel.basic_publish(
				exchange = 'connection_manager',
				routing_key = 'client_requests',
				body = final_data,
				)
		except:
			print("Error in sending code ")

		print("Your code is running \nWait for the judgement")



	def query_request(client_id,query):
		final_data ={
			'Code' : 'QUERY',
			'Client ID' : client_id,
			'Query' : query,
			'Response' : ''
		}
		final_data = json.dumps(final_data)
		print('[QUERY] Sending.....')
		authenticate_login.channel.basic_publish(
			exchange = 'connection_manager',
			routing_key = 'client_requests',
			body = final_data,
			)
		print('[QUERY] Successfully Send')
		print('[QUERY] Waiting for response .....')