import sqlite3
import sys

class manage_database():
	
	def initialize_database():
		try:
			conn = sqlite3.connect('server_database.db')
			cur = conn.cursor()
		except Exception as error:
			print ("[ CRITICAL ERROR ]Database connection error : " + str(error))
		
		
		# Comment out the following lines in production:
		cur.execute("drop table if exists accounts")
		cur.execute("drop table if exists submissions")
		cur.execute("drop table if exists scoreboard")
		# Upto here
			
		try:	
			cur.execute("create table accounts(client_id varchar2(3) PRIMARY KEY, username varchar2(10), password varchar2(10))")
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

	def get_cursor():
		return cur


class client_authentication(manage_database):
	#This function validates the (username, password, client_id) in the database.
	def validate_client(username, password, client_id):
		#Validate client in database
		cur = manage_database.get_cursor()
		cur.execute("select exists(select 1 from accounts where username = ?)", (username))
		t = cur.fetchall()
		print (t);
		status = True
		return status

	#This function generates a new client_id for new connections
	def generate_new_client_id():
		return "123"


	