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
			c.execute("create table if not exists verdict(run_id varchar2(10), p_code varchar2(10), language varchar2(10), verdict varchar2(6))")

		except Exception as error:
			print(str(error))


	def reset_database():
		c = manage_database.cur

		try:
			c.execute("drop table if exists verdict")

		except Exception as error:
			print(str(error))

	def insert_record(run_id, p_code, language, verdict):
		with manage_database.conn:
			c = manage_database.cur
			c.execute("INSERT INTO VERDICT VALUES (?,?,?,?)",(run_id, p_code, language, verdict))

	def get_record():
		c = manage_database.cur
		c.execute("SELECT * FROM VERDICT")
		return c.fetchall()

	def close_db():
		conn = manage_database.conn
		conn.close()
	# conn.close()



