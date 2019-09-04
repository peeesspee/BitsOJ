import pika
from connection import manage_connection
from login import authenticate_login
# from database_management import manage_database
# from submission import submit_solution
# from submission import read_solution, 
from threading import *
import sqlite3


rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'

# cursor = manage_database.initialize_table()
channel,connection = manage_connection.initialize_connection(rabbitmq_username,rabbitmq_password,host)

client_id,username = authenticate_login.login(channel,host)

# submit_solution.read_solution(client_id,username,channel)

manage_connection.terminate_connection(connection)