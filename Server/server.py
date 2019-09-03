import threading
import pika
from rabbitmq_connections import manage_connections
from client_connections import manage_clients
# Variables  
rabbitmq_username = 'BitsOJ'
rabbitmq_password = 'root'
host = 'localhost'


def main():
	print("----------------BitsOJ v1.0----------------")
	
	# This function handles the client login requests
	channel, connection = manage_connections.main_function(rabbitmq_username, rabbitmq_password, host)
	manage_clients.main_function(channel)

	connection.close()

main()



