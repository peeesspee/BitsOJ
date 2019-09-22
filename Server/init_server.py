# This class reads server configuration file and initializes server's variables
class initialize_server():
	superuser_username = 'BitsOJ'
	superuser_password = 'root'
	judge_username = 'judge1'
	judge_password = 'judge1'
	host = 'localhost'
	login_allowed_flag = False
	submission_allowed_flag = False

	def get_login_flag():
		if(initialize_server.login_allowed_flag == 'True'):
			return True
		else:
			return False
		

	def get_submission_flag():
		if(initialize_server.submission_allowed_flag == 'True'):
			return True
		else:
			return False
		

	def get_superuser_details():
		return initialize_server.superuser_username, initialize_server.superuser_password

	def get_judge_details():
		return initialize_server.judge_username, initialize_server.judge_password

	def get_host():
		return initialize_server.host

	def read_file():
		data_list = []
		print('[ READ ] config.cfg')
		config_file = open('config.cfg', 'r')
		config_file.readline()
		for data in config_file:
			data = data[data.find("'")+1:-1]
			data = data[:data.find("'")]
			data_list.append(data)
		
		initialize_server.superuser_username = data_list[0]
		initialize_server.superuser_password = data_list[1]
		initialize_server.judge_username = data_list[2]
		initialize_server.judge_password = data_list[3]
		initialize_server.host = data_list[4]
		initialize_server.login_allowed_flag = data_list[5]
		initialize_server.submission_allowed_flag = data_list[6]
		return