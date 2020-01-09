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
			c.execute("create table if not exists verdict(run_id varchar2(10) , client_id varchar2(10), verdict varchar2(6), message varchar2(10), p_code varchar2(10), timestamp varchar2(10), source varchar2(10))")

		except Exception as error:
			print("[Table CREATION error]"+str(error))


	def reset_database():
		c = manage_database.cur
		try:
			c.execute("drop table if exists verdict")
		except Exception as error:
			print(str(error))

	def insert_record(run_id, client_id, verdict, message, p_code, timestamp, source_code):
		with manage_database.conn:
			c = manage_database.cur
			try:
				c.execute("INSERT INTO VERDICT VALUES (?,?,?,?,?,?,?)",(run_id, client_id, verdict, message, p_code, timestamp, source_code))
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
	manage_database.insert_record('111', '111', 'AC', 'Nul', 'ABCD', '02:09', './././')
	print(manage_database.get_record())