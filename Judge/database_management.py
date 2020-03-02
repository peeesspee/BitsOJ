import sqlite3

class manage_database():
	conn = None
	cur = None

	def initialize_database():
		try:
			print('[ CORE ][ DB ] Initializing database...')
			conn =  sqlite3.connect(
				'judge_database.db', 
				isolation_level = None,
				check_same_thread = False
			)
			cur = conn.cursor()
			manage_database.conn = conn
			manage_database.cur = cur

			cur.execute("create table if not exists verdict(run_id integer, client_id integer, verdict text, language varchar2(20), p_code varchar2(20), time_stamp varchar2(20), source_file text, judge text DEFAULT 'self')")

		except Exception as error:
			print('[ DB ][ ERROR ] ' + str(error))

		finally:
			return conn, cur

	def get_cursor():
		return manage_database.cur

	def get_source(run_id):
		try:
			manage_database.cur.execute("SELECT source FROM verdict WHERE run_id = ? ",(int(run_id),))
			x = manage_database.cur.fetchall()
			x = x[0][0]
			return x
		except Exception as Error:
			print('[ DB ][ ERROR ]' + str(Error))

	def reset_database():
		c = manage_database.cur
		try:
			c.execute("drop table if exists verdict")
		except Exception as error:
			print('[ DB ][ ERROR ]' + str(error))

	def get_cursor():
		return manage_database.cur

	def get_connection_object():
		return manage_database.conn

	def close_db():
		conn = manage_database.get_connection_object()
		conn.close()

class submission_management(manage_database):
	def insert_record(
			run_id, 
			client_id, 
			verdict, 
			language, 
			p_code, 
			time_stamp, 
			source_file_name
		):
		print('[ DB ] Inserting new record...')
		cur = manage_database.get_cursor()
		try:
			cur.execute("INSERT INTO verdict(run_id, client_id, verdict, language, p_code, time_stamp, source_file) values(?, ?, ?, ?, ?, ?, ?)",
				(
					int(run_id), 
					int(client_id), 
					verdict, 
					language, 
					p_code, 
					time_stamp, 
					source_file_name,
				)
			)
			print('[ DB ] Record inserted successfully...')
			return 0
		except  sqlite3.Error as ERROR:
			print('[ DB ] Insertion error: ',  ERROR)
			return 1
		except Exception as error:
			print("[ DB ][ ERROR ] Insertion error: " + str(error))
			return 1

	def get_count(run_id):
		run_id = int(run_id)
		cur = manage_database.get_cursor()
		try:
			cur.execute("SELECT COUNT(*) FROM verdict WHERE run_id = ?",
				(
					run_id,
				)
			)
			a = cur.fetchall()
			return int(a[0][0])
		except Exception as error:
			print('[ DB ] Exception: ', error)
			return 0

	def update_record(run_id, client_id, verdict, language, p_code, time_stamp, source_file_name):
		cur = manage_database.get_cursor()
		try:
			run_id = int(run_id)
			client_id = int(client_id)
			# Check if this run already exists in our table:
			cur.execute("SELECT * FROM verdict WHERE run_id = ?", (run_id, ))
			data = cur.fetchall()
			if data == None or len(data) == 0:
				# New insertion
				print('[ DB ] Inserting record...')
				# run_id , client_id , verdict , language , p_code , time_stamp , source_file , judge 
				cur.execute(
					"INSERT INTO verdict VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
					(
						run_id, 
						client_id, 
						verdict, 
						language, 
						p_code, 
						time_stamp, 
						source_file_name,
						'<NON LOCAL>' 
					)
				)
			cur.execute('commit')
		except Exception as error:
			print("[ DB ][ ERROR ] "+str(error))