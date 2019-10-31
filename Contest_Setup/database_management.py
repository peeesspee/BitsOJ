import sqlite3
import os
import json


class manage_database():
	# cursor object
	cur = None
	# connection object
	conn = None

	def initialize_client_tables():
		try:
			conn = sqlite3.connect('client_setup.db', check_same_thread = False)
			manage_database.conn = conn
			cur = conn.cursor()
			manage_database.cur = cur
			# Execute database query to make tables 
			# Problem table to add problems in the contest
			cur.execute("create table if not exists problems(No varchar2(3) PRIMARY KEY,'Problem No' varchar2(9) , 'Problem Name' varchar2(30), 'Problem Code' varchar2(15))")
		except Exception as Error:
			print(str(Error))
		return cur



# Local Id's for all the submission to have a record for every submission locally 
class manage_local_ids(manage_database):
	global local_run_id
	local_run_id = 0
	# Initialize local run id
	def initialize_local_id():
		try:
			# Query to get the last max local id in my submission table
			manage_database.cur.execute("SELECT MAX(No) from problems")
			# storing the local run id in data
			data = int(manage_database.cur.fetchall()[0][0])
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



class problem_management(manage_database):

	def insert_problem(no,name,code):
		try:
			manage_database.cur.execute("INSERT INTO problems VALUES (?,?,?,?)",(no,'Problem '+no,name,code))
			manage_database.conn.commit()
		except Exception as Error:
			print(str(Error))

	def update_problem(no,name,code):
		try:
			manage_database.cur.execute("UPDATE problems SET 'Problem Name' = ?, 'Problem Code' = ? WHERE No = ?",(name,code,no,))
			manage_database.conn.commit()
		except Exception as Error:
			print(str(Error))


class reset_database(manage_database):

	def reset_problem(table_model):
		try:
			manage_database.cur.execute("drop table if exists problems")
			manage_database.cur.execute("create table if not exists problems(No varchar2(3) PRIMARY KEY,'Problem No' varchar2(9) , 'Problem Name' varchar2(30), 'Problem Code' varchar2(15))")
			manage_database.conn.commit()
			table_model.select()
		except Exception as Error:
			print(str(Error))