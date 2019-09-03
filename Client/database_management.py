import sqlite3

class manage_database():
	def __init(self):
		try:
			conn = sqlite3.connect('client_database.db')
			cur = conn.cursor()
		except Error: 
			print(Error)


	def create_table():
		cur.execute("create table if not exists my_submissions(run_id varchar2(5),verdict varchar2(2),source_file varchar2(30),language varchar2(3), problem_code varchar2(8), time_stamp ")