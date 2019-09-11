import threading
import pika
from client_connections import manage_clients
from database_management import manage_database
from interface import server_window, init_gui
from judge_connections import manage_judges
# Variables  
superuser_username = 'BitsOJ'
superuser_password = 'root'
host = 'localhost'



def main():
	print("----------------BitsOJ v1.0----------------")
	

	# Initialize database
	conn, cur = manage_database.initialize_database()
	manage_database.insert_user("team1", "abcd", cur, conn)
	manage_database.insert_user("dummy", "dummy", cur, conn)
	manage_database.insert_judge("judge1", "judge1", cur, conn)

	# Manage Threads
	manage_threads(superuser_username, superuser_password, host)

	# Initialize GUI handler
	try:
		print('hi')
		#init_gui()
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! " + str(error))

	

def manage_threads(superuser_username, superuser_password, host):
	client_handler_thread = threading.Thread(target = manage_clients.listen_clients, args = (superuser_username, superuser_password, host,))
	judge_handler_thread = threading.Thread(target = manage_judges.listen_judges, args = (superuser_username, superuser_password, host,))

	client_handler_thread.start()
	judge_handler_thread.start()


	try:
		client_handler_thread.join()
		judge_handler_thread.join()

	except:
		print("User Keyboard Interrupt")

main()