import pika
import time
import threading
import sys
import json
rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'

global client_id, mode, channel, connection

mode = 1
client_id = '1'

username = 'team00001'
password = 'bits1'
key = 'fQ40S4J'



def connect():
	global channel, connection
	try:
		creds = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
		params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
		connection = pika.BlockingConnection(params)
		channel = connection.channel()
		channel.queue_declare(queue = username, durable = True)
		channel.queue_bind(exchange = 'connection_manager', queue = 'client_requests')
		channel.queue_bind(exchange = 'connection_manager', queue = username)
	except:
		print("Error")

def handler(ch, method, properties, body):
	global client_id, mode
	server_data = str(body.decode("utf-8"))
	try:
		json_data = json.loads(server_data)
		code = json_data["Code"]
		if code == 'RESPONSE':
			run_id = json_data['Run ID']
			print(' RUN ID: ', run_id)
		elif code == 'VRDCT':
			status = json_data['Status']
			run_id = json_data['Run ID']
			message = json_data['Message']
			print("[ Status ] " + status + "\n[ Run ID ] : " + str(run_id) + "\n[ Message ] : " + message)
		elif code =='VALID':
			client_id = json_data['Client ID']
			message = json_data['Message']
			print("[ Response ] " + code + "\n[ Client ID ] : " + str(client_id) + "\n[ Message ] : " + message)
		elif code == 'INVLD':
			print("Invalid creds")
		elif code == 'LRJCT' : 
			print('Login Rejected')
		elif code == 'SRJCT':
			print('Submission Rejected: ' + json_data['Message'])
		elif code == 'DSCNT':
			type = json_data['Client']
			if type == username:
				print('Houston! We have a problem!\nServer dudes disconnected us :(')
			elif type == 'All':
				print('Everyone has been disconnected! #Maintainance_Break')
		else:
			print(json_data)

	except:
		print('Could not parse message!')
	finally:
		print("[ ACK ]")
		ch.basic_ack(delivery_tag = method.delivery_tag)
		if mode == 1:
			channel.stop_consuming()

def listen():
	global channel, connection
	print("[ LISTEN ]")
	global username
	channel.basic_consume(queue = username, on_message_callback = handler)
	try:
		print("[ CONSUME ] on " + username)
		channel.start_consuming()
	except (KeyboardInterrupt, SystemExit):
		print("[ STOP ] Keyboard interrupt")
		return

def login():
	global channel, connection
	global username, password, client_id, key
	username = input('Enter username: ') or username
	password = input('Enter password: ') or password
	print("Sending")
	
	message = {
		'Client Key' : key,
		'Code' : 'LOGIN', 
		'Username' : username, 
		'Password' : password,
		'ID' : client_id,
		'Type' : 'CLIENT',
		'IP' : '   192.168.0.0'
		}
	
	message = json.dumps(message)

	channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = message)
	print("Sent")

def send():
	global channel, connection
	global client_id, key, username
	print("Sending code")
	code = '#include<iostream>\n int main(void){ std::cout<<"Hello"; return 0; }'
	ctime = time.strftime("%H:%M:%S", time.localtime())
	message = {
		'Client Key' : key,
		'Code' : 'SUBMT', 
		'Username' : username,
		'ID' : client_id,
		'PCode' : 'SXS',
		'Language' : 'C++',
		'Time' : ctime,
		'Source' : code,
		'Local Run ID' : 1,
		'IP' : '192.168.0.0'
		}
	message = json.dumps(message)
	channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = message)
	
def load_test(mode = 1):
	global channel, connection
	global client_id, key, username
	print(":::::::::: LOAD TEST ::::::::::")
	code = '#include<iostream>\n int main(void){ std::cout<<"Hello"; return 0; }'
	ctime = time.strftime("%H:%M:%S", time.localtime())

	while(True):
		try:
			time.sleep(0.5)
			message = {
				'Client Key' : key,
				'Code' : 'SUBMT', 
				'Username' : username,
				'ID' : client_id,
				'PCode' : 'TQL',
				'Language' : 'C++',
				'Time' : ctime,
				'Source' : code,
				'Local Run ID' : 1,
				'IP' : '192.168.1.2'
				}
			message = json.dumps(message)
			channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = message)
			if mode == 1:
				listen()
		except KeyboardInterrupt:
			break

def main():
	global channel, connection
	global username, key
	connect()
	while True:
		print('\n\n' + '#' * 70)
		print('1.Login\n2.Send solution\n3.Listen\n4.Load Test [ LISTEN ]\n5.Load Test [ CONTINUOUS ]\n6.Exit')
		a = input('> ')
		if(a == ''):
			continue
		a = int(a)

		if a == 1:
			login()
		elif a == 2:
			send()
			listen()
		elif a == 3:
			listen()
		elif a == 4:
			load_test()
		elif a == 5:
			load_test(2)
		elif a == 6:
			try:
				print('[ SHUTTING DOWN ')
				message = {
					'Client Key' : key,
					'Code' : 'DSCNT', 
					'ID' : client_id,
					'Username' : username,
					'IP' : '192.168.0.0'
					}
				message = json.dumps(message)
				channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = message)
				print('Published shutdown message...')
				listen()
				print('Shutdown')
				channel.queue_delete(username)
				connection.close()
				
			except Exception as e:
				print("Could not stop listening to the Server: ", e)
			finally:
				print('[ DELETE ] Queue ' + username + ' deleted...')
				break;
		else:
			continue;


	
	

main()