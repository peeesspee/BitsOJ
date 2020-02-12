import json 
import time
# Shamelessly copied from Server :P
class init_setup():
	# Read Setup config file 
	def read_config():
		try:
			with open("config.json", "r") as read_json:
				config = json.load(read_json)
			init_setup.config = config
			return config
		except:
			return {}