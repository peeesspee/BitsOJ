import json 
import time
# This class reads server configuration file and initializes server's variables
class initialize_server():
	file_password = '0000'
	duration = '02:00'	#Default Value
	config = ''

	def get_password():
		return initialize_server.file_password
	def get_duration():
		return initialize_server.duration


	# Read Server config file 
	def read_config():
		print('\n[ READ ] config.json')
		with open("config.json", "r") as read_json:
			config = json.load(read_json)
		initialize_server.config = config

		# Basic credentials for login to RabbitMQ Server
		initialize_server.duration = config["Contest Duration"]
		initialize_server.file_password = config["File Password"]
		initialize_server.config = config
		return config

	def convert_to_seconds(time_str):
		print(time_str)
		h, m, s = time_str.split(':')
		return int(h) * 3600 + int(m) * 60 + int(s)

	def get_remaining_time():
		current_time = initialize_server.convert_to_seconds(time.strftime("%H:%M:%S", time.localtime()))
		contest_end_time = initialize_server.convert_to_seconds(initialize_server.config["Contest End Time"])
		diff = contest_end_time - current_time
		return time.strftime("%H:%M:%S", time.gmtime(diff))

	def get_start_time():
		return initialize_server.config['Contest Start Time']

	def get_end_time():
		return initialize_server.config['Contest End Time']

class save_status():
	def write_config(
		rabbitmq_username, rabbitmq_password, judge_username, judge_password,
		host, allow_login, allow_judge, allow_submission, allow_scoreboard,
		client_key, judge_key, file_password, contest_duration, status,
		contest_start_time, contest_end_time, contest_set_time
		):

		print('\n[ WRITE ] config.json')

		allow_login = str(allow_login)
		allow_submission = str(allow_submission) 
				
		json_data = {
		'Server Username' : rabbitmq_username, 
		'Server Password' : rabbitmq_password, 
		'Server IP' : host,
		'Judge Username' : judge_username,
		'Judge Password' : judge_password,
		'Login Allowed' : allow_login,
		'Judge Login Allowed' : allow_judge,
		'Submission Allowed' : allow_submission,
		'Scoreboard Update Allowed': allow_scoreboard,
		'Judge Key' : judge_key,
		'Client Key' : client_key,
		'File Password' : file_password,
		'Contest Duration' : contest_duration,
		'Contest Status': status,
    	'Contest Start Time': contest_start_time,
    	'Contest End Time': contest_end_time,
    	'Contest Set Time' : contest_set_time,
    	'Number Of Problems' : '5',
    	'Problems': {
	        "Problem 1": "('The Begining of the End','TBE', 1, 1)",
	        "Problem 2": "('Privet Drive','PD', 1, 1)",
	        "Problem 3": "('Dumbledores Cloak','DC', 1, 1)",
	        "Problem 4": "('The Auror Mania','TAM', 1, 1)",
	        "Problem 5": "('A New Start','ANS', 1, 1)"
    	},
    	"Problem Codes" : "('TBE', 'PD', 'DC', 'TAM', 'ANS')",
    	'Languages': "('C','C++','JAVA','PYTHON-2')",
    	"Ranking Algorithm" : "IOI",
    	"AC Points" : 100,
    	"Penalty Score" : -20,
    	"Penalty Time" : 20,
    	"Manual Review" : "False"
		}

		with open("config.json", "w") as data_file:
			json.dump(json_data, data_file, indent=4)


	def update_entry(entry, new_value):
		print('\n[ UPDATE ] ' + str(entry) + ':' + str(new_value))
		try:
			with open("config.json", "r") as read_json:
				config = json.load(read_json)
		except Exception  as error:
			print("[ ERROR ] Could not read json file : "  + str(error))
			return
		
		try:
			config[entry] = new_value
			print('[ WRITE ] config.json')
			with open("config.json", "w") as data_file:
				json.dump(config, data_file, indent=4)
			if entry == "Contest Duration":
				initialize_server.duration = new_value
		except Exception as error:
			print('[ ERROR ] Could not update json file : ' + str(error))
		finally:
			return


