import sqlite3
import sys

global counter
counter = 0


class manage_database():
	cur = None
	def initialize_database():
		try:
			conn = sqlite3.connect('server_database.db')
			cur = conn.cursor()
			manage_database.cur = cur
		except Exception as error:
			print ("[ CRITICAL ERROR ]Database connection error : " + str(error))
		
		
		# Comment out the following lines in production:
		cur.execute("drop table if exists accounts")
		cur.execute("drop table if exists submissions")
		cur.execute("drop table if exists scoreboard")
		cur.execute("drop table if exists active_clients")
		
		# Upto here
			
		try:	
			cur.execute("create table accounts(client_id varchar2(3), username varchar2(10) PRIMARY KEY, password varchar2(10))")
			cur.execute("create table active_clients(client_id varchar2(3) PRIMARY KEY, username varchar2(10))")
			cur.execute("create table submissions(client_id varchar2(3), run_id varchar2(5), language varchar2(3), source_file varchar2(30), verdict varchar2(2), timestamp text, problem_code varchar(8))")
			cur.execute("create table scoreboard(client_id varchar2(3), problems_solved integer, total_time text)")
		except Exception as error:
			print("[ CRITICAL ERROR ] Table creation error : " + str(error))

		return conn, cur

	def insert_user(client_id, user_name, password, cur, conn):
		
		try:
			cur.execute("insert into accounts values (?,?,?)",(client_id, user_name, password))
			conn.commit()
		except Exception as error:
			print("[ CRITICAL ERROR ] Database insertion error : " + str(error))

	def show_active_clients(cur):
		return

	def add_active_client(cur):
		return

	def remove_active_client(cur):
		return

	def check_active_client(cur):
		return


	def get_cursor():
		return manage_database.cur


class client_authentication(manage_database):
	#This function validates the (username, password, client_id) in the database.
	def validate_client(username, password):
		#Validate client in database
		cur = manage_database.get_cursor()
		cur.execute("select exists(select * from accounts where username = ? and password = ?)", (username,password,))
		validation_result = cur.fetchall()
		
		if(validation_result[0][0] == 1):
			status = True
		else:
			status = False
		return status

	#This function generates a new client_id for new connections
	def generate_new_client_id():
		global counter
		client_id = str("{:03d}".format(counter))
		print (counter)
		counter = counter + 1
		return client_id


	