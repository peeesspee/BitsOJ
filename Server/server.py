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
	manage_database.insert_user("Null","team1","abcd", cur, conn)
	
	channel, connection = manage_connection.initialize_connection(rabbitmq_username, rabbitmq_password, host)

	manage_clients.listen_clients(channel)



	manage_connection.terminate_connection(connection)
main()