from database_management import submission_management, query_management
from login import authenticate_login
import pika
import json
import sys
import time
from datetime import date,datetime
from init_client import initialize_contest, handle_config

class start_listening():
	# client_id, username = authenticate_login.get_user_details()
	channel = None
	connection = None
	cursor = None
	host = None
	login_status = False 
	data_changed_flags = ''
	queue = ''
	scoreboard = ''

	def listen_server(rabbitmq_username,rabbitmq_password,cursor,host,data_changed_flags2,queue,scoreboard):
		try:
			creds = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
			params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
			connection = pika.BlockingConnection(params)
			channel = connection.channel()
			start_listening.channel = channel
			start_listening.connection = connection
			start_listening.cursor = cursor
			start_listening.host = host
			start_listening.data_changed_flags = data_changed_flags2
			start_listening.queue = queue
			start_listening.scoreboard = scoreboard


			start_listening.channel.basic_consume(
				queue = authenticate_login.username,
				on_message_callback = start_listening.server_response_handler,
				auto_ack = True,
				exclusive = True
				)
			start_listening.channel.start_consuming()
		except (KeyboardInterrupt, SystemExit):
			print('[ DELETE ] Queue ' + authenticate_login.username + ' deleted...')
			print("[ STOP ] Keyboard interrupt")
		finally:
			start_listening.channel.stop_consuming()
			start_listening.channel.queue_delete(authenticate_login.username)
			start_listening.connection.close()
			
	
			


	def server_response_handler(ch,method,properties,body):
		server_data = str(body.decode("utf-8"))
		json_data = json.loads(server_data)
		code = json_data["Code"]
		if code == 'VRDCT':
			status = json_data['Status']
			run_id = json_data['Run ID']
			message = json_data['Message']
			local_id = json_data["Local Run ID"]
			print("[ Status ] " + status + "\n[ Run ID ] : " + str(run_id) + "\n[ Message ] : " + message)
			start_listening.submission_verdict(json_data)
		elif code == 'QUERY':
			start_listening.query_verdict(json_data)
		elif code == 'SRJCT':
			# print(json_data)
			start_listening.rejected(json_data)
			start_listening.queue.put(json_data["Message"])
			start_listening.data_changed_flags[3] = 1
		elif code == "SCRBD":
			start_listening.leaderboard(json_data)
		elif code == "START":
			start_listening.start_status(json_data)
		elif code == "STOP":
			start_listening.stop_status(json_data)
		elif code == "DSCNT":
			start_listening.disconnect(json_data)
		elif code == "UPDATE":
			pass
		elif code == 'EXTND':
			start_listening.extended_time(json_data)
		elif code == 'EDIT':
			start_listening.edit_problem(json_data)
		elif code == 'BLOCK':
			start_listening.user_blocked(json_data)
		elif code == 'RESPONSE':
			start_listening.run_id_update(json_data)
		elif code == 'SHUTDOWN':
			raise(KeyboardInterrupt)
		else:
			print(code)
			print("WRONG INPUT")


	def run_id_update(server_data):
		print(server_data)
		submission_management.update_run_id(server_data["Local Run ID"],server_data["Run ID"])
		start_listening.data_changed_flags[9] = 1


	def rejected(server_data):
		submission_management.update_verdict_reject(server_data["Local Run ID"])
		start_listening.data_changed_flags[9] = 1

	def user_blocked(server_data):
		start_listening.channel.stop_consuming()
		start_listening.data_changed_flags[8] = 1



	def edit_problem(server_data):
		config = handle_config.read_config_json()
		problem_no = config["Code"][server_data["Problem Code"]]
		try:
			with open('./Problems/Problem_' + problem_no[-1:-2:-1] + '.json','r') as write:
				problem_file = json.load(write)
			problem_file = handle_config.encryptDecrypt(problem_file)
			problem_file = eval(problem_file)
		except Exception as Error:
			print(str(Error))
		problem_file[server_data["Type"]] = server_data["Data"]
		try:
			problem_file = str(problem_file)
			problem_file = handle_config.encryptDecrypt(problem_file)
			with open('./Problems/Problem_' + problem_no[-1:-2:-1] + '.json','w') as write:
				json.dump(problem_file, write, indent = 4)
		except Exception as Error:
			print(str(Error))
		start_listening.queue.put(problem_no)
		start_listening.data_changed_flags[7] = 1


	def extended_time(server_data):
		config = handle_config.read_config_json()
		time = server_data["Time"]
		config["End Time"] = config["End Time"] + time*60
		handle_config.write_config_json(config)
		start_listening.data_changed_flags[4] = 3


	def leaderboard(server_data):
		data = server_data["Data"]
		data = json.dumps(server_data)
		start_listening.scoreboard.put(data)

	def submission_verdict(server_data):
		run_id = str(server_data["Run ID"])
		code_result = server_data["Status"]
		message = server_data["Message"]
		local_id = server_data["Local Run ID"]
		print('[ Run ID : ' + run_id + ' ] [ Result : ' + code_result + ' ] [ error : ' + message + ' ]')
		submission_management.update_verdict(
			local_id,
			authenticate_login.client_id,
			run_id,
			code_result,
			)
		start_listening.data_changed_flags[1] = 2


	def query_verdict(server_data):
		print(server_data)
		client_id = server_data["Client ID"]
		query = server_data["Query"]
		response = server_data["Response"]
		Type = server_data["Type"]
		print("[QUERY] Response received")
		query_management.update_query(
			client_id,
			query,
			response,
			Type,
			)
		start_listening.data_changed_flags[2] = 2

	def convert_time_format(start_time):
		today = date.today()
		current_date = today.strftime("%d/%m/%Y")
		current_date = current_date + ' ' + start_time
		d = datetime.strptime(current_date,"%d/%m/%Y %H:%M:%S")
		return time.mktime(d.timetuple())


	def start_status(server_data):
		print(server_data)
		contest_start_time = time.time()
		# start_time = start_listening.convert_time_format(server_data["Start Time"])
		print('start time',contest_start_time)
		config = handle_config.read_config_json()
		config["Duration"] = server_data["Duration"]
		config["Contest"] = "RUNNING"
		config["Problem Key"] = server_data["Problem Key"]
		# contest_start_time = start_time
		config["Start Time"] = contest_start_time
		initialize_contest.set_duration(config["Duration"])
		contest_duration_seconds = initialize_contest.convert_to_seconds(initialize_contest.get_duration())
		config["End Time"] = contest_duration_seconds + contest_start_time
		handle_config.write_config_json(config)
		start_listening.data_changed_flags[0] =1
		start_listening.data_changed_flags[4] =2
		print("[START] Signal received")
		print("Contest Duration : " + server_data["Duration"])

	def stop_status(server_data):
		start_listening.data_changed_flags[0] = 3
		print("[STOP] Signal received")

	def disconnect(server_data):
		print('[ DSCNT ]', server_data)
		if server_data["Client"] == 'All':
			start_listening.channel.stop_consuming()
			start_listening.data_changed_flags[5] = 2
		else:
			print('[ SELF DSCNT ]')
			config = handle_config.read_config_json()
			if config["Username"] == server_data["Client"]:
				start_listening.channel.stop_consuming()
				start_listening.data_changed_flags[5] = 1

