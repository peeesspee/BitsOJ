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


# if __name__=='__main__':
# 	initialize_judge.show_config()
