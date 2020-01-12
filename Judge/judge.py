from file_creation import file_manager
from connection import manage_connection
from login_request import authenticate_judge 
from communicate_server import communicate_server
from init_judge import initialize_judge
from gui import login_interface
import threading


initialize_judge.read_config()

rabbitmq_username = initialize_judge.rabbitmq_username
rabbitmq_password = initialize_judge.rabbitmq_password
host = initialize_judge.host_ip
key = initialize_judge.key


channel, connection = manage_connection.initialize_connection(rabbitmq_username,rabbitmq_password,host)
print(type (channel))
print("................ BitsOJ Judge .................\n")
try:
	login_interface(channel,host)
except Exception as Error:
	print(str(Error))
# status = ''
# while (status != 'VALID'):
# 	authenticate_judge.login(channel, host)
# 	status = authenticate_judge.login_status
# If VALID response is received
try:
	communicate_server.listen_server()
except Exception as error:
	print('[ ERROR ] Could not listen to server.', error)

manage_connection.terminate_connection(connection)

def manage_threads():
