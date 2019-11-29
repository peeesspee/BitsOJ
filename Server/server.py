import multiprocessing
import pika
import os
import signal
import sys
import time

from time import sleep
from client_connections import manage_clients
from database_management import manage_database
from Interface.interface import server_window, init_gui
from judge_connections import manage_judges
from bitsoj_core import core
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
#		'True',
#		'True' ,
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
	scoreboard_status = config["Scoreboard Update Allowed"]
	ranking_algorithm = config["Ranking Algorithm"]
	manual_review = config["Manual Review"]
	submission_time_limit = config["Submission Time Limit"]
	####################################################

	# Initialize database
	print('[ SETUP ] Initialising database...')
	conn, cur = manage_database.initialize_database()
	
	##################################
	# Create variables/lists that will be shared between processes
	data_changed_flags = multiprocessing.Array('i', 25)
	# This queue will be polled from bitsoj_core for handling tasks like 
	# database updates or data transmission
	task_queue = multiprocessing.Queue(maxsize = 1000)    

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
	#	15		0/1			1: Scoreboard update allowed
	# 	16		0/1			1: Update Scoreboard GUI
	#	17		0/1			1/2/3: ACM/IOI/Long Ranking Algorithm
	#	18		0/1			1: Broadcast Scoreboard to all clients
	#	19		0/1			1: UPDATE remaining time broadcast to all clients
	#	20		0/1			1: Manual Review Allowed
	#	21		X			X: Submission time limit 0 < X 
	

	#####################################################################################
	# Set local variables and flags :

	# Set submission time limit
	data_changed_flags[21] = submission_time_limit
 
	# Do not allow client logins unless Admin checks the allow_login checkbox in Clients tab
	if login_status == 'True' or login_status == 'true':
		data_changed_flags[2] = 1
	else:
		data_changed_flags[2] = 0

	# Check if judges can log in
	if judge_login == 'True' or judge_login == 'true':
		data_changed_flags[12] = 1
	else:
		data_changed_flags[12] = 0

	# Do not allow new submissions unless timer is active or admin begins contest
	if submission_status == 'True' or submission_status == 'true':
		data_changed_flags[3] = 1
	else:
		data_changed_flags[3] = 0

	# If scoreboard update is allowed, set this flag to 1
	if scoreboard_status == 'True' or scoreboard_status == 'true':
		data_changed_flags[15] = 1
	else:
		data_changed_flags[15] = 0

	# Set Ranking Algorithm
	if ranking_algorithm == 'ACM':
		data_changed_flags[17] = 1
	elif ranking_algorithm == 'IOI':
		data_changed_flags[17] = 2
	elif ranking_algorithm == 'LONG':
		data_changed_flags[17] = 3
	else:
		#DEFAULT TO ACM
		data_changed_flags[17] = 1

	if manual_review == 'True':
		data_changed_flags[20] = 1
	else:
		data_changed_flags[20] = 0

	data_changed_flags[4] = 0
	# SYSTEM SHUT flag
	data_changed_flags[7] = 0
	# Contest state flag(0/1/2 values assigned from interface, -1 signifies nothing)
	data_changed_flags[10] = -1
	#####################################################################################

	# Manage subprocesses
	print('[ SETUP ] Initialising subprocesses...')
	client_pid, judge_pid, core_pid = manage_process(
		judge_username, judge_password, host, 
		data_changed_flags, task_queue
		)

	# Initialize GUI handler
	try:
		init_gui(data_changed_flags, task_queue)
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! Restart Server." + str(error))
	#####################################################################################
	# Server process is in idle state here on. Active processes are:
	# client_manager
	# bitsoj_core
	# judge_manager
	#####################################################################################
	# If we reach here, it means the GUI process has ended, 
	# which further means the Server has been shut down by press of Close button.
	print("[ EXIT ] Signal passed")
	# Send SIGINT to both client and judge subprocesses
	# SIGINT : Keyboard Interrupt ( Handled by both subprocesses internally )
	# We're not exactly Killing the processes. They get the time to shut down on their own :)
	os.kill(client_pid, signal.SIGINT)		
	os.kill(judge_pid, signal.SIGINT)

	#####################################################################################
	# Write config file with changed data.
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

	if data_changed_flags[15] == 1:
		scoreboard_status = 'True'
	else:
		scoreboard_status = 'False'

	if data_changed_flags[20] == 1:
		manual_review = 'True'
	else:
		manual_review = 'False'

	submission_time_limit = data_changed_flags[21]

	save_status.update_entry('Judge Login Allowed', judge_login)
	save_status.update_entry('Login Allowed', login_status)
	save_status.update_entry('Submission Allowed', submission_status)
	save_status.update_entry('Scoreboard Update Allowed', scoreboard_status)
	save_status.update_entry('Manual Review', manual_review)
	save_status.update_entry('Submission Time Limit', submission_time_limit)
	#####################################################################################

	# EXIT
	sleep(2)
	print("  ################################################")
	print("  #----------SERVER CLOSED SUCCESSFULLY----------#")
	print("  ################################################")


def manage_process(
	judge_username, judge_password, host, 
	data_changed_flags, task_queue
	):
	client_handler_process = multiprocessing.Process(
		target = manage_clients.prepare, 
		args = (data_changed_flags, task_queue, )
		)
	judge_handler_process = multiprocessing.Process(
		target = manage_judges.listen_judges, 
		args = (judge_username, judge_password, host, data_changed_flags, task_queue,)
		)
	core_process = multiprocessing.Process(
		target = core.init_core,
		args = (data_changed_flags, task_queue, )
	)

	client_handler_process.start()
	judge_handler_process.start()
	core_process.start()

	# We return process ids of both client and server subprocesses to main()
	# to interrupt them when close button is pressed in GUI
	client_pid = client_handler_process.pid
	judge_pid = judge_handler_process.pid
	core_pid = core_process.pid
	return client_pid, judge_pid, core_pid

main()