import pika
import time
import os
from database_management import manage_database
from login import authenticate_login

class submit_solution():
	client_id = ''
	username = ''
	code = ''
	file_path = ''
	Language = {1 : 'C', 2 : 'C++', 3 : 'Python', 4 : 'Java'}
	Problem_Code = { 1 : 'PSP'}
	final_data = ''
	selected_language = ''
	selected_problem = ''
	time_stamp = ''
	cursor = None
	extension = ''


	def read_solution(cur,channel):
		submit_solution.client_id, submit_solution.username = authenticate_login.get_user_details()
		submit_solution.cursor = cur
		try:
			submit_solution.file_path = input('Enter path of solution : ')
			filename, submit_solution.extension = os.path.splitext(submit_solution.file_path)
			submit_solution.code = open(submit_solution.file_path, 'r').read()
			for key,value in submit_solution.Language.items():
				print(key,value)
			submit_solution.selected_language = input('Select language : ')
			submit_solution.selected_language = str(submit_solution.Language[int(submit_solution.selected_language)])
			for key,value in submit_solution.Problem_Code.items():
				print(key,value)
			submit_solution.selected_problem = input('Select Problem : ')
			submit_solution.selected_problem = str(submit_solution.Problem_Code[int(submit_solution.selected_problem)])
			local_time = time.localtime()
			submit_solution.time_stamp = time.strftime("%H:%M:%S", local_time)
			submit_solution.solution_request(
				channel
				)
		except:
			print("File Not Found ------ Try Again")
			submit_solution.read_solution(
				submit_solution.cursor,
				channel
				)

	def solution_request(channel):
		submit_solution.final_data = 'SUBMT ' + submit_solution.client_id + ' '  + submit_solution.selected_problem + ' ' + submit_solution.selected_language + ' ' + submit_solution.time_stamp + ' ' + submit_solution.code
		print(channel)
		channel.basic_publish(
			exchange = 'connection_manager', 
			routing_key = 'client_requests', 
			body = submit_solution.final_data
			)

		print('Your Code is running ......')
		



		