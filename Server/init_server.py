import json 
 
# This class reads server configuration file and initializes server's variables
class initialize_server():
	superuser_username = 'BitsOJ'
	superuser_password = 'root'
	judge_username = 'judge1'
	judge_password = 'judge1'
	host = 'localhost'
	login_allowed_flag = 'False'
	submission_allowed_flag = 'False'
	client_key = '000000000000000'
	judge_key = '000000000000000'
	file_password = '0000'

	def get_password():
		return initialize_server.file_password

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
		initialize_server.file_password = config["File Password"]
		return config

	# To be moved to setup.py
class save_status():
	def write_config(rabbitmq_username, rabbitmq_password, judge_username, judge_password, host, allow_login, allow_submission, client_key, judge_key, file_password, contest_duration):
		print('[ WRITE ] config.json')

		allow_login = str(allow_login)
		allow_submission = str(allow_submission) 
				
		json_data = {
		'Server Username' : rabbitmq_username, 
		'Server Password' : rabbitmq_password, 
		'Server IP' : host,
		'Judge Username' : judge_username,
		'Judge Password' : judge_password,
		'Login Allowed' : allow_login,
		'Submission Allowed' : allow_submission,
		'Judge Key' : judge_key,
		'Client Key' : client_key,
		'File Password' : file_password,
		'Contest Duration' : contest_duration
		}

		with open("config.json", "w") as data_file:
			json.dump(json_data, data_file, indent=4)

	def update_entry(entry, new_value):
		print('[ UPDATE ] ' + str(entry) + ':' + str(new_value))
		try:
			with open("config.json", "r") as read_json:
				config = json.load(read_json)
		except Exception  as error:
			print("[ ERROR ] Could not read json file : "  + str(error))
			return
		
		try:
			config[entry] = new_value
			print('[ WRITE ] config.json')
			# config = json.dumps(config)
			with open("config.json", "w") as data_file:
				json.dump(config, data_file, indent=4)
		except Exception as error:
			print('[ ERROR ] Could not update json file : ' + str(error))
		finally:
			return


