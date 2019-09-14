import multiprocessing
import pika
import os
import signal
from client_connections import manage_clients
from database_management import manage_database
from interface import server_window, init_gui
from judge_connections import manage_judges
# Variables  
superuser_username = 'BitsOJ'
superuser_password = 'root'
host = 'localhost'



def main():
	# Initialize database
	conn, cur = manage_database.initialize_database()
	#manage_database.reset_database(conn)
	#manage_database.insert_user("team1", "abcd", cur, conn)
	#manage_database.insert_user("dummy", "dummy", cur, conn)
	#manage_database.insert_judge("judge1", "judge1", cur, conn)

	# Manage Threads
	cpid, jpid = manage_process(superuser_username, superuser_password, host)

	# Initialize GUI handler
	try:
		print("----------------BitsOJ v1.0----------------")
		init_gui()

	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! " + str(error))

	print("[ EXIT ] Signal passed")
	#Send SIGINT to both client and judge processes
	os.kill(cpid, signal.SIGINT)
	os.kill(jpid, signal.SIGINT)



def manage_process(superuser_username, superuser_password, host):
	client_handler_process = multiprocessing.Process(target = manage_clients.listen_clients, args = (superuser_username, superuser_password, host,))
	judge_handler_process = multiprocessing.Process(target = manage_judges.listen_judges, args = ('judge1', 'judge1', host,))

	
	client_handler_process.start()
	judge_handler_process.start()

	cpid = client_handler_process.pid
	jpid = judge_handler_process.pid
	return cpid, jpid
	

main()