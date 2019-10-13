import pika
import multiprocessing
import os
import signal
import sys
import json

from time import sleep
from connection import manage_connection
from database_management import manage_database
from interface import init_gui
from login_interface import start_interface
from listen_server import start_listening
from manage_code import send_code


with open("config.json", "r") as read_config:
	config = json.load(read_config)

# Basic credentials for login to RabbitMQ Server
rabbitmq_username = config["rabbitmq_username"]
rabbitmq_password = config["rabbitmq_password"]
host = config["host"]


def main():
	#################################
	# Initialize the database and returns the cursor 
	print("[ SETUP ] INITIALISING DATABASE ............")
	cursor = manage_database.initialize_table()

	##################################
	# Create variables/lists that will be shared between processes
	data_changed_flags = multiprocessing.Array('i', 10)
	# index    value     meaning
	# 0        0/1       Contest Not Started/Contest has been started
	# 1        0/1       

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
		# listen_pid = manage_process(channel,connection,cursor,host,data_changed_flags)

		# After successful login 
		# Starting Main GUI
		init_gui(data_changed_flags)
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! " + str(error))

	print("[EXIT] Signal Passed")
	# os.kill(listen_pid, signal.SIGINT)
	

	sleep(1)
	print("  ################################################")
	print("  #----------ClIENT CLOSED SUCCESSFULLY----------#")
	print("  ################################################")


def manage_process(channel, connection, cursor, host, data_changed_flags):
	listen_from_server = multiprocessing.Process(target = start_listening.listen_server, args = (channel, connection, cursor, host, data_changed_flags))

	listen_from_server.start()

	listen_pid = listen_from_server.pid

	return listen_pid

main()