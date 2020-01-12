import sqlite3


class manage_database():
	conn = None
	cur = None

	def initialize_database():

		try:
			conn = sqlite3.connect('judge_database.db')
			c = conn.cursor()
			manage_database.conn = conn
			manage_database.cur = c

		except Exception as error:
			print(str(error))

		try:
			# c.execute("create table if not exists verdict(run_id varchar2(10), p_code varchar2(10), language varchar2(10), verdict varchar2(6)), ")
			c.execute("create table if not exists verdict(run_id integer , client_id varchar2(10), verdict varchar2(6), language varchar2(10) , message varchar2(10), p_code varchar2(10), time_stamp varchar2(10), source varchar2(10))")

		except Exception as error:
			print("[ Table CREATION error ]"+str(error))

	def get_source(run_id):
		try:
			manage_database.cur.execute("SELECT source FROM verdit WHERE run_id =? ",(int(run_id),))
			x = manage_database.cur.fetchall()
			x = x[0][0]
			return x
		except Exception as Error:
			print(str(Error))



	def reset_database():
		c = manage_database.cur
		try:
			c.execute("drop table if exists verdict")
		except Exception as error:
			print(str(error))

	def insert_record(run_id, client_id, verdict,language, message, p_code, time_stamp, source_code):
		with manage_database.conn:
			c = manage_database.cur
			try:
				c.execute("INSERT INTO VERDICT VALUES (?,?,?,?,?,?,?,?)",(int(run_id), client_id, verdict, language, message, p_code, time_stamp, source_code))
				manage_database.conn.commit()
				# c.execute("commit")   this and the upper statements are same
			except Exception as error:
				print("insertion error: "+str(error))

	def get_count(run_id):
		try:
			manage_database.cur.execute("SELECT COUNT(*) FROM verdict WHERE run_id = ?",(int(run_id)))
			a = manage_database.cur.fetchall()
			a = a[0][0]
		except Exception as error:
			print(str(error))
		return a

	def update_record(run_id, client_id, verdict,language, message, p_code, time_stamp, source_code):
		with manage_database.conn:
			c = manage_database.cur
			try:
				c.execute("UPDATE verdict SET client_id = ?,verdict = ?,language = ?,message = ?,p_code = ?,time_stamp = ?,source = ? WHERE run_id = ?",(client_id, verdict, language, message, p_code, time_stamp, source_code, int(run_id), ))
				manage_database.conn.commit()
				# c.execute("commit")   this and the upper statements are same
			except Exception as error:
				print("insertion error: "+str(error))

	def get_record():
		c = manage_database.cur
		c.execute("SELECT * FROM VERDICT")
		return c.fetchall()

	def close_db():
		conn = manage_database.conn
		conn.close()
	# conn.close()

	def get_cursor():
		return manage_database.cur

	def get_connection_object():
		return manage_database.conn



if __name__=='__main__':
	manage_database.initialize_database()
	manage_database.insert_record(5, '11', 'WA', 'C', 'Nul', 'ABCD', '02:09', './././')
	print(manage_database.get_record())