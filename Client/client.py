import pika
from connection import establish_connection
from login import authenticate_login
from threading import *
import sqlite3


rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'

channel,connection = establish_connection.main_function(rabbitmq_username,rabbitmq_password,host)

authenticate_login.main_function(channel,host)

connection.close()