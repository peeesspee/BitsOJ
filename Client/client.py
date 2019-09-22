import pika
import multiprocessing
import os
import signal
import sys

from time import sleep
from connection import manage_connection
from database_management import manage_database
from interface import init_gui
from login_interface import start_interface
from listen_server import start_listening
from manage_code import send_code


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

	try:
		print("----------------BitsOJ v1.0----------------")
		# Starting GUI for login portal 
		start_interface(connection,data_changed_flags) 
		print("[ LOGIN ] Successful")

		# Manage Threads
		print('[ SETUP ] Initialising threads....')
		# listen_pid = manage_process(channel, connection, cursor, host, data_changed_flags)

		# After successful login 
		# Starting Main GUI
		init_gui(data_changed_flags)
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! " + str(error))


def manage_process(channel, connection, cursor, host, data_changed_flags):
	send_data = multiprocessing.Process(target =send_code.uploading_solution , args = (channel, connection, cursor, host, data_changed_flags))
	listen_from_server = multiprocessing.Process(target = start_listening.listen_server, args = (channel, connection, cursor, host, data_changed_flags))

	send_data.start()
	listen_from_server.start()

	# send_pid = send_data.pid
	listen_pid = listen_from_server.pid

	return listen_pid

main()