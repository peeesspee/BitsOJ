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
			    "Server IP": "192.168.20.31",
			    "Judge Username": "judge1",
			    "Judge Password": "judge1",
			    "Admin Password": "root",
			    "Login Allowed": "True",
			    "Judge Login Allowed": "True",
			    "Submission Allowed": "True",
			    "Scoreboard Update Allowed": "True",
			    "Judge Key": "hw0pmpznmkm451m",
			    "Client Key": "qmaa4nwmc724eky",
			    "File Password": "md056rz96r",
			    "Contest Name": "Kodeathon A7",
			    "Contest Theme": "Testing",
			    "Contest Duration": "02:00:00",
			    "Contest Status": "SETUP",
			    "Contest Start Time": "00:00:00",
			    "Contest End Time": "00:00:00",
			    "Contest Set Time": 0,
			    "Problem Codes": "('PIK', 'TFG', 'TFT', 'LGN', 'TRI', 'IRY')",
			    "Languages": "('C', 'C++', 'PYTHON-2', 'PYTHON-3')",
			    "Ranking Algorithm": "IOI",
			    "AC Points": 100,
			    "Penalty Score": -20,
			    "Penalty Time": 20,
			    "Manual Review": "False",
			    "Submission Time Limit": 0,
			    "Number Of Problems": "6",
			    "Problems": {
			        "Problem 1": {
			            "Title": "Plots in Kashmir ",
			            "Code": "PIK",
			            "Time Limit": 1,
			            "Author": "Atharva",
			            "Statement": "Since Article 370 of the Indian constitution is abrogated, you are trying to buy a plot in Jammu and Kashmir. You have been given a graph with four nodes each representing four most famous places of Jammu and Kashmir. Your friend wants you to take her to those four most famous places so she asked you to buy the plot from where each of the places are easily accessible. The distance between the first and third, second and fourth nodes are equal.You have to find a node which is equally far away from each given pair of opposite nodes.",
			            "Input Format": "    \u2022 The first line takes in the number of test cases\n    \u2022 Each of the next 4 lines take 2 space separated integers X and Y, each denoting the coordinates of the nodes on the graph, in any order.",
			            "Output Format": "Print a single line containing 2 space separated numbers, with 2 decimal digit precision, denoting the coordinate of the node which satisfies the mentioned condition.",
			            "Constraints": "    \u2022 1 \u2264 T \u22641000\n    \u2022 -1000000 \u2264 X,Y \u2264 1000000",
			            "Example Input": "1\n0 2\n-2 0\n0 -2\n2 0",
			            "Example Output": "0 0",
			            "IO Files": 1
			        },
			        "Problem 2": {
			            "Title": "Frequency Game",
			            "Code": "TFG",
			            "Time Limit": 1,
			            "Author": "Soham",
			            "Statement": "Gandhiji and Nehruji are playing a game. In this game Nehruji gives Gandhiji N natural numbers and asks him to calculate the frequency of each distinct number. Once Gandhiji finds out the frequency of each element, he has to check how many elements have the same frequency and print each frequency along with the elements having that frequency in ascending order. Gandhiji is busy in organising the Quit India movement, so he wants your help in solving this question.",
			            "Input Format": "    \u2022 The first line takes T, the number of test cases.\n    \u2022 The next line takes N, the number of elements in the sequence.\n    \u2022 Next line contains N space separated numbers, Ai...n .",
			            "Output Format": "Print each frequency followed by the element having that frequency on the next line. The frequencies and the elements having the frequency both must be in ascending order.",
			            "Constraints": "1 < T < 100\n1 < Ai < 10^9\n1 < N , 10^5",
			            "Example Input": "1\n7\n1 1 1 2 2 3 3",
			            "Example Output": "2\n2 3\n3\n1",
			            "IO Files": 1
			        },
			        "Problem 3": {
			            "Title": "The Fight against Terror",
			            "Code": "TFT",
			            "Time Limit": 1,
			            "Author": "Sachinam",
			            "Statement": "The brave soldiers of India guard our borders 24x7 against threats to national security. To aid them in the cause, our intelligence agency, Research and Analysis Wing, listens for all possible sources of terror. Recently, they received some encrypted coordinates of terror camps. However, the encryption key is hidden inside a string S, which is known.\nS contains only digits from 0 to 9. The hidden key is the maximum sum that can be formed by \ninserting \u2018+\u2019 sign in between the characters of S and evaluating the resulting expression.\nYou can add as many \u2018+\u2019 signs as possible,possibly 0, just keeping in mind that no two \u2018+\u2019 signs are consecutive.\nCan you help our agents in cracking the code?",
			            "Input Format": "Single String S",
			            "Output Format": "Print the sum of the evaluated value over all possible formulas.",
			            "Constraints": "    \u2022 1\u2264|S|\u226410\n    \u2022 All letters in S are digits between \u20181\u2019 and \u20189\u2019, inclusive.",
			            "Example Input": "132",
			            "Example Output": "186",
			            "IO Files": 4
			        },
			        "Problem 4": {
			            "Title": "Lagaan",
			            "Code": "LGN",
			            "Time Limit": 1,
			            "Author": "Valiant1",
			            "Statement": "In one of the small towns of India, during the height of the British Raj in the 1800s, the East India Company has imposed high tariffs on people from the local villages. Unable to pay such huge amounts, they gather in the community hall to request the EIC captain, Andrew Russell to decrease their tariffs.\nRussell, being a cunning officer, hatches a new plan to loot the poor population. He thus proposes a new taxation scheme as follows:\n    \u2022 People have to pay X amount of tariff for the first month.\n    \u2022 For next T1 months, they have to pay one unit more tariff than the previous month.\nSo, if they paid X unit of tariff in the first month, they have to pay X+1 tariff next month, for T1 months.\n    \u2022 For next T2 months, they pay double the amount of tariffs paid last month, for T2 months.\n    \u2022 After this time, they have to pay a charge amounting to product of tariffs for K previous months.\n\nHe proposes a very small value for the first month, which makes the villagers very happy. But Bhuvan, a sensible youth of the village sees through Russell's plan at once. \nThe na\u00efve villagers obviously oppose his pleas to reject the scheme.\nCan you help Bhuvan to show the long term mal-consequences to the villagers, by calculating the tariffs for  month, where N may be very large?\nNote: Since the value of tariffs may be too large, find the answer modulo  10^9 + 7",
			            "Input Format": "    \u2022 The first line contains T, the number of test cases.\n    \u2022 Each of the next T lines contain the following data: X T1 T2 K N\nN : The month for which you have to calculate the tariffs.",
			            "Output Format": "For each test case, output the tariff for Nth  month, modulo 10^9+7, in a new line each.",
			            "Constraints": "1 \u2264 T \u2264 5\n1 \u2264 X, T1, T2 \u2264 50\n1 \u2264 K \u2264 T1 + T2 + 1\n1 \u2264 N \u2264 10^9",
			            "Example Input": "2\n1 5 5 2 5\n1 5 5 2 20",
			            "Example Output": "6\n75821660",
			            "IO Files": 1
			        },
			        "Problem 5": {
			            "Title": "Tricolor",
			            "Code": "TRI",
			            "Time Limit": 1,
			            "Author": "Sachinam",
			            "Statement": "On the occasion of our Independence Day, prime minister Narendra Modi is set to hoist our national flag at the Red Fort. The ceremony is being efficiently organised by the government officials. They want the flag support to be in the form of a pyramid with N steps. The step contains 2i-1 blocks, depicted as follows:\n\nEach block has X number of flowers on it. The number of flowers follows a very special procedure:\n    \u2022 The bottom most step has 2N-1 flowers, which is a permutation of 1 to 2N-1\n    \u2022 At any level other than the bottom most one, the number of flowers in the block is the median of the number of flowers in the three blocks directly under it (Below-left, Below, Below-Right).\nGiven the number of flowers in each of the bottom most blocks, find the number of flowers in the top most block.",
			            "Input Format": "    \u2022 The first line contains N, the number of steps.\n    \u2022 The next line contains 2N-1 integers Ai...n, which denote the number of flowers in the bottom most blocks.",
			            "Output Format": "Print the number of flowers in the top most step.",
			            "Constraints": "2 <= N <= 10^5\nAi is a permutation of 1\u2026..2N-1.",
			            "Example Input": "3\n1 3 2 4 5",
			            "Example Output": "3",
			            "IO Files": 5
			        },
			        "Problem 6": {
			            "Title": "Independent Ryuk",
			            "Code": "IRY",
			            "Time Limit": 1,
			            "Author": "Valiant1",
			            "Statement": "On Independence Day, Light Yagami gave N apples to Ryuk. For every apple i, Ryuk knows the amount of energy E[i] the apple initially contains. Taking one bite from an apple decreases the energy of apple by 1. Ryuk can only take one bite from an apple in one day, but can take as many bite(s) as he can from different apples on the same day. Ryuk plans to last the apples at most K days . For each day i, Light tells Ryuk A[i], the number of apples he can take bite(s) from. Being the friend of Ryuk, can you find a strategy of eating apples in order to maximize the number of days the apples can last. Ryuk will stop after the day i when he can\u2019t take bite(s) from A[i] apples.",
			            "Input Format": "    \u2022 The first line contains T ,the no. of test cases. \n    \u2022 The second line contains two integers N and K . \n    \u2022 The third line contains N integers representing the initial energies of apples.\n    \u2022 Next line contains K integers representing the number of apples Ryuk is required to eat.",
			            "Output Format": "Print a single integer denoting the number of maximum days the apples can last. ",
			            "Constraints": "    \u2022 1\u2264 T \u2264 10\n    \u2022 1\u2264 N,K \u2264 10^5 \n    \u2022 1\u2264 E[i],A[i] \u2264  10^5",
			            "Example Input": "1\n4 5\n1 2 5 4\n1 2 3 4 3",
			            "Example Output": "4",
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


