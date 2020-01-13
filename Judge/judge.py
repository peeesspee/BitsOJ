from file_creation import file_manager
from connection import manage_connection
from login_request import authenticate_judge 
from communicate_server import communicate_server
from communicate_server_unicast import communicate_uni_server
from init_judge import initialize_judge
from gui import login_interface
import threading

def manage_threads(judge_username, channel2, channel3):
	listen_common_thread = threading.Thread(target = communicate_server.listen_server, args = (channel2, ))
	listen_uni_thread = threading.Thread(target = communicate_uni_server.listen_server, args = (judge_username, channel3, ))
	listen_uni_thread.start()
	listen_common_thread.start()
	listen_uni_thread.join()
	listen_common_thread.join()
	print('[ EXIT ]')

initialize_judge.read_config()

rabbitmq_username = initialize_judge.rabbitmq_username
rabbitmq_password = initialize_judge.rabbitmq_password
host = initialize_judge.host_ip
key = initialize_judge.key


connection = manage_connection.initialize_connection(rabbitmq_username,rabbitmq_password,host)
channel1 = connection.channel()
channel2 = connection.channel()
channel3 = connection.channel()

print("................ BitsOJ Judge .................\n")
try:
	login_interface(channel1,host)
except Exception as error:
	print('[ ERROR ] Could not initialize GUI.', error)

# status = ''
# while (status != 'VALID'):
# 	authenticate_judge.login(channel, host)
# 	status = authenticate_judge.login_status
# If VALID response is received
judge_username = 'judge00001'
manage_threads(judge_username, channel2, channel3)
manage_connection.terminate_connection(connection)

