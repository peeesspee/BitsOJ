import pika
from connection import manage_connection
from login import authenticate_login
from listen_server import listening
from database_management import manage_database
from submission import submit_solution
from threading import *
import sqlite3


rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'



cursor = manage_database.initialize_table()
listening.initialize()
channel,connection = manage_connection.initialize_connection(rabbitmq_username,rabbitmq_password,host)
def main():
	while(listening.login_status == False):
		authenticate_login.login(channel,host)
		listening.listen_login(channel)





login_thread = Thread(target = main)
login_thread.start()
login_thread.join()



send_data_thread = Thread(target = submit_solution.read_solution, args = (cursor, channel, ))
listen_server_thread = Thread(target = listening.listen_submission_result)
send_data_thread.start()
listen_server_thread.start()
send_data_thread.join()
listen_server_thread.join()
manage_connection.terminate_connection(connection)