import sqlite3
import os
global local_run_id 
import json


class manage_database():
	cur = None
	conn = None
	def initialize_table():
		try:
			conn = sqlite3.connect('client_database.db', check_same_thread = False)
			manage_database.conn = conn
			cur = conn.cursor()
			manage_database.cur = cur
			cur.execute("create table if not exists my_submissions(local_run_id varchar2(5),run_id varchar2(5),verdict varchar2(20),source_file varchar2(30),language varchar2(10),language_code varchar2(5), problem_code varchar2(8), time_stamp text)")
			cur.execute("create table if not exists my_query(Query varchar2(500), Response varchar2(100))")
		except Exception as Error: 
			print(Error)
		try:
			os.system('mkdir Solution')
		except:
			pass

		return conn, cur

	def reset_database(conn):
		cur = conn.cursor()
		try:
			cur.execute("drop table if exists my_submissions")
			cur.execute("drop table if exists my_query")
		except:
			print("[ CRITICAL ERROR ] Table drop error")


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
		source_file = client_id + '_' + str(local_run_id) + extension
		file = open("Solution/" + client_id + '_' + str(local_run_id) + extension, 'w+')
		file.write(code)
		manage_database.cur.execute("INSERT INTO my_submissions VALUES (?,?,?,?,?,?,?,?)",(local_run_id,run_id,verdict,source_file,language,language_code,problem_code,time_stamp))
		manage_database.conn.commit()


	def update_verdict(local_run_id,client_id,run_id,verdict):
		try:
			manage_database.cur.execute("UPDATE my_submissions SET verdict = ?, run_id = ? WHERE local_run_id = ?", (verdict, run_id, local_run_id,))
			manage_database.conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not update submission submission : " + str(error))
		return


class query_management(manage_database):
	
	def insert_query(query,response):
		manage_database.cur.execute("INSERT INTO my_query VALUES(?,?)",(query,response))
		manage_database.conn.commit()


	def update_query(client_id,query,response,Type):
		with open('config.json', 'r') as read_file:
			config = json.load(read_file)
		if Type == 'Broadcast':
			manage_database.cur.execute("SELECT exists(SELECT * FROM my_query WHERE Query = ?)", (query,))
			existence_result = manage_database.cur.fetchall()
			if (existence_result[0][0]):
				manage_database.cur.execute("UPDATE my_query SET Response = ? WHERE Query = ?",(response,query,))
				manage_database.conn.commit()
			else:
				manage_database.cur.execute("INSERT into my_query values(?,?)",(query,response))
				manage_database.conn.commit()
		else:
			print(client_id)
			print(type(client_id))
			print(config["client_id"])
			print(type(config["client_id"]))
			if (str(client_id) == config["client_id"]):
				try:
					print(query)
					manage_database.cur.execute("SELECT * FROM my_query WHERE Query = ?",(query,))
					existence_result = manage_database.cur.fetchall()
					print(existence_result)
					manage_database.cur.execute("UPDATE my_query SET Response = ? WHERE Query = ?",(response,query,))
					manage_database.conn.commit()
				except Exception as Error:
					print("[ ERROR ] Could not update submission submission : " + str(error))
			else:
				pass
		return