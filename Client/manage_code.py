import time
import os
from login import authenticate_login
from connection import manage_connection

class send_code():
	client_id, username = authenticate_login.get_user_details()
	channel,host = manage_connection.channel_host()

	def solution_request(problem_Code,selected_language,time_stamp,code):
		if(selected_language == 'C'):
			extention = '.c'
			language_code = 'GCC'
		elif(selected_language == 'C++'):
			extention = '.cpp'
			language_code = 'CPP'
		elif(selected_language == 'JAVA'):
			extention = '.java'
			language_code = 'JVA'
		elif(selected_language == 'PYTHON-3'):
			extention = '.py'
			language_code = 'PY3'
		else:
			extention = '.py'
			language_code = 'PY2'
		final_data = 'SUBMT ' + authenticate_login.client_id + ' '  + problem_Code + ' ' + language_code + ' ' + time_stamp + ' ' + code
		try:
			authenticate_login.channel.basic_publish(
				exchange = 'connection_manager',
				routing_key = 'client_requests',
				body = final_data,
				)
		except:
			print("Error in channel.basic_publish ")

		print("Your code is running \nWait for the judgement")