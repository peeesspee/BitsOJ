import sqlite3
import os

class manage_database():
	cur = None
	conn = None
	def initialize_table():
		try:
			manage_database.conn = sqlite3.connect('client_database.db', check_same_thread = False)
			manage_database.cur = conn.cursor()
			cur.execute("create table if not exists my_submissions(run_id varchar2(5) PRIMARY KEY,verdict varchar2(2),source_file varchar2(30),language varchar2(3), problem_code varchar2(8), time_stamp text)")
			os.system('mkdir Solution')
			return cur
		except Error: 
			print(Error)

	def insert_verdict(client_id,run_id,verdict,language,problem_code,time_stamp,code,extension):
		source_file = "Solution/" + client_id + '_' + run_id + '.' + extension
		file = open("Solution/" + client_id + '_' + run_id + '.' + extension, 'w')
		file.write(code)
		manage_database.cur.execute("insert into my_submissions values (?,?,?,?,?,?)",(run_id,verdict,source_file,language,problem_code,time_stamp))
		manage_database.conn.commit()