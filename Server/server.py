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

# save_status.write_config(
# 		'BitsOJ', 
# 		'root', 
# 		'judge1', 
# 		'judge1', 
# 		'localhost', 
# 		'True', 
# 		'True', 
# 		'abcdefghij12345', 
# 		'abcdefghij12345', 
# 		'papa', 
# 		'02:00',
# 		'SETUP',
# 		'00:00:00',
# 		'00:00:00',
#		'0'
# 		)


	config = initialize_server.read_config()
	judge_username = config["Judge Username"]
	judge_password = config["Judge Password"]
	host = config["Server IP"]
	login_status = config["Login Allowed"]
	judge_login = config["Judge Login Allowed"]
	submission_status = config["Submission Allowed"]
	
	####################################################
	# TODO : Validate client and server keys when any message is sent, to maintain security 
	# (As project is open source)


	# Initialize database
	print('[ SETUP ] Initialising database...')
	conn, cur = manage_database.initialize_database()
	
	##################################
	# Create variables/lists that will be shared between processes
	data_changed_flags = multiprocessing.Array('i', 20)
	data_from_interface = multiprocessing.Queue(maxsize = 100)    # This queue will be polled for info from interface

	#index		value		meaning
	#	0		0/1			0/1: No new/ New submission data to refresh
	#	1		0/1			0/1: No new/ New login : Refresh connected clients view
	#	2		0/1 		0/1: Disallow/Allow logins
	#	3		0/1			0/1: Disallow/Allow submissions
	#	4		0/1			1: A create accounts window is open
	#	5		0/1			1: New users generated, update view
	#   6		0/1			1: Account deletion under progress
	#	7		0/1			1: Server shutdown
	#   8		0/1			1: Query reply GUI open
	#	9		0/1			1: Refresh query gui
	# 	10		0/1/2		0: SETUP 1: START 2: STOPPED
	#	11		0/1			1: Delete all accounts open
	#	12		0/1			1: JUDGE logins allowed
	#   13		0/1			1: Refresh Judge GUI
	#	14		0/1			1: Client Edit under progress

	# Do not allow client logins unless Admin checks the allow_login checkbox in Clients tab
	if login_status == 'True' or login_status == 'true':
		data_changed_flags[2] = 1
	else:
		data_changed_flags[2] = 0

	if judge_login == 'True' or judge_login == 'true':
		data_changed_flags[12] = 1
	else:
		data_changed_flags[12] = 0

	# Do not allow new submissions unless timer is active or admin begins contest
	
	if submission_status == 'True' or submission_status == 'true':
		data_changed_flags[3] = 1
	else:
		data_changed_flags[3] = 0

	data_changed_flags[4] = 0
	# SYSTEM SHUT flag
	data_changed_flags[7] = 0
	data_changed_flags[10] = -1
	##################################

	# Manage Threads
	print('[ SETUP ] Initialising subprocesses...')
	client_pid, judge_pid = manage_process(judge_username, judge_password, host, data_changed_flags, data_from_interface)

	# Initialize GUI handler
	print('[ SETUP ] Initialising GUI....')
	try:
		print("----------------BitsOJ v1.0----------------")
		init_gui(data_changed_flags, data_from_interface)

	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! " + str(error))

	print("[ EXIT ] Signal passed")
	# Send SIGINT to both client and judge processes
	# SIGINT : Keyboard Interrupt is handled by both subprocesses internally
	os.kill(client_pid, signal.SIGINT)
	os.kill(judge_pid, signal.SIGINT)

	# Write config file
	
	if data_changed_flags[2] == 1:
		login_status = 'True'
	else:
		login_status = 'False'

	if data_changed_flags[12] == 1:
		judge_login = 'True'
	else:
		judge_login = 'False'

	if data_changed_flags[3] == 1:
		submission_status = 'True'
	else:
		submission_status = 'False'

	save_status.update_entry('Judge Login Allowed', judge_login)
	save_status.update_entry('Login Allowed', login_status)
	save_status.update_entry('Submission Allowed', submission_status)
	
	# EXIT
	sleep(2)
	print("  ################################################")
	print("  #----------SERVER CLOSED SUCCESSFULLY----------#")
	print("  ################################################")


def manage_process(judge_username, judge_password, host, data_changed_flags, data_from_interface):
	client_handler_process = multiprocessing.Process(target = manage_clients.prepare, args = (data_changed_flags, data_from_interface, ))
	judge_handler_process = multiprocessing.Process(target = manage_judges.listen_judges, args = (judge_username, judge_password, host, data_changed_flags, ))

	client_handler_process.start()
	judge_handler_process.start()

	# We return process ids of both client and server subprocesses to main()
	# to interrupt them when close button is pressed in GUI
	client_pid = client_handler_process.pid
	judge_pid = judge_handler_process.pid
	return client_pid, judge_pid
	

main()