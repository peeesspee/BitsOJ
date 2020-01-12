import pika
import multiprocessing
import threading
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
	try:
		conn, cursor = manage_database.initialize_table()
		manage_local_ids.initialize_local_id(cursor)
	except Exception as error:
		ex_type,ex_obj, ex_tb = sys.exc_info()
		f_name = os.path.split(ex_tb.tb_frame.f_code.co_filename)[1]
		print(ex_type,f_name,ex_tb.tb_lineno)

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
	# 8        1             Blocked User

	##################################
	# Makes connection with RabbitMQ
	# And returns channel,connection
	print("[ SETUP ] ESTABLISHING CONNECTION .........")
	try:
		channel,connection = manage_connection.initialize_connection(
			rabbitmq_username, 
			rabbitmq_password, 
			host
			)
		channel1 = connection.channel()
		channel2 = connection.channel()
	except:
		ex_type,ex_obj, ex_tb = sys.exc_info()
		f_name = os.path.split(ex_tb.tb_frame.f_code.co_filename)[1]
		print(ex_type,f_name,ex_tb.tb_lineno)



	try:
		print("----------------BitsOJ v1.0----------------")
		# Starting GUI for login portal 
		start_interface(data_changed_flags, queue) 
		print("[ LOGIN ] Successful")
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! " + str(error))


	try:
		# Manage Threads
		print('[ SETUP ] Initialising threads....')
		listen_thread = manage_process(
				rabbitmq_username,
				rabbitmq_password, 
				host ,
				data_changed_flags, 
				queue, 
				scoreboard,
				channel2
			)

		listen_thread.start()

	except Exception as error:
		print('[ CRITICAL ] Could not initialize threads : ' + str(error))
		# After successful login 
	try:
		# Starting Main GUI
		print('Main GUI Loading')
		init_gui(channel1,data_changed_flags, queue,scoreboard)
	except Exception as error:
		ex_type,ex_obj, ex_tb = sys.exc_info()
		f_name = os.path.split(ex_tb.tb_frame.f_code.co_filename)[1]
		print(ex_type,f_name,ex_tb.tb_lineno)

	# try:
	listen_thread.join()
	channel.close()
	channel1.close()
	channel2.close()

	manage_connection.terminate_connection()
	# except Exception as error:
	# 	ex_type,ex_obj, ex_tb = sys.exc_info()
	# 	f_name = os.path.split(ex_tb.tb_frame.f_code.co_filename)[1]
	# 	print('[ ERROR ] : ', ex_type,f_name,ex_tb.tb_lineno)

	sys.exit(0)



	print("[EXIT] Signal Passed")
	# os.kill(listen_pid, signal.SIGINT)

	

	sleep(1)
	print("  ################################################")
	print("  #----------ClIENT CLOSED SUCCESSFULLY----------#")
	print("  ################################################")


# Manageing process
def manage_process(
	rabbitmq_username, 
	rabbitmq_password, 
	host, 
	data_changed_flags, 
	queue, 
	scoreboard,
	channel2,
	):
	# this is from continuously listening from the server
	listen_from_server = threading.Thread(
		target = start_listening.listen_server, 
		args = (rabbitmq_username,rabbitmq_password, host, data_changed_flags, queue, scoreboard, channel2, )
		)

	return listen_from_server
	

	# listen_pid = listen_from_server.pid
	

	# returning process id 
	# return listen_pid



if __name__ == '__main__':
	main()