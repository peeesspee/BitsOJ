import pika

class submit_solution():
	code = ''
	file_path = ''
	Language = {1 : 'C', 2 : 'C++', 3 : 'Python', 4 : 'Java'}
	Problem_Code = { 1 : 'PSP'}
	final_data = ''
	selected_language = ''
	selected_problem = ''


	def read_solution(client_id,username,channel):
		try:
			submit_solution.file_path = input('Enter path of solution : ')
			submit_solution.code = open(submit_solution.file_path, 'r').read() 
			for i,k in submit_solution.Language:
				print(i,k)
			submit_solution.selected_language = input('Select language : ')
			submit_solution.selected_language = str(Language[int(submit_solution.selected_language)])
			for i,k in submit_solution.Problem_Code:
				print(i,k)
			submit_solution.selected_problem = input('Select Problem : ')
			submit_solution.selected_problem = str(Problem_Code[int(submit_solution.selected_problem)])
			submit_solution.solution_request(submit_solution.code,client_id,username,submit_solution.selected_language,submit_solution.selected_problem,channel)
		except:
			print("File Not Found ------ Try Again")
			submit_solution.read_solution()

	def solution_request(code,client_id,username,language,problem_code,channel):
		submit_solution.final_data = 'Submt ' + client_id + ' '  + problem_code + ' ' + language + ' ' + code
		channel.basic_publish(exchange = 'credential_manager', routing_key = 'login_requests', body = submit_solution.final_data)
		print('Your Code is running ......')
		channel.basic_consume(queue = username, on_message_callback =submit_solution.server_response_handler , auto_ack = True)


	def server_response_handler(ch,method,properties,body):
		submission_result = body.decode('utf-8')
		status = submission_result[0:5]
		print(status)
		if (status == 'Vrdct'):
			pass
		else:
			pass