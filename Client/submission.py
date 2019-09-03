import pika
import time
from database_management import manage_database

class submit_solution():
	client_id_1 = ''
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


	def read_solution(cur,client_id,username,channel):
		submit_solution.cursor = cur
		try:
			submit_solution.file_path = input('Enter path of solution : ')
			filename, submit_solution.extension = os.path.splitext(submit_solution.file_path)
			submit_solution.code = open(submit_solution.file_path, 'r').read() 
			for i,k in submit_solution.Language:
				print(i,k)
			submit_solution.selected_language = input('Select language : ')
			submit_solution.selected_language = str(Language[int(submit_solution.selected_language)])
			for i,k in submit_solution.Problem_Code:
				print(i,k)
			submit_solution.selected_problem = input('Select Problem : ')
			submit_solution.selected_problem = str(Problem_Code[int(submit_solution.selected_problem)])
			local_time = time.localtime()
			submit_solution.time_stamp = time.strftime("%H:%M:%S", local_time)
			submit_solution.solution_request(submit_solution.code,client_id,username,submit_solution.selected_language,submit_solution.selected_problem,submit_solution
				.time_stamp,channel)
		except:
			print("File Not Found ------ Try Again")
			submit_solution.read_solution(client_id,username,channel)

	def solution_request(client_id,usernamechannel):
		submit_solution.client_id_1 = client_id
		submit_solution.final_data = 'Submt ' + client_id + ' '  + submit_solution.problem_code + ' ' + submit_solution.language + ' ' + submit_solution.time_stamp + ' ' + submit_solution.code
		channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = submit_solution.final_data)
		print('Your Code is running ......')
		channel.basic_consume(queue = username, on_message_callback =submit_solution.server_response_handler , auto_ack = True)


	def server_response_handler(ch,method,properties,body):
		submission_result = body.decode('utf-8')
		run_id = int(submission_result[6:11])
		result = submission_result[12:14]
		if result != 'AC':
			error = submission_result[15:]
			manage_database.insert_verdict(submit_solution.client_id,submit_solution.cursor,run_id,result,submit_solution.language,submit_solution.problem_code,submit_solution.time_stamp,submit_solution.code,submit_solution.extension)

		else:
			pass