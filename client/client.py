import pika
from connection import manage_connection
from database_management import manage_database
# from manage_data_sending import send_options
from multiprocessing import Process
from interface import init_gui



rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'


init_gui()

cursor = manage_database.initialize_table()
channel,connection = manage_connection.initialize_connection(
	rabbitmq_username, 
	rabbitmq_password, 
	host
	)

