import sqlite3
import os

class manage_database():
	cur = None
	conn = None
	def initialize_table():
		try:
			conn = sqlite3.connect('client_database.db', check_same_thread = False)
			manage_database.conn = conn
			cur = conn.cursor()
			manage_database.cur = cur
			cur.execute("create table if not exists my_submissions(run_id varchar2(5),verdict varchar2(10),source_file varchar2(30),language varchar2(10),language_code varchar2(5), problem_code varchar2(8), time_stamp text)")
		except Exception as Error: 
			print(Error)
		try:
			os.system('mkdir Solution')
		except:
			pass

		return cur




class submission_management(manage_database):

	def insert_verdict(client_id,run_id,verdict,language,language_code,problem_code,time_stamp,code,extension):
		source_file = "Solution/" + client_id + '_' + run_id + '.' + extension
		file = open("Solution/" + client_id + '_' + run_id + '.' + extension, 'w+')
		file.write(code)
		manage_database.cur.execute("insert into my_submissions values (?,?,?,?,?,?,?)",(run_id,verdict,source_file,language,language_code,problem_code,time_stamp))
		manage_database.conn.commit()


	def update_verdict(client_id,run_id,verdict):
		try:
			cur.execute("UPDATE my_submissions SET verdict = ? WHERE run_id = ?", (verdict, run_id,))
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not update submission submission : " + str(error))
		return