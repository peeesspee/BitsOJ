import threading
import pika
from rabbitmq_connections import manage_connection
from client_connections import manage_clients
from database_management import manage_database
# Variables  
rabbitmq_username = 'BitsOJ'
rabbitmq_password = 'root'
host = 'localhost'


def main():
	print("----------------BitsOJ v1.0----------------")
	
	# This function handles the client login requests
	conn, cur = manage_database.initialize_database()
	manage_database.insert_user("team1", "abcd", cur, conn)
	manage_database.insert_user("dummy", "dummy", cur, conn)
	manage_database.insert_user("judge1", "judge1", cur, conn)
	channel, connection = manage_connection.initialize_connection(rabbitmq_username, rabbitmq_password, host)

	# This listen will always be active

	manage_threads(channel)


	manage_connection.terminate_connection(connection)

def gui_handler_placeholder():
	return

def judge_handler_placeholder():
	return

def manage_threads(channel):
	client_handler_thread = threading.Thread(target = manage_clients.listen_clients, args = (channel,))
	gui_handler_thread = threading.Thread()
	judge_handler_thread = threading.Thread()

	client_handler_thread.start()
	try:
		client_handler_thread.join()
	except:
		print("User Keyboard Interrupt")



main()