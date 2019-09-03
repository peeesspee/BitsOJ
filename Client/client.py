import pika
from connection import establish_connection
from login import authenticate_login
from submission import submit_solution
# from submission import read_solution, 
from threading import *
import sqlite3


rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'

channel,connection = establish_connection.initialize_function(rabbitmq_username,rabbitmq_password,host)

client_id,username = authenticate_login.login(channel,host)

# submit_solution.read_solution(client_id,username,channel)

connection.close()