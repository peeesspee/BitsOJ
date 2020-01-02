import json 
import time
# This class reads server configuration file and initializes server's variables
class initialize_server():
	file_password = '0000'
	duration = '02:00'	#Default Value
	config = ''

	def get_password():
		initialize_server.read_config()
		return initialize_server.file_password

	def get_duration():
		initialize_server.read_config()
		return initialize_server.duration
		
	# Read Server config file 
	def read_config():
		# print('\n[ READ ] config.json')
		with open("config.json", "r") as read_json:
			config = json.load(read_json)
		initialize_server.config = config

		# Basic credentials for login to RabbitMQ Server
		initialize_server.duration = config["Contest Duration"]
		initialize_server.file_password = config["File Password"]
		initialize_server.config = config
		return config

	def convert_to_seconds(time_str):
		try:
			h, m, s = time_str.split(':')
			return int(h) * 3600 + int(m) * 60 + int(s)
		except:
			print('[ ERROR ] Could not convert time to seconds: Time was: ' + time_str)
			return -1

	def convert_to_hhmmss(seconds):
		try:
			seconds = int(seconds)
			h = int(seconds / 3600)
			m = int((seconds % 3600) / 60)
			s = int(((seconds % 3600) % 60))
			if h <= 9:
				h = '0' + str(h)
			if m <= 9:
				m = '0' + str(m)
			if s <= 9:
				s = '0' + str(s)
			return str(h) + ':' + str(m) + ':' + str(s)
		except:
			print('[ ERROR ] Could not convert time to HH:MM:SS format.')
			return '00:00:00'

	def get_time_difference(time1, time2):
		# Return difference between time2 and time1 in hhmmss format
		time1_s = initialize_server.convert_to_seconds(time1)
		time2_s = initialize_server.convert_to_seconds(time2)
		if time2_s < time1_s:
			time2_s = time2_s + 86400
		return initialize_server.convert_to_hhmmss(
				time2_s - time1_s 
			)

	def get_abs_time_difference(time1, time2):
		# Return difference between time2 and time1 in hhmmss format
		time1_s = initialize_server.convert_to_seconds(time1)
		time2_s = initialize_server.convert_to_seconds(time2)
		if time1_s >= time2_s:
			val = time1_s - time2_s
		else:
			val = time2_s - time1_s
		return val

	def get_remaining_time():
		initialize_server.read_config()
		current_time = initialize_server.convert_to_seconds(time.strftime("%H:%M:%S", time.localtime()))
		contest_end_time = initialize_server.convert_to_seconds(initialize_server.config["Contest End Time"])
		diff = contest_end_time - current_time
		return time.strftime("%H:%M:%S", time.gmtime(diff))

	def get_start_time():
		initialize_server.read_config()
		return initialize_server.config['Contest Start Time']

	def get_duration():
		initialize_server.read_config()
		return initialize_server.config['Contest Duration']

	def get_end_time():
		initialize_server.read_config()
		return initialize_server.config['Contest End Time']

	def get_problem_details(problem_code):
		try:
			problems = initialize_server.config['Problems']
			for problem, content in problems.items():
				if content['Code'] == problem_code:
					return content
			return 'NULL'
		except Exception as error:
			print('[ ERROR ] ' + str(error))
			return 'NULL'


class save_status():
	def write_config():
		print('\n[ WRITE ] config.json')		
		json_data = {
			    "Server Username": "BitsOJ",
			    "Server Password": "root",
			    "Server IP": "localhost",
			    "Judge Username": "judge1",
			    "Judge Password": "judge1",
			    "Admin Password" : "",
			    "Login Allowed": "True",
			    "Judge Login Allowed": "True",
			    "Submission Allowed": "True",
			    "Scoreboard Update Allowed": "True",
			    "Judge Key": "000000000000000",
			    "Client Key": "000000000000000",
			    "File Password": "papa",
			    "Contest Duration": "02:00:00",
			    "Contest Status": "SETUP",
			    "Contest Start Time": "00:00:00",
			    "Contest End Time": "00:00:00",
			    "Contest Set Time": 0,
			    "Problem Codes": "('SAC', 'TPH', 'TFS', 'TAM', 'ANS')",
			    "Languages": "('C','C++','JAVA','PYTHON-2')",
			    "Ranking Algorithm": "IOI",
			    "AC Points": 100,
			    "Penalty Score": -20,
			    "Penalty Time": 20,
			    "Manual Review": "False",
			    "Submission Time Limit": 0,
			    "Number Of Problems": "5",
			    "Problems": {
			        "Problem 1": {
			            "Title": "The Pursuit of Happyness",
			            "Code": "TPH",
			            "Time Limit": 1,
			            "Author": "Prakhar",
			            "Statement": "This is a long, long story of a boy named Harry!",
			            "Input Format": "First line has test cases, each of the following T lines are cases.",
			            "Output Format": "Print each answer in a separate line.",
			            "Constraints": "1 \u2264 N \u2264 1000",
			            "Example Input": "1 2",
			            "Example Output": "3",
			            "IO Files": 1
			        },
			        "Problem 2": {
			            "Title": "The Fight for Survival",
			            "Code": "TFS",
			            "Time Limit": 1,
			            "Author": "Prakhar",
			            "Statement": "This is a long, long story of a girl\nnamed Hermione!",
			            "Input Format": "First line has test cases, each of the following T lines are cases.",
			            "Output Format": "Print each answer in a separate line.",
			            "Constraints": "1 N 1000",
			            "Example Input": "1 2",
			            "Example Output": "3",
			            "IO Files": 1
			        },
			        "Problem 3": {
			            "Title": "The Triwizard Cup",
			            "Code": "SAC2",
			            "Time Limit": "2",
			            "Author": "Remus",
			            "Statement": "This is a long, long story of a boy\nnamed Ronald Weasley. :)",
			            "Input Format": "First line has test cases, each of the following T lines are cases.",
			            "Output Format": "Print each answer in a separate line.",
			            "Constraints": "1 \u2264 N  \u2265 1000",
			            "Example Input": "1\n2",
			            "Example Output": "3",
			            "IO Files": 1
			        },
			        "Problem 4": {
			            "Title": "The Accio Magic",
			            "Code": "TAM",
			            "Time Limit": 1,
			            "Author": "Sirius",
			            "Statement": "This is a long, long story of a boy\nnamed Neville!",
			            "Input Format": "First line has test cases, each of the following T lines are cases.",
			            "Output Format": "Print each answer in a separate line.",
			            "Constraints": "1 N 1000",
			            "Example Input": "1 2",
			            "Example Output": "3",
			            "IO Files": 1
			        },
			        "Problem 5": {
			            "Title": "The Big Elemental",
			            "Code": "TBE",
			            "Time Limit": 1,
			            "Author": "James",
			            "Statement": "This is a long, long story of a girl\nnamed Ginny!",
			            "Input Format": "First line has test cases, each of the following T lines are cases.",
			            "Output Format": "Print each answer in a separate line.",
			            "Constraints": "1 N \u2264 1000",
			            "Example Input": "1 2",
			            "Example Output": "3",
			            "IO Files": 1
			        }
			    }
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

	def update_problem_content(code, key, value):
		try:
			problems_content = initialize_server.config['Problems']
			for problem, content in problems_content.items():
				if content['Code'] == code:
					# Match found
					content[key] = value
					break
			initialize_server.config['Problems'] = problems_content
			with open("config.json", "w") as data_file:
				json.dump(initialize_server.config, data_file, indent=4)

			return 0
		except Exception as error:
			print('[ ERROR ] Could not update problem: ' + str(error))
			return 1


