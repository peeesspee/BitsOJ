import time
import os
import json
from login import authenticate_login
from connection import manage_connection

# Class to handle sending of code 
class send_code():
	client_id, username = authenticate_login.get_user_details()
	channel,host = manage_connection.channel_host()
	extention = None

	# Solution request function 
	def solution_request(problem_Code,selected_language,time_stamp,code,local_run_id,client_key,username,ip):
		if(selected_language == 'C'):
			send_code.extention = '.c'
			language_code = 'C'
		elif(selected_language == 'C++'):
			send_code.extention = '.cpp'
			language_code = 'C++'
		elif(selected_language == 'JAVA'):
			send_code.extention = '.java'
			language_code = 'JAVA'
		elif(selected_language == 'PYTHON-3'):
			send_code.extention = '.py'
			language_code = 'PYTHON-3'
		else:
			send_code.extention = '.py'
			language_code = 'PYTHON-2'
		final_data = {
			'Code' : 'SUBMT',
			'IP' : ip,
			'Username' : username,
			'Client Key': client_key,
			'Local Run ID' : local_run_id,
			'ID' : authenticate_login.client_id,
			'PCode' : problem_Code,
			'Language' : language_code,
			'Time' : time_stamp,
			'Source' : code,
			'Type' : "CLIENT"
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



	def query_request(client_id,client_key,query,username,ip):
		final_data ={
			'Code' : 'QUERY',
			"IP" : ip,
			"Username" : username,
			'ID' : client_id,
			'Client Key': client_key,
			'Query' : query,
			'Type' : 'CLIENT'
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