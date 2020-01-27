import json 
import time
# Shamelessly copied from Server :P
class init_setup():
	# Read Setup config file 
	def read_config():
		# print('\n[ READ ] config.json')
		with open("config.json", "r") as read_json:
			config = json.load(read_json)
		init_setup.config = config
		return config

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
				init_setup.duration = new_value
		except Exception as error:
			print('[ ERROR ] Could not update json file : ' + str(error))
		finally:
			return

	# def update_problem_content(code, key, value):
	# 	try:
	# 		problems_content = init_setup.config['Problems']
	# 		for problem, content in problems_content.items():
	# 			if content['Code'] == code:
	# 				# Match found
	# 				content[key] = value
	# 				break
	# 		init_setup.config['Problems'] = problems_content
	# 		with open("config.json", "w") as data_file:
	# 			json.dump(init_setup.config, data_file, indent=4)

	# 		return 0
	# 	except Exception as error:
	# 		print('[ ERROR ] Could not update problem: ' + str(error))
	# 		return 1