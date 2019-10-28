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
			cur.execute("create table if not exists problems(Problem_No varchar2(9) PRIMARY KEY, Problem_Name varchar2(30), Problem_Code varchar2(10))")
			