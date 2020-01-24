import sqlite3
import sys
import random
import string
import os
  
global client_id_counter

class manage_database():
	cur = None
	conn = None
	def initialize_database():
		try:
			conn = sqlite3.connect(
				'server_database.db', 
				check_same_thread = False,
				timeout = 20
			)
			cur = conn.cursor()
			manage_database.cur = cur
			manage_database.conn = conn
		except Exception as error:
			print ("[ CRITICAL ERROR ]Database connection error : " + str(error))
		
		try:	
			cur.execute("create table if not exists accounts(user_name varchar2(10) PRIMARY KEY, password varchar2(15), client_type varchar2(10))")
			cur.execute("create table if not exists connected_clients(client_id integer PRIMARY KEY, user_name varchar2(10), password varchar2(10), ip varchar2(16) DEFAULT '0.0.0.0', state varchar2(15))")
			cur.execute("create table if not exists connected_judges(judge_id varchar2(10), user_name varchar2(10), password varchar2(10), ip varchar2(16) DEFAULT '0.0.0.0', state varchar2(15))")
			cur.execute("create table if not exists submissions(run_id integer PRIMARY KEY, client_run_id integer, client_id integer, language varchar2(3), source_file varchar2(30),problem_code varchar(10), verdict varchar2(5), timestamp text, sent_status varchar2(15) DEFAULT 'WAITING', judge varchar2(15) DEFAULT '-', score integer DEFAULT 0)")
			cur.execute("create table if not exists queries(query_id integer, client_id integer, query varchar2(550), response varchar2(550))")
			cur.execute("create table if not exists scoreboard(client_id integer PRIMARY KEY, user_name varchar2(10), score integer, problems_solved integer, total_time text, penalty integer, is_hidden text DEFAULT 'False')")
			cur.execute("create table if not exists problems(problem_name varchar2(30), problem_code varchar(10), test_files integer, time_limit integer)")

		except Exception as error:
			print("[ DB ][ CRITICAL ERROR ] Table creation error : " + str(error))

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
			print("[ DB ][ CRITICAL ] Table drop error")

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
			print('[ DB ][ CRITICAL ] Could not load problems! '  + str(error))
			return

		try:
			cur.execute('DELETE FROM problems')
		except:
			print('[ DB ][ ERROR ] Could not refresh problems!')
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
			print('[ DB ][ ERROR ] Corrupted config file: ' + str(error))
			
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
			print('[ DB ][ ERROR ] Could not update database: ' + str(error))

class scoreboard_management():
	def insert_new_user(client_id, user_name, score, problems_solved, total_time):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("INSERT INTO scoreboard values(?, ?, ?, ?, ?, ?, ?)", 
				(client_id, user_name, score, problems_solved, total_time, 0, 'False'))
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Could not add scoreboard entry : " + str(error))
			conn.rollback()
		return

	def get_scoreboard():
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT user_name, score, problems_solved, total_time FROM scoreboard ORDER BY score DESC, total_time ASC")
			data = cur.fetchall()
			return data
		except Exception as error:
			print("[ DB ][ CRITICAL ] Could not get scoreboard : " + str(error))
		return	

	def get_user_score(username):
		try:
			cur = manage_database.get_cursor()
			cur.execute(
				"SELECT user_name, score, problems_solved, total_time FROM scoreboard WHERE user_name = ?",
				(
					username,
				)
			)
			data = cur.fetchall()
			return data
		except Exception as error:
			print("[ DB ][ CRITICAL ] Could not get scoreboard : " + str(error))
		return	

	def delete_all():
		try:
			cur = manage_database.get_cursor()
			cur.execute("DELETE FROM scoreboard")
			cur.execute('commit')
		except:
			print("[ DB ][ CRITICAL ] Could not reset scoreboard : " + str(error))


	def update_user_score(
			client_id,
			run_id, 
			problem_max_score, 
			penalty_score, 
			penalty_time, 
			status, 
			problem_code, 
			time_stamp, 
			ranking_algorithm
		):
		problem_max_score = int(problem_max_score)
		# scoreboard(client_id user_name score problems_solved total_time penalty) <- Here, score is total score
		# submissions(run_id client_run_id client_id language source_file problem_code) 
		# verdict timestamp sent_status judge score) <- This score is submission score
		if ranking_algorithm == 1:
			# ACM style ranklist
			# For every unsolved problem, if it is a wrong answer, penalty of penalty_time is added 
			# For every unsolved problem, the first AC submission time is recorded 
			# along with all the penalties for the solved problems.
			try:
				pass
			except Exception as error:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print('[ DB ][ CRITICAL ][ SCOREBOARD ] Updation error: ' + str(error) + 'On ', exc_type, fname, exc_tb.tb_lineno)
			finally:
				return
		elif ranking_algorithm == 2 or ranking_algorithm == 3:
			print('\n[ SCOREBOARD ] Checking new submission...')
			# IOI style ranklist
			# For every unsolved problem, if there is a wrong answer, no penalty is issued
			# If there is an AC submission, then problem_max_score is issued to the problem.
			# If there is an AC submission for an already solved problem, no points are issued.
			# Tie breaker is done through total time taken to solve the problems. 
			# Minimum time is preferred.

			# LONG style ranklist
			# No penalty for wrong answers, and no tie breaker 

			# No logical difference between LONG and IOI styles, so their algo is same
			# Only that we do not consider time in LONG style

			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			try:
				# Get number of problems solved till now based on client_id
				cur.execute(
				"SELECT DISTINCT problem_code FROM submissions WHERE client_id = ? AND verdict = 'AC'",
					(
						client_id, 
					)
				)
				data = cur.fetchall()
				if data == None:
					problems_solved = 0
				else:
					problems_solved = len(data)

				print('[ SCOREBOARD ] Client: ', client_id, ' Problems Solved: ', problems_solved)

				# Get Previous total score of the client
				cur.execute("SELECT score FROM scoreboard WHERE client_id = ?", (client_id, ))
				data = cur.fetchall()
				if data == None or len(data) == 0: 
					previous_total_score = 0
				else:
					previous_total_score = int(data[0][0])

				print('[ SCOREBOARD ] Run: ', run_id, ' Previous Score: ', previous_total_score)

				# Get Previous problem score of the run_id
				cur.execute("SELECT score FROM submissions WHERE run_id = ?", (run_id, ))
				data = cur.fetchall()
				# Data can not be NONE (Guarenteed)
				if data == None or len(data) == 0: 
					print('[ DB ][ ERROR ] No submission data found!')
					return
				else:
					previous_score = int(data[0][0])

				print('[ SCOREBOARD ] Run: ', run_id, ' Previous RunID Score: ', previous_score)


				# Check if this is an AC submission, and if it is the first AC of this problem
				if status == 'AC':
					print('[ SCOREBOARD ] Run: ', run_id, ' This is an AC submission.')
					cur.execute(
						"SELECT run_id FROM submissions WHERE client_id = ? and problem_code = ? and verdict = 'AC' and score = ?",
						(
							client_id,
							problem_code,
							problem_max_score,
						)
					)
					data = cur.fetchall()
					number_of_submissions = len(data)
					if number_of_submissions > 0:
						previous_scored_run_id = int(data[0][0])

					print(
						'[ SCOREBOARD ] Client: ', 
						client_id, 
						' Number of Scored AC Submissions: ', 
						number_of_submissions
					)
					# If the problem has not been solved yet, ie, number_of_submissions = 0
					if number_of_submissions == 0:
						print('[ SCOREBOARD ][ RUN ', run_id, ' ][ PASS ] New AC')
						
						new_total_score = previous_total_score + problem_max_score

						# THIS ASSERTION SHOULD NEVER OCCUR, BUT IT IS THERE AS A FAILSAFE
						# Assert new_total_score should not be greater than 
						# problem_solve_count * problem_max_score
						if new_total_score > problem_max_score * problems_solved:
							print('[ DB ][ SCOREBOARD ][ SECURITY ] Client Total Score error')
							print('[ DB ][ SCOREBOARD ][ SECURITY ] Run ID: ', run_id)
							print('[ DB ][ SCOREBOARD ][ SECURITY ] Client ID: ', client_id)
							new_total_score = problem_max_score * problems_solved 
							print('[ DB ][ SCOREBOARD ][ SECURITY ] Total Score RESET to ', new_total_score)

						print(
							'[ SCOREBOARD ][ UPDATE ] Client: ' 
							+ str(client_id) 
							+ " Prev Score :" 
							+ str(previous_total_score) 
							+ " New Score:" 
							+ str(new_total_score)
						)
						# Set this submission as SCORED
						cur.execute(
							"UPDATE submissions SET score = ? WHERE run_id = ? ", 
							(
								problem_max_score,
								run_id,
							)
						)
						conn.commit()
						# Update scoreboard score
						cur.execute(
							"UPDATE scoreboard SET score = ?, problems_solved = ?, total_time = ? WHERE client_id = ? ", 
							(
								new_total_score, 
								problems_solved, 
								time_stamp, 
								client_id,
							)
						)
						conn.commit()
						
					elif number_of_submissions > 0 and run_id < previous_scored_run_id:
						# If this AC is for a submission with lower RunID for the same problem,
						# If so, then time is updated but score is not
				
						# Update Scoreboard timestamp
						print('[ SCOREBOARD ][ RUN ' + str(run_id) + ' ][ PASS ] This AC has a lower Timestamp than the previous one.')
						# Set this runid score to max
						print('[ SCOREBOARD ][ RUN ' + str(run_id) + ' ] Score: ', problem_max_score)
						cur.execute(
							"UPDATE submissions SET score = ? WHERE run_id = ? ", 
							(
								problem_max_score,
								run_id,
							)
						)
						conn.commit()
						# Set previous runid score to 0
						print('[ SCOREBOARD ][ RUN ' + str(previous_scored_run_id) + ' ] Score: ', 0)
						cur.execute(
							"UPDATE submissions SET score = ? WHERE run_id = ? ", 
							(
								0,
								previous_scored_run_id,
							)
						)
						conn.commit()
						# Get last timestamp
						cur.execute(
							"SELECT timestamp FROM submissions WHERE client_id = ? and verdict = 'AC' and score > 0 ORDER BY run_id DESC", 
							(
								client_id, 
							)
						)
						data = cur.fetchall()
						previous_timestamp = data[0][0]
						# Update leaderboard timestamp
						cur.execute(
							"UPDATE scoreboard SET total_time = ? WHERE client_id = ? ", 
							(
								previous_timestamp,
								client_id,
							)
						)
						conn.commit()


					else:
						print('[ SCOREBOARD ][ RUN ' + str(run_id) + ' ][ FAIL ] Already received AC Verdict on this problem.')
						# Set this problem score to 0 ( not SCORED )
						cur.execute(
							"UPDATE submissions SET score = ? WHERE run_id = ? ", 
							(
								0,
								run_id,
							)
						)
						conn.commit()
						return

				elif status != 'AC':
					print('[ SCOREBOARD ] Run: ', run_id, ' This is NOT an AC submission.')
					# If status is not AC
					# Check if the client had recieved AC verdict earlier?
					# If verdict is not AC but RUN SCORE is non zero, then this score
					# must be removed

					# Also check if client has already solved this problem based on another run id?
					# If so, then we do not decrease his score					
					if previous_score == problem_max_score:
						print('[ SCOREBOARD ] Run: ', run_id, ' This RunID was an AC submission earlier.')
						# Check if there is any other submission which can take its place?
						cur.execute(
							"SELECT run_id FROM submissions WHERE client_id = ? and problem_code = ? and verdict = 'AC' and score = ? ORDER BY timestamp ASC",
							(
								client_id,
								problem_code,
								0,
							)
						)
						data = cur.fetchall()
						previous_ac_submission_count = len(data)
						# We can make the oldest submission AC now.

						# If there is any such submission,
						if previous_ac_submission_count > 0:
							# Submissions are sorted by increasing timestamp. 
							# So the oldest submission is scored
							oldest_ac_runid = int(data[0][0])
							print(
								'[ SCOREBOARD ] Run: ', run_id, ' Another RunID has an AC verdict for this problem: ',
								oldest_ac_runid
							)
							# Set that RunID score to problem_max_score
							cur.execute(
								"UPDATE submissions SET score = ? WHERE run_id = ? ", 
								(
									problem_max_score,
									oldest_ac_runid,
								)
							)
							conn.commit()
							# Set this RunID score to 0
							cur.execute(
								"UPDATE submissions SET score = ? WHERE run_id = ? ", 
								(
									0,
									run_id,
								)
							)
							conn.commit()

							print(
								'[ SCOREBOARD ] Run: ', oldest_ac_runid, ' Score set to ', problem_max_score
							)
							
							# Now find the new timestamp for the leaderboard : The score does not change
							# This timestamp includes every submission
							cur.execute(
								"SELECT max(timestamp) FROM submissions WHERE client_id = ? and verdict = 'AC' and score > 0",
								(
									client_id,
								)
							)
							data = cur.fetchall()
							max_problem_ac_timestamp  = data[0][0]

							print(
								'[ SCOREBOARD ] CLient: ', client_id, ' New Total Time: ', max_problem_ac_timestamp, ' UPDATE SCOREBOARD' 
							)

							# Update the time on leaderboard
							cur.execute(
								"UPDATE scoreboard SET total_time = ? WHERE client_id = ? ", 
								(
									max_problem_ac_timestamp,
									client_id,
								)
							)
							conn.commit()

						elif previous_ac_submission_count == 0:
							# If no submission can take its place, we make the score equal to 0
							# We also decrease the total score by problem_max_score
							# Also change total time for that client
							print('[ SCOREBOARD ] Client: ', client_id, ' No RunID has AC for this problem now')
							print('[ SCOREBOARD ] Client: ', client_id, ' This problem is unsolved by the client.')
							new_total_score = previous_total_score - problem_max_score
							# Also, problems_solved count is now decreased
							# problems_solved -= 1
							# Problems_solved is automatically correct ( Calculated earlier on the basis of AC count )

							print('[ SCOREBOARD ] Client: ', client_id, ' New Total Score: ', new_total_score)
							# Get previous total_time : Last AC time
							cur.execute(
								"SELECT timestamp FROM submissions WHERE client_id = ? and verdict = 'AC'  and score > 0 ORDER BY run_id DESC", 
								(
									client_id, 
								)
							)
							data = cur.fetchall()
							# Data can not be NONE (Guarenteed)
							if data == None or len(data) == 0: # Meh, Anyways 
								previous_timestamp = '00:00:00'
							else:
								previous_timestamp = data[0][0]

							print('[ SCOREBOARD ] Client: ', client_id, ' New Total Time: ', previous_timestamp)

							# Update this submission score to 0
							cur.execute(
								"UPDATE submissions SET score = ? WHERE run_id = ? ", 
								(
									0,
									run_id,
								)
							)
							conn.commit()

							# The problem_solved count automatically takes this into account
							cur.execute(
								"UPDATE scoreboard SET score = ?, problems_solved = ?, total_time = ? WHERE client_id = ? ", 
								(
									new_total_score,
									problems_solved,
									previous_timestamp,
									client_id,
								)
							)
							conn.commit()
							print(
								'[ SCOREBOARD ][ UPDATE ][ REJUDGE ] Client: ' 
								+ str(client_id) 
								+ " Prev Score :" 
								+ str(previous_total_score) 
								+ " New Score:" 
								+ str(new_total_score)
							)

					elif previous_score == 0:
						print('[ SCOREBOARD ] Client: ', client_id, ' This RunID is a new verdict, with no score.')
						# This is a wrong submission, and was not AC earlier, so set its score to 0 and be done
						cur.execute(
							"UPDATE submissions SET score = 0 WHERE run_id = ? ", 
							(
								run_id,
							)
						)
						conn.commit()

			except Exception as error:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print('[ DB ][ CRITICAL ][ SCOREBOARD ] Updation error: ' + str(error) + 'in File ', fname, ' Line No. ', exc_tb.tb_lineno)
			finally:
				return

class previous_data(manage_database):
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
			print('[ DB ][ INIT ] Client ID initialised to 0')
			client_id_counter = 0

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

	def validate_connected_client(user_name, client_id, client_ip, session_key = 'None'):
		#Validate client in database
		cur = manage_database.get_cursor()
		cur.execute(
			"SELECT exists(SELECT * FROM connected_clients WHERE user_name = ? and client_id = ? and ip = ?)",
			(
				user_name, 
				client_id, 
				client_ip, 
			)
		)
		validation_result = cur.fetchall()
		
		if validation_result[0][0] == 1:
			return True
		else:
			return False
		return

	def validate_connected_judge(user_name, judge_id, judge_ip):
		#Validate judge in database
		cur = manage_database.get_cursor()
		cur.execute(
			"SELECT exists(SELECT * FROM connected_judges WHERE user_name = ? and judge_id = ? and ip = ?)",
			(
				user_name, 
				judge_id, 
				judge_ip, 
			)
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

	def generate_judge_key():
		try:
			chars = string.ascii_uppercase + string.digits + string.ascii_lowercase	
			password = ''.join(random.choice(chars) for _ in range(6))
			return password
		except:
			return '__JUDGE__'

	def add_client(client_id, user_name, password, ip, state, table_name):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute(
				"INSERT INTO " + table_name + " values(?, ?, ?, ?, ?)", 
				(client_id, user_name, password, ip, state, )
			)
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Could not add client : " + str(error))
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
			if len(client_id) == 0:
				return -1
			else:
				return client_id[0][0]
		except Exception as error:
			print("[ DB ][ ERROR ] : The user does not have a client id yet.")
			return -1

	# Get user_name when client_id is known
	def get_client_username(client_id):
		try:
			cur = manage_database.get_cursor()
			client_id = int(client_id)
			cur.execute("SELECT user_name FROM connected_clients WHERE client_id = ?", (client_id, ))
			client_username = cur.fetchall()
			return client_username[0][0]
		except Exception as error:
			print("[ DB ][ ERROR ] : Could not fetch username.")
			return 'Null'

	# Check if a client with given client_id is connected in the system, and return its state
	def check_connected_client(user_name, table_name ):
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT * FROM " + table_name + " WHERE user_name = ?", (user_name,))
			result = cur.fetchall()
			# print('[ LOGIN ][ VALIDATION ] ' + str(user_name) + ' :: Status -> ' + str(result[0][3]))
			return result[0][4]
		except:
			# If user was not connected earlier, this exception will be raised
			return 'New'

	def check_client_ip(client_id, ip):
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT * FROM connected_clients WHERE client_id = ? and ip = ?", (client_id, ip, ))
			result = cur.fetchall()
			if len(result) == 0 or result == '':
				return 0
			return 1
		except:
			# If user was not connected earlier, this exception will be raised
			return 0

	def get_connected_clients():
		response = []
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT user_name FROM connected_clients")
			data = cur.fetchall()
			for entry in data:
				response.append(entry[0])
		except Exception as error:
			print("[ DB ][ ERROR ] : Could not fetch client list.")
		return response

	
class submissions_management(manage_database):
	def insert_submission(run_id, local_run_id, client_id, language, source_file_name, problem_code, verdict, timestamp):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		run_id = int(run_id)
		client_id = int(client_id)
		local_run_id = int(local_run_id)
		try:
			cur.execute("INSERT INTO submissions values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (run_id, local_run_id, client_id, language, source_file_name, problem_code, verdict, timestamp, 'WAITING', '-', 0, ))
			conn.commit()
			return 1
		except Exception as error:
			print("[ DB ][ ERROR ] Could not insert into submission : " + str(error))
			return 0
		

	def generate_new_run_id():
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT max(run_id) FROM submissions")
			data = cur.fetchall()
			if len(data) == 0 or data[0][0] == None:
				return 1
			else:
				return int(data[0][0]) + 1
		except Exception as error:
			return 1
 
	def get_held_submissions():
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT run_id, client_id, client_run_id, source_file, problem_code, verdict, judge, timestamp FROM submissions WHERE sent_status = 'REVIEW' ORDER BY run_id ASC")
			data = cur.fetchall()
			if len(data) == 0 or data == '':
				return []
			else:
				return data
		except Exception as error:
			return []

	def update_submission_status(run_id, verdict, sent_status, judge = '-'):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		run_id = int(run_id)
		try:
			cur.execute("UPDATE submissions SET verdict = ?, sent_status = ?, judge = ? WHERE run_id = ?", (verdict, sent_status, judge, run_id,))
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Could not update submission submission : " + str(error))
			conn.rollback()
		return

	def delete_all():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("DELETE FROM submissions")
			conn.commit()
			
		except Exception as error:
			print("[ DB ][ ERROR ] Database deletion error : " + str(error))

	def get_last_sub_time(client_id):
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT max(timestamp) FROM submissions WHERE client_id = ?" , (client_id,))
			data = cur.fetchall()
			if len(data) == 0 or data[0][0] == None:
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
			if len(data) == 0 or data[0][0] == None:
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
			if len(data) == 0 or data[0][0] == None:
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
			if len(data) == 0 or data[0][0] == None:
				return "NONE"
			else:
				return data[0][0]
		except Exception as error:
			return "NONE"

	def get_submission_data(code, client):
		items = 'client_id, run_id, language, problem_code, source_file, client_run_id, timestamp'
		if client == '*' and code == '*':
			try:
				cur = manage_database.get_cursor()
				query = "SELECT " + items + " FROM submissions ORDER BY timestamp ASC"
				cur.execute(query)
				data = cur.fetchall()
				if data == '' or len(data) == 0:
					return "NF"
				else:
					return data
			except Exception as error:
				print('[ DB ][ ERROR ] ' + str(error))
				return "NONE"

		elif client == '*':
			try:
				cur = manage_database.get_cursor()
				query = (
					"SELECT " + 
					items + 
					" FROM submissions " +
					" WHERE problem_code = '" +
					code +
					"' " +
					"ORDER BY timestamp ASC"
				)
				cur.execute(query)
				data = cur.fetchall()
				if data == '' or len(data) == 0:
					return "NF"
				else:
					return data
			except Exception as error:
				print('[ DB ][ ERROR ] ' + str(error))
				return "NONE"

		elif code == '*':
			try:
				cur = manage_database.get_cursor()
				query = (
					"SELECT " + 
					items + 
					" FROM submissions " +
					" WHERE client_id = '" +
					client + 
					"' " + 
					"ORDER BY timestamp ASC"
				)
				cur.execute(query)
				data = cur.fetchall()
				if data == '' or len(data) == 0:
					return "NONE"
				else:
					return data
			except Exception as error:
				print('[ DB ][ ERROR ] ' + str(error))
				return "NONE"
		else:
			try:
				cur = manage_database.get_cursor()
				query = (
					"SELECT " + 
					items + 
					" FROM submissions " +
					" WHERE client_id = '" +
					client + 
					"' and problem_code = '" + 
					code +
					"' ORDER BY timestamp ASC"
				)
				cur.execute(query)
				data = cur.fetchall()
				if data == '' or len(data) == 0:
					return "NONE"
				else:
					return data
			except Exception as error:
				print('[ DB ][ ERROR ] ' + str(error))
				return "NONE"

	def get_judge_data(judge_username):
		try:
			cur = manage_database.get_cursor()
			query = (
				"SELECT " + 
				"run_id" + 
				" FROM submissions " +
				"WHERE judge = ?"
			)
			cur.execute(query, (judge_username, ))
			data1 = cur.fetchall()

			query = (
				"SELECT MAX(" + 
				"timestamp)" + 
				" FROM submissions " +
				"WHERE judge = ?"
			)
			cur.execute(query, (judge_username, ))
			data2 = cur.fetchall()

			if (
				data1 == '' or 
				len(data1) == 0 or
				data2 == '' or
				len(data2) == 0
			):
				return 'NONE', 'NONE'
			else:
				return str(len(data1)), data2[0][0]

		except Exception as error:
			print('[ DB ][ ERROR ] ' + str(error))
			return 'NONE', 'NONE'


class query_management(manage_database):
	def insert_query(query_id, client_id, query):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		try:
			cur.execute("INSERT INTO queries values(?, ?, ?, ?)", (query_id, client_id, query, 'TO BE ANSWERED', ))
			cur.execute('commit')
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Could not insert into submission : " + str(error))
		return

	def generate_new_query_id():
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT max(query_id) FROM queries")
			data = cur.fetchall()
			if len(data) == 0 or data[0][0] == None:
				return 1
			else:
				return int(data[0][0]) + 1
		except Exception as error:
			return 1

	def update_query(query_id, query, response):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		query_id = int(query_id)
		if query_id != -1:
			try:
				cur.execute("UPDATE queries SET response = ? WHERE query_id = ?", (response, query_id,))
				conn.commit()
			except Exception as error:
				print("[ DB ][ ERROR ] Could not insert into submission : " + str(error))
		else:
			try:
				cur.execute("INSERT INTO queries values(?, ?, ?, ?)", (0, 0, query, response, ))
				conn.commit()
			except Exception as error:
				print("[ DB ][ ERROR ] Could not insert into submission : " + str(error))
		return

	def delete_all():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("DELETE FROM queries")
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Database deletion error : " + str(error))


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

		except Exception as error:
			print('[ CRITICAL ] Database insertion error: ' + str(error))
			cur.execute('rollback')
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
			cur.execute("DELETE FROM accounts WHERE user_name = ?",(user_name,))
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Database deletion error : " + str(error))

	def delete_all_accounts():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("DELETE FROM accounts")
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Database deletion error : " + str(error))

	def disconnect_all():
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("UPDATE connected_clients SET state = 'Disconnected'")
			conn.commit()
			cur.execute("UPDATE connected_judges SET state = 'Disconnected'")
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Database updation error : " + str(error))
			conn.rollback()
		finally:
			return

	def delete_all():
		try:
			cur = manage_database.get_cursor()
			cur.execute("DELETE FROM connected_clients")
			cur.execute("DELETE FROM connected_judges")
			cur.execute('commit')
		except Exception as error:
			print("[ DB ][ ERROR ] Database deletion error : " + str(error))
			conn.rollback()
		finally:
			return

	def update_user_state(username, state, ip):
		if state == 'Blocked':
			hidden = 'True'
		else:
			hidden = 'False'

		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute(
				"UPDATE connected_clients SET state = ?, ip = ? where user_name = ? ", 
				(state, ip, username, )
			)
			cur.execute(
				"UPDATE scoreboard SET is_hidden = ? where user_name = ? ", 
				(hidden, username, )
			)
			
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Database updation error : " + str(error))
		finally:
			return

	def update_judge_state(username, state, ip):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute(
				"UPDATE connected_judges SET state = ?, ip = ? where user_name = ? ", 
				(state, ip, username, )
			)
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Database updation error : " + str(error))
		finally:
			return

	def update_user_password(username, password):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("UPDATE accounts SET password = ? where user_name = ? ", (password, username, ))
			cur.execute("UPDATE connected_clients SET password = ? where user_name = ? ", (password, username, ))
			conn.commit()
		except Exception as error:
			print("[ DB ][ ERROR ] Database updation error : " + str(error))
			conn.rollback()
		finally:
			return

	def add_sheet_accounts(user_list, password_list, type_list):
		u_len = len(user_list)
		p_len = len(password_list)
		t_len = len(type_list)
		if u_len != p_len or u_len != t_len:
			print('[ CRITICAL ] Database insertion error: Incorrect datatype or amount')
			return

		cur = manage_database.get_cursor()
		# INSERTIONS INTO DATABASE [ CRITICAL SETION ]

		cur.execute("begin")
		try:
			for i in range(0, u_len):
				cur.execute("INSERT into accounts values (?, ?, ? )" , (user_list[i], password_list[i], type_list[i], ))
			cur.execute("commit")

		except Exception as error:
			print('[ CRITICAL ] Database insertion error: ' + str(error))
			cur.execute('rollback')
			return 0
			
		# INSERTION FINISHED
		return 1

	def get_sheet_accounts():
		cur = manage_database.get_cursor()
		u_list = []
		p_list = []
		t_list = []
		try:
			cur.execute("SELECT * FROM accounts ORDER BY user_name ASC")
			data = cur.fetchall()
			if data != '' and len(data) != 0:
				for entry in data:
					u_list.append(entry[0])
					p_list.append(entry[1])
					t_list.append(entry[2])

		except Exception as error:
			print('[ CRITICAL ] Database fetch error: ' + str(error))

		return u_list, p_list, t_list

class report_management(manage_database):
	def get_account_data():
		try:
			cur = manage_database.get_cursor()
			query = 'SELECT * FROM accounts ORDER BY user_name ASC'
			cur.execute(query)
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return 'NULL'
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching account reports : ', error)
			return 'NULL'

	def get_all_submission_data():
		try:
			cur = manage_database.get_cursor()
			query = 'SELECT run_id, client_id, problem_code, language, timestamp, verdict, judge FROM submissions ORDER BY run_id ASC'
			cur.execute(query)
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return 'NULL'
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching submission reports : ', error)
			return 'NULL'

	def get_grouped_problem_sub_data(problem):
		try:
			cur = manage_database.get_cursor()
			query = 'SELECT run_id, client_id, language, timestamp, verdict FROM submissions where problem_code = ? ORDER BY run_id ASC'
			cur.execute(query, (problem, ))
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return []
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching submission reports : ', error)
			return 'NULL'

	def get_all_client_data():
		try:
			cur = manage_database.get_cursor()
			query = 'SELECT client_id, user_name, ip FROM connected_clients ORDER BY client_id ASC'
			cur.execute(query)
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return []
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching submission reports : ', error)
			return 'NULL'

	def get_grouped_client_sub_data(client_id):
		try:
			cur = manage_database.get_cursor()
			query = 'SELECT run_id, problem_code, language, timestamp, verdict FROM submissions where client_id = ? ORDER BY run_id ASC'
			cur.execute(query, (client_id, ))
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return []
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching submission reports : ', error)
			return 'NULL'

	def get_all_judge_data():
		try:
			cur = manage_database.get_cursor()
			query = 'SELECT judge_id, user_name, ip FROM connected_judges'
			cur.execute(query)
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return []
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching submission reports : ', error)
			return []

	def get_grouped_judge_sub_data(judge):
		try:
			cur = manage_database.get_cursor()
			query = 'SELECT run_id, client_id, problem_code, language, timestamp, verdict FROM submissions where judge = ? ORDER BY run_id ASC'
			cur.execute(query, (judge, ))
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return []
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching submission reports : ', error)
			return 'NULL'

	def get_judgement_count(judge):
		try:
			cur = manage_database.get_cursor()
			query = 'SELECT count(run_id) FROM submissions where judge = ?'
			cur.execute(query, (judge, ))
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return 0
			return data[0][0]
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching submission reports : ', error)
			return 0

	def get_winner():
		try:
			cur = manage_database.get_cursor()
			query = "select max(scoreboard.score), connected_clients.user_name from scoreboard, connected_clients where connected_clients.client_id = scoreboard.client_id"
			cur.execute(query)
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return []
			return data[0]
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching scoreboard reports : ', error)
			return "NULL"

	def get_scoreboard_data():
		try:
			cur = manage_database.get_cursor()
			query = "SELECT user_name, score, problems_solved, total_time FROM scoreboard where is_hidden = 'False' ORDER BY score DESC"
			cur.execute(query)
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return []
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching scoreboard reports : ', error)
			return "NULL"

	def get_query_data():
		try:
			cur = manage_database.get_cursor()
			query = "SELECT client_id, query, response FROM queries"
			cur.execute(query)
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return []
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching query reports : ', error)
			return "NULL"

	def get_problem_data():
		try:
			cur = manage_database.get_cursor()
			query = "SELECT * FROM problems"
			cur.execute(query)
			data = cur.fetchall()
			if data == '' or len(data) == 0:
				return []
			return data
		except Exception as error:
			print('[ DB ][ REPORTS ][ ERROR ] Error while fetching problem reports : ', error)
			return "NULL"

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







