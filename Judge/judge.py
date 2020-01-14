from file_creation import file_manager
from connection import manage_connection
from login_request import authenticate_judge 
from communicate_server import communicate_server
from communicate_server_broadcast import communicate_broadcast_server
from init_judge import initialize_judge
from gui import login_interface
from interface import main_interface
import multiprocessing, os, signal, time, sys

def main():
	data_changed_flags = multiprocessing.Array('i', 10)
	data_changed_flags[1] = 0 # For unicast process flag
	data_changed_flags[2] = 0 # For broadcast process flag
	data_changed_flags[3] = 0 # For login close flag
	data_changed_flags[4] = 0 # For table update

	# Read config file
	initialize_judge.read_config()

	rabbitmq_username = initialize_judge.rabbitmq_username
	rabbitmq_password = initialize_judge.rabbitmq_password
	host = initialize_judge.host_ip
	key = initialize_judge.key

	connection = manage_connection.initialize_connection(rabbitmq_username, rabbitmq_password, host, data_changed_flags)
	channel1 = connection.channel()
	
	

	print("................ BitsOJ Judge .................\n")
	try:
		login_interface(channel1, host, data_changed_flags)
	except Exception as error:
		print('[ ERROR ] Could not initialize GUI.', error)

	channel1.close()
	connection.close()
	if data_changed_flags[3] == 1:
		# Login cancelled
		sys.exit()

	judge_username, judge_password, judge_id = initialize_judge.get_credentials()


	try:
		pid1, pid2 = manage_processes( judge_username, judge_id, data_changed_flags, rabbitmq_username, rabbitmq_password, host)
	except:
		print('[ ERROR ] Could not Init Processes.')
		return
	time.sleep(1)

	try:
		main_interface(data_changed_flags)
	except:
		print('[ ERROR ] Could not init GUI.')

	print('[ JUDGE ] EXIT Called.')

	# if we are here, it means the GUI has finished.
	os.kill(pid1, signal.SIGINT)		
	os.kill(pid2, signal.SIGINT)

	# Wait until both processes confirm clean exit
	try:
		while data_changed_flags[1] != 1:
			pass
		print('[ JUDGE ][ UNICAST ] Process ended successfully.')
		while  data_changed_flags[2] != 1:
			pass
		print('[ JUDGE ][ BROADCAST ] Process ended successfully.')
	except:
		pass

	print("................ BitsOJ Judge .................\n")


def manage_processes(judge_username, judge_id, data_changed_flags, rabbitmq_username, rabbitmq_password, host):
	listen_common_process = multiprocessing.Process(
		target = communicate_server.listen_server, 
		args = (
			rabbitmq_username,
			rabbitmq_password,
			host,
			judge_username,
			judge_id,
			data_changed_flags,
		)
	)
	listen_uni_process = multiprocessing.Process(
		target = communicate_broadcast_server.listen_server, 
		args = (
			rabbitmq_username,
			rabbitmq_password,
			host,
			judge_username, 
			data_changed_flags,
		)
	)
	listen_uni_process.start()
	listen_common_process.start()

	uni_process_pid = listen_uni_process.pid
	broadcast_pid = listen_common_process.pid
	return uni_process_pid, broadcast_pid

if __name__ == '__main__':
	main()