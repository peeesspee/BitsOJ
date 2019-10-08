import json

# This class reads server configuration file and initializes server's variables
class initialize_server():
	superuser_username = 'BitsOJ'
	superuser_password = 'root'
	judge_username = 'judge1'
	judge_password = 'judge1'
	host = 'localhost'
	login_allowed_flag = False
	submission_allowed_flag = False
	client_key = '000000000000000'
	judge_key = '000000000000000'

	def get_keys():
		return initialize_server.client_key, initialize_server.judge_key

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

	# Read Server config file 
	def read_config():
		print('[ READ ] config.json')
		with open("config.json", "r") as read_json:
			config = json.load(read_json)

		# Basic credentials for login to RabbitMQ Server
		initialize_server.superuser_username = config["Server Username"]
		initialize_server.superuser_password = config["Server Password"]
		initialize_server.host = config["Server IP"]
		initialize_server.judge_username = config["Judge Username"]
		initialize_server.judge_password = config["Judge Password"]
		initialize_server.login_allowed_flag = config["Login Allowed"]
		initialize_server.submission_allowed_flag = config["Submission Allowed"]
		initialize_server.judge_key = config["Judge Key"]
		initialize_server.client_key = config["Client Key"]
		return

	# To be moved to setup.py
	def write_config():
		print('[ WRITE ] config.json')

		rabbitmq_username = 'BitsOJ'
		rabbitmq_password = 'root'
		host = 'localhost'
		judge_username = 'judge1'
		judge_password = 'judge1'
		allow_login = 'True'
		allow_submission = 'True'
		judge_key = 'ahSuuiWQ12SthD1'
		client_key = '1sadHGAD379qKKq'
				

		json_data = {
		'Server Username' : rabbitmq_username, 
		'Server Password' : rabbitmq_password, 
		'Server IP' : host,
		'Judge Username' : judge_username,
		'Judge Password' : judge_password,
		'Login Allowed' : allow_login,
		'Submission Allowed' : allow_submission,
		'Judge Key' : judge_key,
		'Client Key' : client_key
		}

		with open("config.json", "w") as data_file:
			json.dump(json_data, data_file, indent=4)