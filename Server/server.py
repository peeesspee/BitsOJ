import threading
import pika
from rabbitmq_connections import manage_connection
from client_connections import manage_clients
from database_management import manage_database
from interface import server_window, init_gui
# Variables  
rabbitmq_username = 'BitsOJ'
rabbitmq_password = 'root'
host = 'localhost'



def main():
	print("----------------BitsOJ v1.0----------------")
	
	# This function initializes RMQ connections
	try:
		channel, connection = manage_connection.initialize_connection(rabbitmq_username, rabbitmq_password, host)
	except Exception as error:
		print("[ CRITICAL ] Could not connect to RabbitMQ server : " + str(error))

	# Initialize GUI handler
	try:
		init_gui()
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! " + str(error))

	# Initialize database
	conn, cur = manage_database.initialize_database()
	manage_database.insert_user("team1", "abcd", cur, conn)
	manage_database.insert_user("dummy", "dummy", cur, conn)
	manage_database.insert_user("judge1", "judge1", cur, conn)
	

	# Manage Threads
	manage_threads(channel)


	manage_connection.terminate_connection(connection)

def manage_threads(channel):
	client_handler_thread = threading.Thread(target = manage_clients.listen_clients, args = (channel, ))
	judge_handler_thread = threading.Thread(target = judge_handler_placeholder)

	client_handler_thread.start()
	judge_handler_thread.start()

	try:
		client_handler_thread.join()
		judge_handler_thread.join()

	except:
		print("User Keyboard Interrupt")


def judge_handler_placeholder():
	return

main()