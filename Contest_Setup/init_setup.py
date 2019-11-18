import json

class read_write():

	def read_json():
		with open('test_case.json', 'r') as read:
			data = json.load(read)

		return data


	def write_json(data):
		with open('test_case.json', 'w') as write:
			json.dump(data, write , indent = 4)