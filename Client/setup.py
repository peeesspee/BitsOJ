import json

class inittialize_client():

	def setting_client():
		# Don't Change the order of any data
		rabbitmq_username = input('Enter rabbitmq client username : ')
		rabbitmq_password = input('Enter rbbitmq client password : ')
		host = input('Enter host IP : ')

		No_of_Problems = int(input('Enter Number of Problems to be added : '))
		Problems = {}

		for i in range(No_of_Problems):
			problem_name = input('Enter Problem file name : ')
			problem_code = input('Enter Problem Code : ')
			Problems[problem_name] = problem_code

		json_data = {'client_id' : '','client_key' : '139728abcder65bf', 'rabbitmq_username' : rabbitmq_username, 'rabbitmq_password' : rabbitmq_password,'host' : host, 'No_of_Problems' : No_of_Problems, 'Problems' : Problems}
		with open("config.json", "w") as data_file:
			json.dump(json_data, data_file, indent=4)


