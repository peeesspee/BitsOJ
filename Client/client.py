import pika
from connection import manage_connection
from login import authenticate_login
from listen_server import listening
# from database_management import manage_database
# from submission import read_solution
from threading import *
import sqlite3


rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'



# cursor = manage_database.initialize_table()
listening.initialize()
channel,connection = manage_connection.initialize_connection(rabbitmq_username,rabbitmq_password,host)
while(listening.login_status == False):
	authenticate_login.login(channel,host)
	listening.listen_server(channel)
	

# submit_solution.read_solution(cursor,channel)
manage_connection.terminate_connection(connection)