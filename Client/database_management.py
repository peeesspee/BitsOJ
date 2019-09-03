import sqlite3
import os

class manage_database():
	def initialize_table():
		try:
			conn = sqlite3.connect('client_database.db')
			cur = conn.cursor()
			cur.execute("create table if not exists my_submissions(run_id varchar2(5),verdict varchar2(2),source_file varchar2(30),language varchar2(3), problem_code varchar2(8), time_stamp ")
			os.system('mkdir Solution')
			return cur
		except Error: 
			print(Error)

	def insert_verdict(client_id,cur,run_id,verdict,language,problem_code,time_stamp,code,extension):
		source_file = "Solution/" + client_id + '_' + run_id + '.' + extension
		file = open("Solution/" + client_id + '_' + run_id + '.' + extension, 'w')
		file = write(code)
		cur.execute("insert into my_submission values (?,?,?,?,?,?)",(run_id,verdict,source_file,language,problem_code,time_stamp))