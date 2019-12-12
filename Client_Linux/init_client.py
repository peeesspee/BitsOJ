import json
from PyQt5.QtWidgets import *

##########################################################################
##########################################################################


class initialize_contest():
	duration = '00:00:00'
	contest_set_time = None

	def get_duration():
		return initialize_contest.duration

	def set_duration(data):
		initialize_contest.duration = data

	def convert_to_seconds(data):
		h, m, s = data.split(':')
		return int(h) * 3600 + int(m) * 60 + int(s)

	def contest_end_time():
		with open('config.json', 'r') as contest:
			config = json.load(contest)
		initialize_contest.contest_set_time = config["End Time"]

	def return_contest_end_time():
		return initialize_contest.contest_set_time
		
#############################################################################
#############################################################################

#############################################################################
#############################################################################

class handle_config():
	def read_config_json():
		try:
			with open('config.json', 'r') as read_config:
				data = json.load(read_config)
			return data
		except Exception as Error:
			print(str(Error))

	def read_config_string():
		with open('config.json', 'r') as read_config:
			data = json.loads(read_config)

		return data

	def write_config_json(data):
		with open('config.json', 'w') as write_config:
			json.dump(data, write_config, indent=4)

	def read_score_json():
		try:
			with open('score.json', 'r') as read_score:
				data = json.load(read_score)
		except:
			data = None

		return data

	def write_score_json(data):
		with open('score.json', 'w') as write_score:
			json.dump(data,write_score, indent = 4)

################################################################################
################################################################################

################################################################################
################################################################################

class rabbitmq_detail():
	rabbitmq_username = None
	rabbitmq_password = None
	host = None

	def fill_detail(username,password,host):
		rabbitmq_detail.rabbitmq_username = username
		rabbitmq_detail.rabbitmq_password = password
		rabbitmq_detail.host = host

	def get_host():
		return rabbitmq_detail.host

################################################################################
################################################################################

################################################################################
################################################################################

class user_detail():
	client_id = 'Nul'
	username = None

	def insert_detail(client_id,username):
		user_detail.client_id = client_id
		user_detail.username = username

	def get_user_details():
		return user_detail.client_id,user_detail.username

##################################################################################
##################################################################################