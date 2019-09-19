import pika 
# from login import authenticate_login
# from manage_code import send_code

class send_options():
	channel = None
	host = None
	option_list = ['SUBMT', 'LOGIN', 'QUERY', 'RJDGE']

	def options(channel, host):
		send_options.channel = channel
		send_options.host = host
		for i in option_list:
			print(i)
		select_option = input('What do you want to do ? : ')
		if (select_option == 'LOGIN'):
			authenticate_login.login(channel,host)
		elif (select_option == 'SUBMT'):
			send_code.uploading_solution(channel)
		elif (select_option == 'QUERY'):
			print("Work in progress")
		elif (select_option == 'RJDGE'):
			print("Work in progress")
		else:
			print('Wrong option selected')
			optinons(channel,host)


	def publish_data(channel):

		# sending username and password to the server
		authenticate_login.channel.basic_publish(
			exchange = 'connection_manager', 
			routing_key = 'client_requests', 
			body = 'LOGIN ' + authenticate_login.username + ' ' + password + ' ' + authenticate_login.client_id + ' CLIENT'
			)