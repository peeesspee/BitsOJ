import pika
from connection import manage_connection
from database_management import manage_database
import multiprocessing
from interface import init_gui
from login_interface import start_interface


# Basic credentials for login to RabbitMQ Server
rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'


def main():
	#################################
	# Initialize the database and returns the cursor 
	print("[ SETUP ] INITIALISING DATABASE ............")
	cursor = manage_database.initialize_table()

	##################################
	# Create variables/lists that will be shared between processes
	data_changed_flags = multiprocessing.Array('i', 10)

	##################################
	# Makes connection with RabbitMQ
	# And returns channel,connection
	print("[ SETUP ] ESTABLISHING CONNECTION .........")
	channel,connection = manage_connection.initialize_connection(
		rabbitmq_username, 
		rabbitmq_password, 
		host
		)

	# Starting GUI for login portal 
	start_interface(connection) 
	print("[ LOGIN ] Successful")
	# After successful login 
	# Starting Main GUI
	init_gui()


main()