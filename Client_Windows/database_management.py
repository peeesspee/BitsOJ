import sqlite3
import os
global local_run_id 
import json

from init_client import handle_config


#############################################################
#############################################################

# Managing initialization and resetting of database 
class manage_database():
	# cursor object
	cur = None
	# connection object
	conn = None
	def initialize_table():
		try:
			conn = sqlite3.connect('client_database.db', check_same_thread = False)
			manage_database.conn = conn
			cur = conn.cursor()
			manage_database.cur = cur
			# Executing database query to make tables
			# My Submissions table for storing submission of the client
			cur.execute("create table if not exists my_submissions(local_run_id integer,run_id integer,verdict varchar2(20),source_file varchar2(30),language varchar2(10),language_code varchar2(5), problem_code varchar2(8),problem_number varchar2(10), time_stamp text)")
			# My Query table to store the queries asked by the individual client
			cur.execute("create table if not exists my_query(Query varchar2(500), Response varchar2(100))")
			cur.execute("create table if not exists score_table(team_name varchar2(20),score integer,problems_solved integer,time_taken text)")
		except Exception as Error: 
			print(Error)
		try:
			if os.path.isdir('./Solution'):
				pass
			else:
				os.system('mkdir -p Solution')
		except Exception as Error:
			print(str(Error))

		return conn, cur


	def insert_score(
		team_name,
		score,
		problems_solved,
		time_taken
		):
		try:
			manage_database.cur.execute("INSERT INTO score_table VALUES (?,?,?,?)",(team_name,int(score),int(problems_solved),time_taken))
			manage_database.conn.commit()
		except Exception as Error:
			print('[ SCORE INSERTION ERRRO ] ' + str(Error))


	def update_score(
		team_name,
		score,
		problems_solved,
		time_taken
		):
		try:
			manage_database.cur.execute("UPDATE score_table SET score = ?,problems_solved = ?,time_taken = ? WHERE team_name = ?",(int(score),int(problems_solved),time_taken,team_name,))
			manage_database.conn.commit()
		except Exception as Error:
			print('[ SCORE UPDATION ERROR ] ' + str(Error))

	def get_whether_exist_or_not(
		team
		):
		manage_database.cur.execute("SELECT COUNT(*) FROM score_table WHERE team_name = ?",(team,))
		x = manage_database.cur.fetchall()
		x = x[0][0]
		return x

	# reset database function to drop all the tables in the database
	def reset_database(conn):
		cur = conn.cursor()
		try:
			# Query to drom my submissions and my query table
			cur.execute("drop table if exists my_submissions")
			cur.execute("drop table if exists my_query")
			cur.execute("drop table if exists score_table")
		except Exception as Error:
			print(str(Error))

##############################################################
##############################################################

##############################################################
##############################################################

class source_code(manage_database):

	def get_source(run_id):
		try:
			manage_database.cur.execute("SELECT source_file FROM my_submissions WHERE run_id = ?",(run_id,))
			data = manage_database.cur.fetchall()
			data = data[0][0]	
			return data
		except Exception as error:
			ex_type,ex_obj, ex_tb = sys.exc_info()
			f_name = os.path.split(ex_tb.tb_frame.f_code.co_filename)[1]
			print(ex_type,f_name,ex_tb.tb_lineno)

# Local Id's for all the submission to have a record for every submission locally 
class manage_local_ids():
	global local_run_id
	local_run_id = 0
	# Initialize local run id
	def initialize_local_id(cur):
		try:
			# Query to get the last max local id in my submission table
			cur.execute("SELECT MAX(local_run_id) from my_submissions")
			# storing the local run id in data
			data = int(cur.fetchall()[0][0])
			if(data == ''):
				# if the table is empty then initialize it with 0
				manage_local_ids.local_run_id =  0
			else:
				# Else initialize it with that local id
				manage_local_ids.local_run_id =  data
		except:
			manage_local_ids.local_run_id =  0

	# Function to get the new local id
	def get_new_id():
		# Increment local run id by 1
		manage_local_ids.local_run_id += 1
		return manage_local_ids.local_run_id 

####################################################################
####################################################################


####################################################################
####################################################################


# Submission Managemnt class to update ad insert query in my submission table
class submission_management(manage_database):
	# Query to insert a new submission 
	def insert_verdict(
		local_run_id,
		client_id,
		run_id,
		verdict,
		language,
		language_code,
		problem_code,
		problem_number,
		time_stamp,
		code,
		extension
		):
		# Creating a source file for every submission 
		source_file = client_id + '_' + str(local_run_id) + extension
		file = open("Solution\\" + client_id + '_' + str(local_run_id) + extension, 'w+')
		file.write(code)
		try:
			# Query to insert the submission
			manage_database.cur.execute("INSERT INTO my_submissions VALUES (?,?,?,?,?,?,?,?,?)",(int(local_run_id),int(run_id),verdict,source_file,language,language_code,problem_code,problem_number,time_stamp))
			manage_database.conn.commit()
		except Exception as Error:
			print(str(Error))

	# Query to update the submission table whenever receive a verdict for any submission
	def update_verdict(local_run_id,client_id,run_id,verdict):
		try:
			# Query to update the table
			manage_database.cur.execute("UPDATE my_submissions SET verdict = ?, run_id = ? WHERE local_run_id = ?", (verdict, int(run_id), int(local_run_id),))
			manage_database.conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not update submission submission : " + str(error))
		return


	def update_run_id(local_run_id,run_id):
		try:
			# Query to update the table
			manage_database.cur.execute("UPDATE my_submissions SET run_id = ? WHERE local_run_id = ?", (int(run_id), int(local_run_id),))
			manage_database.conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not update submission submission : " + str(error))
		return

	def update_verdict_reject(local_run_id):
		try:
			# Query to update the table
			manage_database.cur.execute("UPDATE my_submissions SET verdict = ? WHERE local_run_id = ?", ('REJECTED', int(local_run_id),))
			manage_database.conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not update submission submission : " + str(error))
		return
####################################################################
####################################################################


####################################################################
####################################################################

# Query Management Class all the queries related to query asked 
class query_management(manage_database):
	
	# Insert a new query in the table whenever asked
	def insert_query(query,response):
		try:
			# Query to insert in the table
			manage_database.cur.execute("INSERT INTO my_query VALUES(?,?)",(query,response))
			manage_database.conn.commit()
		except Exception as Error:
			print(str(Error))

	# Update a new query function
	def update_query(client_id,query,response,Type):
		# with open('config.json', 'r') as read_file:
		# 	config = json.load(read_file)
		config = handle_config.read_config_json()
		# if type will be broadcast the query wil be updated in every client's table 
		if Type == 'Broadcast':
			# Query to check whether that query exist in the table or not
			manage_database.cur.execute("SELECT exists(SELECT * FROM my_query WHERE Query = ?)", (query,))
			existence_result = manage_database.cur.fetchall()
			# if exist then just update the table with the response
			if (existence_result[0][0]):
				# Update  Query to update the table
				manage_database.cur.execute("UPDATE my_query SET Response = ? WHERE Query = ?",(response,query,))
				manage_database.conn.commit()
			else:
				# Else insert it as a new query
				manage_database.cur.execute("INSERT into my_query values(?,?)",(query,response))
				manage_database.conn.commit()
		# Else it will be updated in only the client's table who have raised that query
		else:
			# if client id matches then update the table
			if (str(client_id) == config["client_id"]):
				try:
					# Query to update the table 
					manage_database.cur.execute("UPDATE my_query SET Response = ? WHERE Query = ?",(response,query,))
					manage_database.conn.commit()
				except Exception as Error:
					print("[ ERROR ] Could not update submission submission : " + str(error))
			else:
				pass
		return

####################################################################
####################################################################