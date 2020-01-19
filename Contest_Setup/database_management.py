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
			cur.execute("create table if not exists problems(No integer PRIMARY KEY,'Problem No' varchar2(9) , 'Problem Name' varchar2(30), 'Problem Code' varchar2(15), 'Time Limit' integer)")
		except Exception as Error:
			print(str(Error))
		return cur


class testing(manage_database):
	def get_testing_details():
		manage_database.cur.execute("SELECT No, `Problem No`, `Problem Code`, `Time Limit` FROM problems")
		data = manage_database.cur.fetchall()
		return data


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
		manage_database.cur.execute("SELECT COUNT(*) FROM problems")
		x = manage_database.cur.fetchall()
		x = x[0][0]
		return (x+1)



class problem_management(manage_database):

	def insert_problem(no,name,code,time_limit):
		try:
			manage_database.cur.execute("INSERT INTO problems VALUES (?,?,?,?,?)",(int(no),'Problem '+no,name,code,time_limit))
			manage_database.conn.commit()
		except Exception as Error:
			print(str(Error))

	def update_problem(no,name,code,time_limit):
		try:
			manage_database.cur.execute("UPDATE problems SET 'Problem Name' = ?, 'Problem Code' = ?, 'Time Limit' = ? WHERE No = ?",(name,code,time_limit,int(no),))
			manage_database.conn.commit()
		except Exception as Error:
			print(str(Error))


class reset_database(manage_database):

	def reset_problem(table_model):
		try:
			manage_database.cur.execute("drop table if exists problems")
			manage_database.cur.execute("create table if not exists problems(No integer PRIMARY KEY,'Problem No' varchar2(9) , 'Problem Name' varchar2(30), 'Problem Code' varchar2(15), 'Time Limit' integer)")
			manage_database.conn.commit()
			table_model.select()
		except Exception as Error:
			print(str(Error))