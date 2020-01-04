import pika
import multiprocessing
import os
import signal
import sys
import json
import socket

from time import sleep
from connection import manage_connection
from database_management import manage_database, manage_local_ids
from interface_package.interface import init_gui
from interface_package.login_interface import start_interface
from listen_server import start_listening
from init_client import handle_config,rabbitmq_detail


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)


try:
	config = handle_config.read_config_json()
	config["IP"] = ip
	handle_config.write_config_json(config)
	config = handle_config.read_config_json()
except Exception as Error:
	print(str(Error))
	sys.exit()

	
try:
	# Basic credentials for login to RabbitMQ Server
	rabbitmq_username = config["rabbitmq_username"]
	rabbitmq_password = config["rabbitmq_password"]
	host = config["host"]
except Exception as Error:
	print(str(Error))
	sys.exit()

rabbitmq_detail.fill_detail(rabbitmq_username,rabbitmq_password,host)


def main():
	#################################
	# Initialize the database and returns the cursor 
	print("[ SETUP ] INITIALISING DATABASE ............")
	conn, cursor = manage_database.initialize_table()
	manage_local_ids.initialize_local_id(cursor)

	##################################
	# Create variables/lists that will be shared between processes
	data_changed_flags = multiprocessing.Array('i', 10)
	queue = multiprocessing.Queue()
	scoreboard = multiprocessing.Queue()
	for i in range(10):
		data_changed_flags[i] = 0
	# index    value         meaning
	# 0        0/1/2/3/4     Contest Not Started/Contest has been started/Running/Contest Stopped/Time Up
	# 1        0/1/2         Initialize/Verdict Not received/Verdict Received
	# 2        0/1/2         Initiaize/Query response Not received/Query response received
	# 3        1             Server NOt Accepting Submission
	# 4        0/1/3         Timer Stopped/ Timer running/Update Timer   
	# 5        0/1/2         Proper Connection/Single Client Disconnected/All Clients Disconnected
	# 6        1             Leader Board Update
	# 7        1             Problem Edited

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
		start_interface(connection,data_changed_flags, queue) 
		print("[ LOGIN ] Successful")


		# Manage Threads
		print('[ SETUP ] Initialising threads....')
		listen_pid = manage_process(rabbitmq_username,rabbitmq_password,cursor,host,data_changed_flags, queue,scoreboard)

		# After successful login 
		# Starting Main GUI
		init_gui(channel,data_changed_flags, queue,scoreboard)
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! " + str(error))

	print("[EXIT] Signal Passed")
	os.kill(listen_pid, signal.SIGINT)

	

	sleep(1)
	print("  ################################################")
	print("  #----------ClIENT CLOSED SUCCESSFULLY----------#")
	print("  ################################################")


# Manageing process
def manage_process(rabbitmq_username, rabbitmq_password, cursor, host, data_changed_flags,queue,scoreboard):
	# this is from continuously listening from the server
	listen_from_server = multiprocessing.Process(target = start_listening.listen_server, args = (rabbitmq_username,rabbitmq_password, cursor, host, data_changed_flags, queue,scoreboard))

	listen_from_server.start()

	listen_pid = listen_from_server.pid

	# returning process id 
	return listen_pid

main()