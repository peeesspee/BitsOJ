# Special thanks to www.pythonspot.com for this!
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import *
from ui_widgets import *
import time, string, random, shutil, json, os

class main_window(QWizard):
	def __init__(
			self, 
			config, 
			available_width, 
			available_height, 
			key,
			parent=None
		):
		super(main_window, self).__init__(parent)
		self.setWindowIcon(QIcon('Elements/logo.png'))
		self.config = config

		self.hardcode_key = key

		self.available_width = available_width
		self.available_height = available_height

		self.selected_languages = {}
		languages = self.config.get("Languages", ['C'])
		allowed_languages = self.config.get("Allowed Languages", ['C'])
		for language in languages:
			if language in allowed_languages:
				self.selected_languages[language] = "TRUE"
			else:
				self.selected_languages[language] = "FALSE"

		self.ranklist_states = {}
		ranklists = self.config.get("Available Ranklists", ["IOI"])
		config_selected_rankist = self.config.get("Selected Ranklist", "IOI")
		for ranklist in ranklists:
			if ranklist == config_selected_rankist:
				self.ranklist_states[ranklist] = "TRUE"
			else:
				self.ranklist_states[ranklist] = "FALSE"

		self.problems = self.config.get('Problems', {})
		self.problem_codes = []
		self.number_of_problems = self.config.get('Number Of Problems', 0)

		self.home_page = wizard_page(config, 1)
		self.addPage(self.home_page)
		self.contest_page = wizard_page(config, 2)
		self.addPage(self.contest_page)
		self.rabbitmq_page = wizard_page(config, 3)
		self.addPage(self.rabbitmq_page)
		self.problems_page = wizard_page(config, 4)
		self.addPage(self.problems_page)
		self.languages_page = wizard_page(config, 5)
		self.addPage(self.languages_page)
		self.ranking_page = wizard_page(config, 6)
		self.addPage(self.ranking_page)
		self.all_done_page = wizard_page(config, 7)
		self.addPage(self.all_done_page)
		
		self.setWindowTitle("BitsOJ v1.1 [ CONTEST SETUP ]")
		self.setFixedSize(1200, 750)

		self.currentIdChanged.connect(self.page_changed_handler)

	def page_changed_handler(self, page):
		if page == -1:
			print('[ SETUP ] Cancelled')
		elif page == 0:
			print('[ SETUP ] Home')
		elif page == 1:
			print('[ SETUP ] Contest Settings')
		elif page == 2:
			print('[ SETUP ] RabbitMQ Configuration')
		elif page == 3:
			print('[ SETUP ] Problems')
		elif page == 4:
			print('[ SETUP ] Language')
		elif page == 5:
			print('[ SETUP ] Ranking')
		elif page == 6:
			# Do final config creation here
			print('[ SETUP ] Updating self configuration file...')
			self.write_changes()
			print('[ SETUP ] Generating Server data...')
			self.generate_server_config()
			print('[ SETUP ] Generating Client data...')
			self.generate_client_config()
			print('[ SETUP ] Generating Judge data...')
			self.generate_judge_config()
			print('[ SETUP ] Copying Problem data...')
			self.copy_problems()
			print('[ SETUP ] Encrypting Client configs...')
			exit_code = self.encrypt_client_configs()
			if exit_code == 0:
				print('[ SETUP ] Process Completed')
			else:
				print('[ SETUP ] Client configurations could not be encrypted. Restart setup.')

	def write_changes(self):
		# RabbitMQ Page Data
		self.config['Server Username'] = self.field("Server_Username")
		self.config['Server Password'] = self.field("Server_Password")
		self.config['Client Username'] = self.field("Client_Username")
		self.config['Client Password'] = self.field("Client_Password")
		self.config['Judge Username'] = self.field("Judge_Username")
		self.config['Judge Password'] = self.field("Judge_Password")
		self.config['Host'] = self.field("Host")

		# Contest settings Page Data
		self.config['Contest Name'] = self.field("Contest_Name")
		self.config['Contest Theme'] = self.field("Contest_Theme")
		self.config['Admin Key'] = self.field("Admin_Key")

		# Problems Page Data
		self.config['Problems'] = self.problems
		self.config['Number Of Problems'] = len(self.problems)
		self.config['Problem Codes'] = self.problem_codes
		for i in range(len(self.problems)):
			problem_code = self.problems['Problem ' + str(i + 1)]['Code']
			self.problem_codes.append(problem_code)
		
		# Languages Page Data
		allowed_languages = []
		for language in self.config["Languages"]:
			if self.selected_languages[language] == "TRUE":
				allowed_languages.append(language)
		self.config['Allowed Languages'] = allowed_languages

		# Ranklist Page Data
		for ranklist in self.config["Ranking Styles"]:
			if self.ranklist_states[ranklist] == "TRUE":
				self.config['Selected Ranklist'] = ranklist
				break
		problem_max_score = self.field("Problem_Score")
		penalty_score = self.field("Penalty_Score")
		penalty_time = self.field("Penalty_Time")
		self.config['Problem Max Score'] = int(problem_max_score)
		self.config['Penalty Score'] = int(penalty_score)
		self.config['Penalty Time'] = int(penalty_time)

		# Client and Judge Keys
		chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
		client_key = ''.join(random.choice(chars) for _ in range(7))
		judge_key = ''.join(random.choice(chars) for _ in range(15))
		contest_key = ''.join(random.choice(chars) for _ in range(15))
		self.config['Client Key'] = client_key
		self.config['Judge Key'] = judge_key
		self.config['Contest Key'] = contest_key

		try:
			content = json.dumps(self.config, indent = 4)
			with open('config.json', 'w') as file:
				file.write(content)
		except Exception as error:
			print('[ ERROR ] File could not be written: ', error)

	def generate_server_config(self):
		config = {
			"Server Username": "",
			"Server Password": "",
			"Server IP": "",
			"Admin Password": "",
			"Login Allowed": False,
			"Judge Login Allowed": True,
			"Submission Allowed": False,
			"Scoreboard Update Allowed": True,
			"Judge Key": "",
			"Client Key": "",
			"File Password": "",
			"Contest Name": "",
			"Contest Theme": "",
			"Contest Duration": "00:00:00",
			"Contest Status": "SETUP",
			"Contest Start Time": "00:00:00",
			"Contest End Time": "00:00:00",
			"Contest Set Time": 0,
			"Problem Codes": [],
			"Languages": [],
			"Ranking Algorithm": "",
			"AC Points": 0,
			"Penalty Score": 0,
			"Penalty Time": 0,
			"Manual Review": False,
			"Submission Time Limit": 0,
			"Number Of Problems": 0,
			"Problems": {}
		}
		
		config['Server Username'] = self.config['Server Username']
		config['Server Password'] = self.config['Server Password']
		config['Server IP'] = self.config['Host']
		config['Admin Password'] = self.config['Admin Key']
		config['Judge Key'] = self.config['Judge Key']
		config['Client Key'] = self.config['Client Key']
		config['File Password'] = self.config['Contest Key']
		config['Contest Name'] = self.config['Contest Name']
		config['Contest Theme'] = self.config['Contest Theme']
		config['Problem Codes'] = self.config['Problem Codes']
		config['Languages'] = self.config['Allowed Languages']
		config['Ranking Algorithm'] = self.config['Selected Ranklist']
		config['AC Points'] = self.config['Problem Max Score']
		config['Penalty Score'] = self.config['Penalty Score']
		config['Penalty Time'] = self.config['Penalty Time']
		config['Problems'] = self.config['Problems']

		self.server_config = config

		try:
			content = json.dumps(config, indent = 4)
			with open('./Contest_Data/Server/config.json', 'w') as file:
				file.write(content)
		except Exception as error:
			print('[ ERROR ] Server File could not be written: ', error)

	def generate_client_config(self):
		# DEFAULT Config
		config = {
			"rabbitmq_username": "",
			"rabbitmq_password": "",
			"host": "",
			"client_id": "",
			"client_key": "",
			"Username" : "",
			"Problem Key" : "",
			"Contest": "START",
			"Duration": "00:00:00",
			"Start Time": 0,
			"End Time": 0,
			"Contest Name": "",
			"Contest Theme": "",
			"Languages": "('C', 'C++', 'PYTHON-3', 'JAVA')",
			"No_of_Problems": "",
			"Problems": {},
			"Code": {}
		}
		
		config['rabbitmq_username'] = self.config['Client Username']
		config['rabbitmq_password'] = self.config['Client Password']
		config['host'] = self.config['Host']
		config['client_id'] = 'NUL'
		config['client_key'] = self.config['Client Key']
		config['Username'] = 'NUL'
		config['Problem Key'] = self.config['Contest Key']
		config['Contest Name'] = self.config['Contest Name']
		config['Contest Theme'] = self.config['Contest Theme']
		config['Languages'] = str(self.config['Allowed Languages'])
		# Problem codes are in list of string,
		# convert them to required format(dict):
		# "ABC": "Problem 1",
		problem_codes_list = self.config['Problem Codes']
		formatted_dict = {}
		for i in range(len(problem_codes_list)):
			problem_code = problem_codes_list[i]
			formatted_dict[problem_code] = 'Problem ' + str(i+1)
		config['Code'] = formatted_dict

		# Convert problems to required format ( Dict of lists )
		# Problems{
		#	"Problem 1": [
		#		"Problem Name",
		#		"Problem Code",
		#		"Time Limit"
		#	]
		# }
		new_problem_dict = {}
		i = 1	# Counter
		for problem in self.config['Problems'].keys():
			problem_name = self.config['Problems'][problem]['Name']
			problem_code = self.config['Problems'][problem]['Code']
			time_limit = self.config['Problems'][problem]['Time Limit']
			new_problem_list = []
			new_problem_list.append(problem_name)
			new_problem_list.append(problem_code)
			new_problem_list.append(time_limit)
			new_problem_dict['Problem ' + str(i)] = new_problem_list
			i += 1
		config['Problems'] = new_problem_dict
		config['No_of_Problems'] = i - 1

		self.client_config = config

		try:
			content = json.dumps(config, indent = 4)
			# Make this config accessible later on for tweaking
			self.client_config_content = content
			with open('./Contest_Data/Client/decrypted_config.json', 'w') as file:
				file.write(content)
		except Exception as error:
			print('[ ERROR ] Client File could not be written: ', error)

	def generate_judge_config(self):
		# DEFAULT Config
		config = {
			"rabbitmq_username": "", 
			"rabbitmq_password": "", 
			"host_ip": "localhost", 
			"key": "", 
			"processlimit": "500", 
			"Number of Problems": "0", 
			"Problems": {},  # Same as client
			"Problem Codes": "('ABC')", 	# Same as client
			"Code Time Limit": {"ABC": 1}, # This one's tricky :|
			"Username": "NUL", 
			"Password": "NUL", 
			"ID": "NUL"
		}
		config['rabbitmq_username'] = self.config['Judge Username']
		config['rabbitmq_password'] = self.config['Judge Password']
		config['host_ip'] = self.config['Host']
		config['key'] = self.config['Judge Key']

		# Problems in reuquired format
		all_problem_dict = {}
		i = 1	# Counter
		for problem in self.config['Problems'].keys():
			problem_name = self.config['Problems'][problem]['Name']
			problem_code = self.config['Problems'][problem]['Code']
			time_limit = self.config['Problems'][problem]['Time Limit']
			new_problem_dict = {}
			new_problem_dict['Title'] = problem_name
			new_problem_dict['Code'] = problem_code
			new_problem_dict['Time Limit'] = int(time_limit)

			all_problem_dict['Problem ' + str(i)] = new_problem_dict
			i += 1
		config['Problems'] = all_problem_dict
		config['Number of Problems'] = str(i - 1)

		# Problem codes in reuquired format
		config['Problem Codes'] = str(self.config['Problem Codes'])

		# Code Time Limit
		problem_codes_list = self.config['Problem Codes']
		formatted_dict = {}
		for i in range(len(problem_codes_list)):
			problem_id = 'Problem ' + str(i+1)
			problem_code = problem_codes_list[i]
			# Get time limit of this problem code:
			problem_time_limit = self.config['Problems'][problem_id]['Time Limit']
			formatted_dict[problem_code] = int(problem_time_limit)
		config['Code Time Limit'] = formatted_dict

		self.judge_config = config

		try:
			content = json.dumps(config, indent = 4)
			with open('./Contest_Data/Judge/config.json', 'w') as file:
				file.write(content)
		except Exception as error:
			print('[ ERROR ] Client File could not be written: ', error)

	def copy_problems(self):
		try:
			# Copy test cases in Server and Judge
			shutil.rmtree('./Contest_Data/Server/Problem Data')
			shutil.rmtree('./Contest_Data/Judge/problems')
			
			shutil.copytree('./Problems', './Contest_Data/Server/Problem Data')
			shutil.copytree('./Problems', './Contest_Data/Judge/problems')

			# Copy problem json data in Client
			for problem_key, problem_value in self.config['Problems'].items():
				print('[ WRITE ] ' , problem_key)
				# Make problem json
				filename = problem_key.replace(' ', '_')

				# 'problem_value' is our original problem dict
				# we have to tweak some keys a bit
				problem_value['Problem Name'] = problem_value['Name']
				problem_value['Problem Code'] = problem_value['Code']
				
				temp = problem_value.pop('Name', 'NULL')
				temp = problem_value.pop('Code', 'NULL')

				problem_value = json.dumps(problem_value, indent = 4)
				# ENCRYPT HERE
				file_content = problem_value
				
				with open('./Contest_Data/Client/Problems/' + filename + '.json', 'w+') as file:
					file.write(file_content)

		except Exception as error:
			print('[ ERROR ] Could not copy problem data: ', error)
		finally:
			return
	
	def encrypt_client_configs(self):
		# Encrypt client config.json
		# Content in self.client_config_content
		client_config_encrypted = self.encryptDecrypt(
			str(self.client_config), 
			self.hardcode_key
		)
		# Remove unencrypted config
		os.remove('./Contest_Data/Client/decrypted_config.json')
		# Write new config file
		with open('./Contest_Data/Client/config.json', 'w+') as file:
			json.dump(client_config_encrypted, file, indent = 4)

		# Re check encrypted config
		try:
			with open('./Contest_Data/Client/config.json', 'r') as file:
				client_config_encrypted = json.load(file)

			client_config_decrypted = self.encryptDecrypt(
				client_config_encrypted, 
				self.hardcode_key
			)
			client_config_decrypted = eval(client_config_decrypted)
			
			if self.client_config != client_config_decrypted:
				print('[ CRITICAL ] Error occured while encrypting client config.json! Restart setup.')
				return 1
		except:
			return 1

		# Encrypt problem content
		file_key = self.server_config['File Password']
		folder_path = './Contest_Data/Client/Problems/'
		for file_name in os.listdir(folder_path):
			# Read file
			with open(folder_path + file_name, 'r') as file:
				data = json.load(file)
			data = str(data)

			# Encrypt Key
			encrypted_data = self.encryptDecrypt(data, file_key)

			# Write file
			with open(folder_path + file_name, 'w+') as file:
				json.dump(encrypted_data, file, indent = 4)

			# Check by re-decrypting
			with open(folder_path + file_name, 'r') as file:
				encrypted_data = json.load(file)
				new_data = self.encryptDecrypt(encrypted_data, file_key)
				if new_data != data:
					print('[ CRITICAL ] Error occured in encryption of file data.')
					return 1

			# Encrypted
			print('\t> ', file_name, '  [ ENCRYPTED ]')

		return 0

	def encryptDecrypt(self, inpString, xorKey): 
		length = len(inpString)
		for i in range(length):
			inpString = (inpString[:i] + chr(ord(inpString[i]) ^ ord(xorKey[i%len(xorKey)])) + inpString[i+1 : ])
		return inpString