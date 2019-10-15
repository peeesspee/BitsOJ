import sqlite3
import os
global local_run_id 
class manage_database():
	cur = None
	conn = None
	def initialize_table():
		try:
			conn = sqlite3.connect('client_database.db', check_same_thread = False)
			manage_database.conn = conn
			cur = conn.cursor()
			manage_database.cur = cur
			cur.execute("create table if not exists my_submissions(local_run_id varchar2(5),run_id varchar2(5),verdict varchar2(10),source_file varchar2(30),language varchar2(10),language_code varchar2(5), problem_code varchar2(8), time_stamp text)")
		except Exception as Error: 
			print(Error)
		try:
			os.system('mkdir Solution')
		except:
			pass

		return cur


class manage_local_ids():
	global local_run_id
	local_run_id = 0
	def initialize_local_id(cur):
		try:
			cur.execute("SELECT MAX(local_run_id) from my_submissions")
			data = int(cur.fetchall()[0][0])
			if(data == ''):
				manage_local_ids.local_run_id =  0
			else:
				manage_local_ids.local_run_id =  data
		except:
			manage_local_ids.local_run_id =  0

	def get_new_id():
		manage_local_ids.local_run_id += 1
		return manage_local_ids.local_run_id 




class submission_management(manage_database):

	def insert_verdict(local_run_id,client_id,run_id,verdict,language,language_code,problem_code,time_stamp,code,extension):
		source_file = client_id + '_' + local_run_id + '.' + extension
		file = open("Solution/" + client_id + '_' + local_run_id + '.' + extension, 'w+')
		file.write(code)
		# print("yes")
		manage_database.cur.execute("insert into my_submissions values (?,?,?,?,?,?,?,?)",(local_run_id,run_id,verdict,source_file,language,language_code,problem_code,time_stamp))
		manage_database.conn.commit()


	def update_verdict(local_run_id,client_id,run_id,verdict):
		try:
			manage_database.cur.execute("UPDATE my_submissions SET verdict = ?, run_id = ? WHERE local_run_id = ?", (verdict, run_id, local_run_id,))
			manage_database.conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not update submission submission : " + str(error))
		return