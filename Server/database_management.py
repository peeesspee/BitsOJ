import sqlite3
import sys

global client_id_counter
client_id_counter = 1


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
		
		
		# Comment out the following lines in production:
		cur.execute("drop table if exists accounts")
		cur.execute("drop table if exists submissions")
		cur.execute("drop table if exists scoreboard")
		cur.execute("drop table if exists connected_clients")
		cur.execute("drop table if exists judge_accounts")
		
		
		# Upto here
		try:	
			cur.execute("create table accounts(user_name varchar2(10) PRIMARY KEY, password varchar2(10))")
			cur.execute("create table judge_accounts(user_name varchar2(10) PRIMARY KEY, password varchar2(10))")
			cur.execute("create table connected_clients(client_id varchar2(3) PRIMARY KEY, user_name varchar2(10))")
			cur.execute("create table submissions(run_id varchar2(5) PRIMARY KEY, client_id varchar2(3), language varchar2(3), source_file varchar2(30),problem_code varchar(4), verdict varchar2(2), timestamp text)")
			cur.execute("create table scoreboard(client_id varchar2(3), problems_solved integer, total_time text)")
		except Exception as error:
			print("[ CRITICAL ERROR ] Table creation error : " + str(error))

		return conn, cur

	def insert_user(user_name, password, cur, conn):
		
		try:
			cur.execute("insert into accounts values (?,?)",(user_name, password,))
			conn.commit()
		except Exception as error:
			print("[ CRITICAL ERROR ] Database insertion error : " + str(error))

	def insert_judge(user_name, password, cur, conn):
		try:
			cur.execute("insert into judge_accounts values (?,?)",(user_name, password,))
			conn.commit()
		except Exception as error:
			print("[ CRITICAL ERROR ] Database insertion error : " + str(error))


	def get_cursor():
		return manage_database.cur

	def get_connection_object():
		return manage_database.conn


class client_authentication(manage_database):
	# This function validates (judge_username, judge_password) in database
	def validate_judge(user_name, password):
		cur = manage_database.get_cursor()
		cur.execute("select exists(select * from judge_accounts where user_name = ? and password = ?)", (user_name,password,))
		validation_result = cur.fetchall()
		
		if validation_result[0][0] == 1:
			return True
		else:
			return False
		

	#This function validates the (user_name, password, client_id) in the database.
	def validate_client(user_name, password):
		#Validate client in database
		cur = manage_database.get_cursor()
		cur.execute("select exists(select * from accounts where user_name = ? and password = ?)", (user_name,password,))
		validation_result = cur.fetchall()
		
		if validation_result[0][0] == 1:
			return True
		else:
			return False

	#This function generates a new client_id for new connections
	def generate_new_client_id():
		global client_id_counter
		client_id = str("{:03d}".format(client_id_counter))
		client_id_counter = client_id_counter + 1
		return client_id

	def add_connected_client(client_id, user_name):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		try:
			cur.execute("insert into connected_clients values(?, ?)", (client_id, user_name,))
		except:
			pass
		conn.commit()
		return	

	# Returns a list of tuple, containing client_id, user_name of connected clients.
	def show_connected_clients():
		cur = manage_database.get_cursor()
		try:
			cur.execute("select * from connected_clients")
			list_connected_clints = cur.fetchall()
			return list_connected_clints
		except Exception as error:
			print("[ ERROR ] Could not access client database : " + str(error))
			return Null
		
	# Get client_id when user_name is known
	def get_client_id(user_name):
		cur = manage_database.get_cursor()
		try:
			cur.execute("select client_id from connected_clients where user_name = ?", (user_name, ))
			client_id = cur.fetchall()
			return client_id[0][0]
		except Exception as error:
			print("[ ERROR ] : The user does not have a client id yet.")

	# Get user_name when client_id is known
	def get_client_username(client_id):
		cur = manage_database.get_cursor()
		try:
			cur.execute("select user_name from connected_clients where client_id = ?", (client_id, ))
			client_username = cur.fetchall()
			return client_username[0][0]
		except Exception as error:
			print("[ ERROR ] : Could not fetch username.")

	# Check if a client with given client_id is connected in the system
	def check_connected_client(user_name ):
		cur = manage_database.get_cursor()
		cur.execute("select exists(select * from connected_clients where user_name = ?)", (user_name,))
		existence_result = cur.fetchall()

		if existence_result[0][0] == 1:
			return True
		else:
			return False

	

class submissions_database_management(manage_database):
	def insert_submission(run_id, client_id, language, source_file_name, problem_code, verdict, timestamp):
		#cur.execute("create table submissions(run_id varchar2(5) PRIMARY KEY, client_id varchar2(3), language varchar2(3), source_file varchar2(30), verdict varchar2(2), timestamp text, problem_code varchar(4))")
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		try:
			cur.execute("insert into submissions values(?, ?, ?, ?, ?, ?, ?)", (run_id, client_id, language, source_file_name, verdict, timestamp, ))
			conn.commit()
		except:
			print("[ ERROR ] Could not insert into submission")
		return

	def view_submissions():
		cur = manage_database.get_cursor()
		try:
			cur.execute("select * from submissions")
			submission_data = cur.fetchall()
			return submission_data
		except:
			print("[ ERROR ] Could not view submissions")
			return Null

