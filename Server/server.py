import multiprocessing
import pika
import os
import signal

from time import sleep
from client_connections import manage_clients
from database_management import manage_database
from interface import server_window, init_gui
from judge_connections import manage_judges


# Variables  (to be read from server_init.ini later)
superuser_username = 'BitsOJ'
superuser_password = 'root'
judge_username = 'judge1'
judge_password = 'judge1'
host = 'localhost'


def main():
	# Initialize database
	conn, cur = manage_database.initialize_database()
	
	##################################
	# Create variables/lists that will be shared between processes
	data_changed_flags = multiprocessing.Array('i', 10)
	##################################

	# Manage Threads
	client_pid, judge_pid = manage_process(superuser_username, superuser_password, host, data_changed_flags)

	# Initialize GUI handler
	try:
		print("----------------BitsOJ v1.0----------------")
		init_gui(data_changed_flags)

	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! " + str(error))

	print("[ EXIT ] Signal passed")
	# Send SIGINT to both client and judge processes
	# SIGINT : Keyboard Interrupt is handled by both subprocesses internally
	os.kill(client_pid, signal.SIGINT)
	os.kill(judge_pid, signal.SIGINT)
	# EXIT
	sleep(1)
	print("  ################################################")
	print("  #----------SERVER CLOSED SUCCESSFULLY----------#")
	print("  ################################################")


def manage_process(superuser_username, superuser_password, host, data_changed_flags):
	client_handler_process = multiprocessing.Process(target = manage_clients.listen_clients, args = (superuser_username, superuser_password, host, data_changed_flags,))
	judge_handler_process = multiprocessing.Process(target = manage_judges.listen_judges, args = (judge_username, judge_password, host, data_changed_flags,))

	
	client_handler_process.start()
	judge_handler_process.start()

	# we return process ids of both client and server subprocesses to main()
	# to interrupt them when close button is pressed in GUI
	client_pid = client_handler_process.pid
	judge_pid = judge_handler_process.pid
	return client_pid, judge_pid
	

main()