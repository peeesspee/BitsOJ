import json
import socket

class initialize_judge():
	rabbitmq_username = 'Nul'
	rabbitmq_password = 'Nul'
	host_ip = 'Nul'
	key = 'Nul'
	processlimit = 'Nul'

	def read_config():
		with open("./config.json",'r') as read_json:
			config = json.load(read_json)
			initialize_judge.rabbitmq_username = config["rabbitmq_username"]
			initialize_judge.rabbitmq_password = config["rabbitmq_password"]
			initialize_judge.host_ip = config["host_ip"]
			initialize_judge.key = config["key"]
			initialize_judge.processlimit = config["processlimit"]

	def key():
		with open("./config.json",'r') as read_json:
			config = json.load(read_json)
			return config["key"]

	def my_ip():
		hostname = socket.gethostname()
		IPAddr = socket.gethostbyname(hostname)
		return IPAddr


	def show_config():
		with open("./config.json",'r') as read_json:
			config = json.load(read_json)
			print(eval(config["Problem Codes"])[3])
			for i in eval(config["Problem Codes"]):
				print(i)
			print("config is ->\n",type(config))

	def save_details(username, password, judge_id):
		with open("./config.json",'r') as read_json:
			config = json.load(read_json)
			config['Username'] = username
			config['Password'] = password
			config['ID'] = judge_id
			config = json.dumps(config)
		with open("./config.json", "w") as file:
			file.write(config)

	def get_credentials():
		with open("./config.json",'r') as read_json:
			config = json.load(read_json)
			try:
				return config['Username'], config['Password'], config['ID'] 
			except:
				return 'NULL', 'NULL', 'NULL'
