import multiprocessing
import pika
import os
import signal
import sys

from time import sleep
from client_connections import manage_clients
from database_management import manage_database
from Interface.interface import server_window, init_gui
from judge_connections import manage_judges
from init_server import initialize_server, save_status

sys.path.append('../')

def main():
	# Initialize server
	print('[ SETUP ] Initialising server...')

	#save_status.write_config('BitsOJ', 'root', 'judge1', 'judge1', 'localhost', 'True', 'True', 'abcdefghij12345', 'abcdefghij12345')

	initialize_server.read_config()
	superuser_username, superuser_password = initialize_server.get_superuser_details()
	judge_username, judge_password = initialize_server.get_judge_details()
	host = initialize_server.get_host()
	client_key, judge_key = initialize_server.get_keys()
	####################################################
	# TODO : Validate client and server keys when any message is sent, to maintain security 
	# (As project is open source)


	# Initialize database
	print('[ SETUP ] Initialising database...')
	conn, cur = manage_database.initialize_database()
	
	##################################
	# Create variables/lists that will be shared between processes
	data_changed_flags = multiprocessing.Array('i', 10)
	#index		value		meaning
	#	0		0/1			0/1: No new/ New submission data to refresh
	#	1		0/1			0/1: No new/ New login : Refresh login view
	#	2		0/1 		0/1: Disallow/Allow logins
	#	3		0/1			0/1: Disallow/Allow submissions
	#	4		0/1			1: A create accounts window is open
	#	5		0/1			1: New users generated, update view

	# Do not allow client logins unless Admin checks the allow_login checkbox in Clients tab
	login_status = initialize_server.get_login_flag()
	if login_status == True:
		data_changed_flags[2] = 1
	else:
		data_changed_flags[2] = 0

	# Do not allow new submissions unless timer is active or admin begins contest
	submission_status = initialize_server.get_submission_flag()
	if submission_status == True:
		data_changed_flags[3] = 1
	else:
		data_changed_flags[3] = 0
	data_changed_flags[4] = 0
	##################################

	# Manage Threads
	print('[ SETUP ] Initialising subprocesses...')
	client_pid, judge_pid = manage_process(superuser_username, superuser_password, judge_username, judge_password, host, data_changed_flags)

	# Initialize GUI handler
	print('[ SETUP ] Initialising GUI....')
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

	# Write config file
	if data_changed_flags[2] == 1:
		login_status = True
	else:
		login_status = False
	if data_changed_flags[3] == 1:
		submission_status = True
	else:
		submission_status = False
	save_status.write_config(superuser_username, superuser_password, judge_username, judge_password, host, login_status, submission_status, client_key, judge_key)

	# EXIT
	sleep(1)
	print("  ################################################")
	print("  #----------SERVER CLOSED SUCCESSFULLY----------#")
	print("  ################################################")


def manage_process(superuser_username, superuser_password, judge_username, judge_password, host, data_changed_flags):
	client_handler_process = multiprocessing.Process(target = manage_clients.prepare, args = (superuser_username, superuser_password, host, data_changed_flags,))
	judge_handler_process = multiprocessing.Process(target = manage_judges.listen_judges, args = (judge_username, judge_password, host, data_changed_flags,))

	client_handler_process.start()
	judge_handler_process.start()

	# We return process ids of both client and server subprocesses to main()
	# to interrupt them when close button is pressed in GUI
	client_pid = client_handler_process.pid
	judge_pid = judge_handler_process.pid
	return client_pid, judge_pid
	

main()