import sqlite3
import sys
import random
import string



global client_id_counter
global query_id_counter

class manage_database():
	cur = None
	conn = None
	def initialize_database():
		try:
			conn = sqlite3.connect('server_database.db', check_same_thread = False)
			cur = conn.cursor()
			manage_database.cur = cur
			manage_database.conn = conn
		except Exception as error:
			print ("[ CRITICAL ERROR ]Database connection error : " + str(error))
		
		try:	
			cur.execute("create table if not exists accounts(user_name varchar2(10) PRIMARY KEY, password varchar2(15), client_type varchar2(10))")
			cur.execute("create table if not exists connected_clients(client_id integer PRIMARY KEY, user_name varchar2(10), password varchar2(10), state varchar2(15))")
			cur.execute("create table if not exists connected_judges(judge_id varchar2(10), user_name varchar2(10), password varchar2(10), state varchar2(15))")
			cur.execute("create table if not exists submissions(run_id integer PRIMARY KEY, client_run_id integer, client_id integer, language varchar2(3), source_file varchar2(30),problem_code varchar(10), verdict varchar2(5), timestamp text, sent_status varchar2(15) DEFAULT 'WAITING', judge varchar2(15) DEFAULT '-')")
			cur.execute("create table if not exists queries(query_id integer, client_id integer, query varchar2(550), response varchar2(550))")
			cur.execute("create table if not exists scoreboard(client_id integer PRIMARY KEY, user_name varchar2(10), score integer, problems_solved integer, total_time text)")
			cur.execute("create table if not exists problems(problem_name varchar2(30), problem_code varchar(10), test_files integer, time_limit integer)")
			
		except Exception as error:
			print("[ CRITICAL ERROR ] Table creation error : " + str(error))

		# try:
		# 	cur.execute("INSERT INTO problems VALUES(?, ?, ?, ?)", ('The Fight for Survival', 'TFS', 1, 1, ))
		# 	conn.commit()
		# except:
		# 	print('Errorororor')

		return conn, cur

	def reset_database(conn):
		cur = conn.cursor()
		try:
			cur.execute("drop table if exists accounts")
			cur.execute("drop table if exists submissions")
			cur.execute("drop table if exists scoreboard")
			cur.execute("drop table if exists connected_clients")
			cur.execute("drop table if exists connected_judges")
			cur.execute("drop table if exists queries")
			cur.execute("drop table if exists problems")
		except:
			print("[ CRITICAL ERROR ] Table drop error")

	def get_cursor():
		return manage_database.cur

	def get_connection_object():
		return manage_database.conn

class problem_management(manage_database):
	def init_problems(problem_dictionary):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
		except Exception as error:
			print('[ CRITICAL ] Could not load problems! '  + str(error))
			return

		try:
			cur.execute('DELETE FROM problems')
		except:
			print('[ ERROR ] Could not refresh problems!')
			return

		try:
			for problem, content in problem_dictionary.items():
				problem_name = content['Title']
				problem_code = content['Code']
				problem_time = content['Time Limit']
				files = content['IO Files']
				cur.execute(
					"INSERT INTO problems VALUES(?, ?, ?, ?)",
					(problem_name, problem_code, files, problem_time, )
				)
				conn.commit()
		except Exception as error:
			print('[ ERROR ] Corrupted config file: ' + str(error))
			
			cur.execute('rollback')
		return

	def update_problem(change_type, key, new_value):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			
			if change_type == 1:
				cur.execute("UPDATE problems SET problem_name = ? WHERE problem_code = ?", (new_value, key, ))
				conn.commit()
			elif change_type == 2:
				cur.execute("UPDATE problems SET problem_code = ? WHERE problem_code = ?", (new_value, key, ))
				conn.commit()
			elif change_type == 4:
				new_value = int(new_value)
				cur.execute("UPDATE problems SET time_limit = ? WHERE problem_code = ?", (new_value, key, ))
				conn.commit()
			return
		except Exception as error:
			print('[ ERROR ] Could not update database: ' + str(error))

class scoreboard_management():
	def insert_new_user(client_id, user_name, score, problems_solved, total_time):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("INSERT INTO scoreboard values(?, ?, ?, ?, ?)", (client_id, user_name, score, problems_solved, total_time, ))
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not add scoreboard entry : " + str(error))
			conn.rollback()
		return

	def get_scoreboard():
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT user_name, score, problems_solved, total_time FROM scoreboard")
			data = cur.fetchall()
			return data
		except Exception as error:
			print("[ CRITICAL ] Could not get scoreboard : " + str(error))
		return	

	def update_user_score(client_id, run_id, problem_max_score, problem_penalty, status, problem_code, time_stamp, ranking_algorithm):
		
		try:
			new_ac_submission = 0
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			# Get number of problems solved till now based on client_id
			cur.execute("SELECT DISTINCT problem_code FROM submissions WHERE client_id = ? AND verdict = 'AC'", (client_id, ))
			data = cur.fetchall()
			if data == None:
				problems_solved = 0
			else:
				problems_solved = len(data)


			# Get Previous score of the client
			cur.execute("SELECT score FROM scoreboard WHERE client_id = ?", (client_id, ))
			data = cur.fetchall()
			# Data can not be NONE (Guarenteed)
			if data == None: # Meh, Anyways 
				previous_score = 0
			else:
				previous_score = data[0][0]

			# Check if this verdict is a new AC or a pre-scored AC
			# So that score is not updated when user sends same AC code again.
			if status == 'AC':
				cur.execute(
					"SELECT * FROM submissions WHERE client_id = ? and problem_code = ? and verdict = 'AC'", 
					(client_id, problem_code, )
				)
				data = cur.fetchall()
				# If there is only one such entry, it means this is a new AC (The same AC that the entry was for)
				if data == None or len(data) == 1:
					score = problem_max_score
					new_ac_submission = 1
				else:
					# IGNORE this submission in leaderboard
					return

			elif status == 'CE':
				score = 0
			elif ranking_algorithm == 1:	# For ACM style contest, there is penalty
				score = problem_penalty
			else:							# For Long contest or IOI style contest, no penalty
				score = 0

			# Get Previous timestamp of the client
			cur.execute("SELECT timestamp FROM submissions WHERE run_id = ?", (run_id, ))
			data = cur.fetchall()
			# Data can not be NONE (Guarenteed)
			if data == None: # Meh, Anyways 
				previous_timestamp = '00:00:00'
			else:
				previous_timestamp = data[0][0]

		except Exception as error:
			print("[ ERROR ] Could Not Fetch data : " + str(error))
			return

		# If it is a new AC submission, total time taken by user is updated.
		if new_ac_submission == 1:
			updated_time_stamp = time_stamp
		else:
			updated_time_stamp = previous_timestamp

		new_score = previous_score + score
		
		try:
			print('[ SCOREBOARD ][ UPDATE ] Client: ' + str(client_id) + " Prev Score :" + str(previous_score) + " New Score:" + str(new_score))
			cur.execute(
				"UPDATE scoreboard SET score = ?, problems_solved = ?, total_time = ? WHERE client_id = ? ", 
				(new_score, problems_solved, updated_time_stamp, client_id)
			)
			conn.commit()

		except Exception as error:
			print('[ ERROR ][ CRITICAL ] Scoreboard could not be updated : ' + str(error))

		return


class previous_data(manage_database):
	def get_last_run_id():
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT max(run_id) FROM submissions")
			data =  cur.fetchall()

			if(data[0][0] == ''):
				return 0
			else:
				return int(data[0][0])
		except:
			print('[ INIT ] Run ID initialised to 0')
			return 0

	def get_last_client_id():
		global client_id_counter
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT max(client_id) FROM connected_clients")
			data =  cur.fetchall()
			if(data[0][0] != ''):
				client_id_counter = int(data[0][0])
			else:
				client_id_counter = 0

		except:
			print('[ INIT ] Client ID initialised to 0')
			client_id_counter = 0

	def get_last_query_id():
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT max(query_id) FROM queries")
			data =  cur.fetchall()
			if(data[0][0] == ''):
				return 0
			else:
				return int(data[0][0])
		except:
			print('[ INIT ] Query ID initialised to 0')
			return 0

			




class client_authentication(manage_database):
	#This function validates the (user_name, password, client_id) in the database.
	def validate_client(user_name, password):
		#Validate client in database
		cur = manage_database.get_cursor()
		cur.execute(
			"SELECT exists(SELECT * FROM accounts WHERE user_name = ? and password = ?)", 
			(user_name, password, )
		)
		validation_result = cur.fetchall()
		
		if validation_result[0][0] == 1:
			return True
		else:
			return False

	def validate_connected_client(user_name, client_id, session_key = 'None'):
		#Validate client in database
		cur = manage_database.get_cursor()
		cur.execute(
			"SELECT exists(SELECT * FROM connected_clients WHERE user_name = ? and client_id = ?)",
			(user_name, client_id, )
		)
		validation_result = cur.fetchall()
		
		if validation_result[0][0] == 1:
			return True
		else:
			return False
		return

	#This function generates a new client_id for new connections
	def generate_new_client_id():
		global client_id_counter
		client_id_counter = client_id_counter + 1
		client_id = int(client_id_counter)
		return client_id

	def add_client(client_id, user_name, password, state, table_name):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute(
				"INSERT INTO " + table_name + " values(?, ?, ?, ?)", 
				(client_id, user_name, password, state, )
			)
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not add client : " + str(error))
			conn.rollback()
		return	

		
	# Get client_id when user_name is known
	def get_client_id(user_name):
		try:
			cur = manage_database.get_cursor()
			cur.execute(
				"SELECT client_id FROM connected_clients WHERE user_name = ?", 
				(user_name, )
			)
			client_id = cur.fetchall()
			return client_id[0][0]
		except Exception as error:
			print("[ ERROR ] : The user does not have a client id yet.")

	# Get user_name when client_id is known
	def get_client_username(client_id):
		try:
			cur = manage_database.get_cursor()
			client_id = int(client_id)
			cur.execute("SELECT user_name FROM connected_clients WHERE client_id = ?", (client_id, ))
			client_username = cur.fetchall()
			return client_username[0][0]
		except Exception as error:
			print("[ ERROR ] : Could not fetch username.")
			return 'Null'

	# Check if a client with given client_id is connected in the system, and return its state
	def check_connected_client(user_name, table_name ):
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT * FROM " + table_name + " WHERE user_name = ?", (user_name,))
			result = cur.fetchall()
			# print('[ LOGIN ][ VALIDATION ] ' + str(user_name) + ' :: Status -> ' + str(result[0][3]))
			return result[0][3]
		except:
			# If user was not connected earlier, this exception will be raised
			return 'New'

	
class submissions_management(manage_database):
	def insert_submission(run_id, local_run_id, client_id, language, source_file_name, problem_code, verdict, timestamp):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		run_id = int(run_id)
		client_id = int(client_id)
		local_run_id = int(local_run_id)
		try:
			cur.execute("INSERT INTO submissions values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (run_id, local_run_id, client_id, language, source_file_name, problem_code, verdict, timestamp, 'WAITING', '-', ))
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not insert into submission : " + str(error))
		return

	def update_submission_status(run_id, verdict, sent_status, judge = '-'):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		run_id = int(run_id)
		try:
			cur.execute("UPDATE submissions SET verdict = ?, sent_status = ?, judge = ? WHERE run_id = ?", (verdict, sent_status, judge, run_id,))
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not update submission submission : " + str(error))
			conn.rollback()
		return

	def delete_all():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("DELETE FROM submissions")
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Database deletion error : " + str(error))

	def get_last_sub_time(client_id):
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT max(timestamp) FROM submissions WHERE client_id = ?" , (client_id,))
			data = cur.fetchall()
			if data[0][0] == None:
				return "NONE"
			else:
				return data[0][0]
		except Exception as error:
			return "NONE"

	def get_judge(run_id):
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT judge FROM submissions WHERE run_id = ?" , (run_id,))
			data = cur.fetchall()
			if data[0][0] == None:
				return "NONE"
			else:
				return data[0][0]
		except Exception as error:
			return "NONE"

	def get_local_run_id(run_id):
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT client_run_id FROM submissions WHERE run_id = ?" , (run_id,))
			data = cur.fetchall()
			if data[0][0] == None:
				return "NONE"
			else:
				return data[0][0]
		except Exception as error:
			return "NONE"

	def get_source_file_name(run_id):
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT source_file FROM submissions WHERE run_id = ?" , (run_id,))
			data = cur.fetchall()
			if data[0][0] == None:
				return "NONE"
			else:
				return data[0][0]
		except Exception as error:
			return "NONE"


class query_management(manage_database):
	def insert_query(query_id, client_id, query):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		try:
			cur.execute("INSERT INTO queries values(?, ?, ?, ?)", (query_id, client_id, query, 'TO BE ANSWERED', ))
			cur.execute('commit')
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not insert into submission : " + str(error))
		return

	def update_query(query_id, response):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		try:
			cur.execute("UPDATE queries SET response = ? WHERE query_id = ?", (response, query_id,))
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not insert into submission : " + str(error))
		return

	def delete_all():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("DELETE FROM queries")
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Database deletion error : " + str(error))


class user_management(manage_database):
	def generate_n_users(no_of_clients, no_of_judges, password_type):
		cur = manage_database.get_cursor()
		# Get max client and judge usernames till now
		try:
			cur.execute("SELECT max(user_name) from accounts where client_type = 'CLIENT'")
			max_client_username = int(cur.fetchall()[0][0][4:])
		except:
			max_client_username = 0

		try:
			cur.execute("SELECT max(user_name) from accounts where client_type = 'JUDGE'")
			max_judge_username = int(cur.fetchall()[0][0][5:])
		except:
			max_judge_username = 0
		
		client_list = user_management.generate_clients(no_of_clients, max_client_username)
		judge_list = user_management.generate_judges(no_of_judges, max_judge_username)
		client_pass_list = user_management.generate_passwords(max_client_username, no_of_clients, password_type)
		judge_pass_list = user_management.generate_passwords(max_judge_username, no_of_judges, password_type)

		# INSERTIONS INTO DATABASE [ CRITICAL SETION ]
		cur.execute("begin")
		try:
			for i in range(0, no_of_clients):
				cur.execute("INSERT into accounts values (?, ?, ? )" , (client_list[i], client_pass_list[i], 'CLIENT'))

			for i in range(0, no_of_judges):
				cur.execute("INSERT into accounts values (?, ?, ? )" , (judge_list[i], judge_pass_list[i], 'JUDGE'))

			cur.execute("commit")

		except:
			print('[ CRITICAL ] Database insertion error! Roll back')
			cur.execute("rollback")

		# INSERTION FINISHED
		return

	def generate_clients(no_of_clients, max_so_far):
		client_list = list()
		for i in range(max_so_far+1, max_so_far+no_of_clients+1):
			team_number = "{:05d}".format(i)
			client_list.append('team' + str(team_number))

		return client_list
	
	def generate_judges(no_of_judges, max_so_far):
		judge_list = list()
		for i in range(max_so_far+1, max_so_far+no_of_judges+1):
			judge_number = "{:05d}".format(i)
			judge_list.append('judge' + str(judge_number))
		return judge_list
		
	def generate_passwords(prev, number, type):
		password_list = list()
		chars=string.ascii_uppercase + string.digits+string.ascii_lowercase
		for i in range(0, number):
			if type == 'Simple':
				password = 'bits'+str(i + prev + 1)
			elif type == 'Random':
				password = ''.join(random.choice(chars) for _ in range(6))

			password_list.append(password)
		return password_list

	def delete_user(user_name):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			# Check if client is logged in : 
			# if client_authentication.check_connected_client(user_name) == 'Connected':
			# 	cur.execute("SELECT * FROM accounts WHERE user_name = ?", (user_name,))
			# 	data = cur.fetchall()
			# 	client_type = data[0][2]
			# 	if client_type == 'CLIENT':
			# 		print("[ DISCONNECT ] " + user_name)
			# 		cur.execute("UPDATE connected_clients SET state = 'Blocked' WHERE user_name = ?", (user_name, ))

			cur.execute("DELETE FROM accounts WHERE user_name = ?",(user_name,))
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Database deletion error : " + str(error))

	def delete_all():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("DELETE FROM accounts")
			cur.execute("DELETE FROM connected_clients")
			cur.execute("DELETE FROM connected_judges")
			cur.execute("DELETE FROM scoreboard")
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Database deletion error : " + str(error))

	def disconnect_all():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("UPDATE connected_clients SET state = 'Disconnected'")
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Database updation error : " + str(error))
			conn.rollback()
		finally:
			return

	def update_user_state(username, state):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("UPDATE connected_clients SET state = ? where user_name = ? ", (state, username, ))
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Database updation error : " + str(error))
			conn.rollback()
		finally:
			return
			
	def get_ac_count(problem_code):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			# cur.execute("SELECT DISTINCT client_id FROM submissions WHERE problem_code = ? and verdict = 'AC'", (problem_code, ))
			cur.execute("SELECT client_id FROM submissions WHERE problem_code = ? and verdict = 'AC'", (problem_code, ))
			data = cur.fetchall()
			if data == None:
				return 0
			else:
				return len(data)

		except Exception as error:
			print(str(error))
			return 0

			return
	def get_submission_count(problem_code):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("SELECT client_id FROM submissions WHERE problem_code = ?", (problem_code, ))
			data = cur.fetchall()
			if data == None:
				return 0
			else:
				return len(data)

		except Exception as error:
			print(str(error))
			return 0

	def get_participant_count():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("SELECT DISTINCT (client_id) FROM submissions")
			data = cur.fetchall()
			if data == None:
				return 0
			else:
				return len(data)

		except Exception as error:
			print(str(error))
			return 0

	def get_participant_pro_count():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("SELECT DISTINCT (client_id) FROM submissions WHERE verdict = 'AC'")
			data = cur.fetchall()
			if data == None:
				return 0
			else:
				return len(data)

		except Exception as error:
			print(str(error))
			return 0