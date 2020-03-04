import multiprocessing
import pika
import os
import signal
import sys
import time
 
from time import sleep
from client_connections import manage_clients
from database_management import manage_database, problem_management, interface_sync
from Interface.interface import server_window, init_gui
from judge_connections import manage_judges
from bitsoj_core import core
from log_manager import handle_logs
from init_server import initialize_server, save_status


sys.path.append('../')

def main():
	config = initialize_server.read_config()
	rabbitmq_username = config["Server Username"]
	rabbitmq_password = config["Server Password"]
	host = config["Server IP"]
	login_status = config["Login Allowed"]
	judge_login = config["Judge Login Allowed"]
	submission_status = config["Submission Allowed"]
	scoreboard_status = config["Scoreboard Update Allowed"]
	ranking_algorithm = config["Ranking Algorithm"]
	manual_review = config["Manual Review"]
	submission_time_limit = config["Submission Time Limit"]

	####################################################################
	# Create variables/lists that will be shared between processes
	data_changed_flags = multiprocessing.Array('i', 30)
	# This queue will be polled from bitsoj_core for handling tasks like 
	# database updates or data transmission
	task_queue = multiprocessing.Queue(maxsize = 1000)   
	# This queue sends table update messages to the interface
	update_queue = multiprocessing.Queue(maxsize = 1000)  
	# This queue handles logs from all the 3 processes 
	log_queue = multiprocessing.Queue(maxsize = 100)
	# Lock object for database
	lock = multiprocessing.Lock()
	####################################################################

	log_process = multiprocessing.Process(
		target = handle_logs.init_logs,
		args = (data_changed_flags, log_queue, )
	)
	log_process.start()
	log_pid = log_process.pid

	log_queue.put('#### SERVER START ####')
	####################################################################
	# System check
	# This checks if the server shut down correctly during last system exit.
	flag = system_check()
	if flag == 0:
		# Unsafe
		print('[ SELF CHECK ][ FAIL ] Detected an abnormal system exit.')
		log_queue.put('[ SELF CHECK ][ FAIL ] Detected an abnormal system exit.')
		print('[ SELF CHECK ][ FAIL ] Please check that there are no active connections to RabbitMQ server', end = ' ' )
		print('in RabbitMQ Management portal ( http://localhost:15672/#/channels )')
		print('[ SELF CHECK ] Also close any running instances of the server from the task manager')
		print('[ SELF CHECK ] ( For Linux, use \'ps -a\' Command, and \'kill -9 pid\' where pid is the process id of server process.')
		print('[ SELF CHECK ] Press ENTER to continue')
		input()

	else:
		print('[ SELF CHECK ][ PASS ] Systems OK.')
		log_queue.put('[ SELF CHECK ][ PASS ] Systems OK.')
		
	####################################################################

	# Initialize server
	print('[ SETUP ] Initialising server...')
	log_queue.put('[ SETUP ] Initialising server...')

	# Initialize database
	print('[ SETUP ] Initialising database...')
	log_queue.put('[ SETUP ] Initialising database...')

	manage_database()
	manage_database.init_tables()
	if config["Contest Status"] == "SETUP":
		# Load Problems into problems table
		print('[ SETUP ] Loading problems...')
		problem_management.init_problems(config['Problems'])
		log_queue.put('[ SETUP ] Loading problems...')

	# Get table data for interface
	client_data = interface_sync.get_connected_clients_table()
	judge_data = interface_sync.get_connected_judges_table()
	account_data = interface_sync.get_account_table()
	submission_data = interface_sync.get_submission_table()
	scoreboard_data = interface_sync.get_scoreboard_table()
	query_data = interface_sync.get_queries_table()
	problem_data = interface_sync.get_problems_table()
	
	db_list = [
		account_data, 
		submission_data, 
		client_data, 
		judge_data, 
		query_data, 
		scoreboard_data, 
		problem_data
	]

	# Set local variables and flags :
	#####################################################################################
	#index		value		meaning
	#	0		0/1			New Submission : Show indication
	#	1		0/1			New Query : Show indication
	#	2		0/1 		0/1: Disallow/Allow logins
	#	3		0/1			0/1: Disallow/Allow submissions
	#	4		0/1			1: A create accounts window is open 
	#	5		0/1			
	#   6		0/1			1: Database data deletion under progress 
	#	7		0/1			1: Server shutdown
	#   8		0/1			1: Core EXIT 
	#	9		0/1			
	# 	10		0/1/2		0: SETUP 1: START 2: STOPPED	Contest Status
	#	11		0/1			1: Submission files open
	#	12		0/1			1: JUDGE logins allowed
	#   13		0/1			
	#	14		0/1			1: Do not allow multiple logins with same IP address
	#	15		0/1			1: Scoreboard update allowed
	# 	16		0/1			
	#	17		0/1			1/2/3: ACM/IOI/Long Ranking Algorithm
	#	18		0/1			1: Broadcast Scoreboard to all clients
	#	19		0/1			1: UPDATE remaining time broadcast to all clients
	#	20		0/1			1: Manual Review Allowed
	#	21		X			X: Submission time limit 0 < X 
	#	22		0/1			
	#	23		0/1			1: Stop logger
	#	24		0/1			1: Server locked
	#	25		0/1			1: Manual Reviews have just been turned off : Try to send all unjudged submissions?
	#	26		0/1			1: Connection error : Restart server
	#	27		0/1			1: Allow multiple IP 
	
	#####################################################################################
	
	# Set submission time limit
	data_changed_flags[14] = 0
	data_changed_flags[21] = submission_time_limit
	data_changed_flags[23] = 0
	data_changed_flags[26] = 0
	data_changed_flags[27] = 0
	# Do not allow client logins unless Admin checks the allow_login checkbox in Clients tab
	if login_status == True:
		data_changed_flags[2] = 1
	else:
		data_changed_flags[2] = 0

	# Check if judges can log in
	if judge_login == True:
		data_changed_flags[12] = 1
	else:
		data_changed_flags[12] = 0

	# Do not allow new submissions unless timer is active or admin begins contest
	if submission_status == True:
		data_changed_flags[3] = 1
	else:
		data_changed_flags[3] = 0

	# If scoreboard update is allowed, set this flag to 1
	if scoreboard_status == True:
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

	if manual_review == True:
		data_changed_flags[20] = 1
	else:
		data_changed_flags[20] = 0

	data_changed_flags[4] = 0
	# SYSTEM SHUT flag
	data_changed_flags[7] = 0
	# Server lock flag
	data_changed_flags[24] = 0
	data_changed_flags[25] = 0
	# Contest state flag(0/1/2 values assigned from interface, -1 signifies nothing)
	if config["Contest Status"] == "RUNNING":
		data_changed_flags[10] = 1
	elif config["Contest Status"] == "STOPPED":
		data_changed_flags[10] = 2
	elif config["Contest Status"] == "SETUP":
		data_changed_flags[10] = 0
		
 
	#####################################################################################

	# Manage subprocesses
	print('[ SETUP ] Initialising subprocesses...')
	log_queue.put('[ SETUP ] Initialising subprocesses...')
	client_pid, judge_pid, core_pid = manage_process(
		rabbitmq_username, 
		rabbitmq_password, 
		host, 
		data_changed_flags, 
		task_queue,
		log_queue,
		update_queue,
		lock
	)
	print('[ SETUP ] Subprocesses started')
	log_queue.put('[ SETUP ] Subprocesses started')
	print('[ SETUP ][ Process ] Client Manager: ', client_pid)
	log_queue.put('[ SETUP ][ Process ] Client Manager: ' + str(client_pid))
	print('[ SETUP ][ Process ] Judge Manager: ', judge_pid)
	log_queue.put('[ SETUP ][ Process ] Judge Manager: ' + str(judge_pid))
	print('[ SETUP ][ Process ] Core: ', core_pid)
	log_queue.put('[ SETUP ][ Process ] Core: ' + str(core_pid))
	print('[ SETUP ][ Process ] Log Manager: ', log_pid)
	log_queue.put('[ SETUP ][ Process ] Log Manager: ' + str(log_pid))
	
	# Initialize GUI handler

	try:
		######################################################################################
		init_gui(data_changed_flags, task_queue, log_queue, update_queue, db_list, lock)
		######################################################################################
	except Exception as error:
		print("[ MAIN ][ CRITICAL ] GUI could not be loaded! Restart Server." + str(error))
		log_queue.put("[ CRITICAL ] GUI could not be loaded! Restart Server." + str(error))
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print('[ MAIN ] Error data: ' , exc_type, fname, exc_tb.tb_lineno)
	#####################################################################################
	# Server process handles GUI here on. Other active processes are:
	# client_manager
	# Bitsoj_core
	# judge_manager
	# Log_manager
	#####################################################################################
	# If we reach here, it means the GUI process has ended, 
	# which further means the Server has been shut down by press of Close button.
	print("[ EXIT ] Signal passed")
	log_queue.put("[ EXIT ] Signal passed")

	# Send SIGINT to both client and judge subprocesses
	# SIGINT : Keyboard Interrupt ( Handled by both subprocesses internally )
	# We're not exactly Killing the processes. They get the time to shut down on their own :)
	os.kill(client_pid, signal.SIGINT)		
	os.kill(judge_pid, signal.SIGINT)

	#####################################################################################
	# Write config file with changed data.
	if data_changed_flags[2] == 1:
		login_status = True
	else:
		login_status = False

	if data_changed_flags[12] == 1:
		judge_login = True
	else:
		judge_login = False

	if data_changed_flags[3] == 1:
		submission_status = True
	else:
		submission_status = False

	if data_changed_flags[15] == 1:
		scoreboard_status = True
	else:
		scoreboard_status = False

	if data_changed_flags[20] == 1:
		manual_review = True
	else:
		manual_review = False

	submission_time_limit = data_changed_flags[21]

	print('[ EXIT ] Saving Server state to file.')
	log_queue.put('[ EXIT ] Saving Server state to file.')

	save_status.update_entry('Judge Login Allowed', judge_login)
	save_status.update_entry('Login Allowed', login_status)
	save_status.update_entry('Submission Allowed', submission_status)
	save_status.update_entry('Scoreboard Update Allowed', scoreboard_status)
	save_status.update_entry('Manual Review', manual_review)
	save_status.update_entry('Submission Time Limit', submission_time_limit)
	print('[ EXIT ] Saved Server state to file.')
	log_queue.put('[ EXIT ] Saved Server state to file.')
	#####################################################################################
	
	# EXIT
	sleep(1)
	log_queue.put("#### SERVER EXIT ####\n\n")
	# Stop logger service
	data_changed_flags[23] = 1
	system_stop()
	# Wait until LOGGER exits successfully
	while data_changed_flags[23] != 0:
		pass

	# Wait until CORE exits successfully
	while data_changed_flags[8] != 1:
		pass

	# Disconnect from Database
	manage_database.disconnect_database()
	
	print("  ################################################")
	print("  #----------SERVER CLOSED SUCCESSFULLY----------#")
	print("  ################################################")
	#####################################################################################

def manage_process(
		rabbitmq_username, 
		rabbitmq_password, 
		host, 
		data_changed_flags, 
		task_queue,
		log_queue,
		update_queue,
		lock
	):
	core_process = multiprocessing.Process(
		target = core.init_core,
		args = (data_changed_flags, task_queue, log_queue, update_queue, lock, )
	)
	client_handler_process = multiprocessing.Process(
		target = manage_clients.prepare, 
		args = (data_changed_flags, task_queue, log_queue, )
		)
	judge_handler_process = multiprocessing.Process(
		target = manage_judges.listen_judges, 
		args = (rabbitmq_username, rabbitmq_password, host, data_changed_flags, task_queue, log_queue, )
		)
	
	core_process.start()
	time.sleep(1)
	client_handler_process.start()
	judge_handler_process.start()
	

	# We return process ids of both client and server subprocesses to main()
	# to interrupt them when close button is pressed in GUI
	client_pid = client_handler_process.pid
	judge_pid = judge_handler_process.pid
	core_pid = core_process.pid
	
	return client_pid, judge_pid, core_pid

def system_check():
	flag = -1
	try:
		file = open('state_check.info', 'r')
		data = file.read()
		if data == 'SAFE':
			flag = 1
		elif data == 'UNSAFE':
			flag = 0
		file.close()

		if flag == 1:
			file = open('state_check.info', 'w')
			file.write('UNSAFE')
			file.close()
		return flag
	except Exception as error:
		return 0
	
def system_stop():
	try:
		file = open('state_check.info', 'w+')
		file.write('SAFE')
		file.close()
	except:
		pass


if __name__ == '__main__':
	# If this file is run natively, and not imported
	main()