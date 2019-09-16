import pika
from connection import manage_connection
from database_management import manage_database
from multiprocessing import Process
from interface import init_gui
from login_interface import start_interface



rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'

def main():
	cursor = manage_database.initialize_table()
	channel,connection = manage_connection.initialize_connection(
		rabbitmq_username, 
		rabbitmq_password, 
		host
		)

	start_interface(connection) 
	print("[ LOGIN ] Successful")
	init_gui()

main()