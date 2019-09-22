import time
import os
from login import authenticate_login
from manage_data_sending import send_options

class send_code():
	client_id, username = authenticate_login.get_user_details()
	code = None
	file_path = None
	Language = {1 : 'GCC', 2 : 'CPP', 3 : 'PY2', 4 : 'JVA' , 5 : 'PY3'}
	Problem_Code = { 1 : 'PSPA'}
	final_data = ''
	selected_language = ''
	selected_problem = ''
	time_stamp = ''
	cursor = None
	extension = ''


	def uploading_solution(channel, connection, cursor, host, data_changed_flags):
		try:
			submit_solution.file_path = input('Enter path of solution : ') or '/home/sj1328/Desktop/algoPractice/dfs.cpp'
			filename, submit_solution.extension = os.path.splitext(submit_solution.file_path)
			submit_solution.code = open(submit_solution.file_path, 'r').read()
			for key,value in submit_solution.Language.items():
				print(key,value)
			submit_solution.selected_language = input('Select language : ') or 2
			submit_solution.selected_language = str(submit_solution.Language[int(submit_solution.selected_language)])
			for key,value in submit_solution.Problem_Code.items():
				print(key,value)
			submit_solution.selected_problem = input('Select Problem : ') or 1
			submit_solution.selected_problem = str(submit_solution.Problem_Code[int(submit_solution.selected_problem)])
			local_time = time.localtime()
			submit_solution.time_stamp = time.strftime("%H:%M:%S", local_time)
			submit_solution.solution_request(
				channel
				)
		except:
			print("File Not Found ------ Try Again")
			submit_solution.uploading_solution(
				channel
				)

	def solution_request(channel):
		submit_solution.final_data = 'SUBMT ' + submit_solution.client_id + ' '  + submit_solution.selected_problem + ' ' + submit_solution.selected_language + ' ' + submit_solution.time_stamp + ' ' + submit_solution.code

		try:
			send_options.publish_data(channel)
		except:
			print("Error i channel.basic_publish ")

		print("Your code is running \n Wait for the judgement")