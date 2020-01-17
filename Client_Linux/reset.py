from database_management import manage_database
import os

rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'

conn, cur = manage_database.initialize_table()
manage_database.reset_database(conn)

for i in os.listdir('./Solution/'):
	os.remove('./Solution/'+i)