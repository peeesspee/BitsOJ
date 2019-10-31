import pika
import time
import threading
import sys
import json
rabbitmq_username = 'judge1'
rabbitmq_password = 'judge1'
host = 'localhost'

global client_id
client_id = 0

username = 'judge00001'
password = 'bits1'
channel = ''
connectio = ''

def login():
	global username
	global password
	global channel
	global connectio
	username = input('Enter judge username: ') or username
	password = input('Enter judge password: ') or password
	try:
		creds = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
		params = pika.ConnectionParameters(host = host, credentials = creds, heartbeat=0, blocked_connection_timeout=0)
		connection = pika.BlockingConnection(params)

		channel1 = connection.channel()
		channel1.queue_declare(queue = username, durable = True)
		channel1.queue_bind(exchange = 'connection_manager', queue = 'client_requests')
		channel1.queue_bind(exchange = 'connection_manager', queue = username)
		channel = channel1
		connectio = connection

	except:
		print("Error")
		return
	print("Sending")
	message = {
		'Code' : 'LOGIN', 
		'Username' : username, 
		'Password' : password,
		'ID' : client_id,
		'Type' : 'JUDGE'
		}
	
	message = json.dumps(message)
	channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = message)
	print("Sent")


def handler(ch, method, properties, body):
	global client_id
	server_data = str(body.decode("utf-8"))
	if(server_data == ''):
		print("Empty!")
		return
	
	try:
		json_data = json.loads(server_data)
		

		code = json_data['Code']
		if code == 'JUDGE':
			run_id = json_data['Run ID']
			username = json_data['Client Username'] 
			client_id = json_data['Client ID']
			language = json_data['Language']
			PCode = json_data['PCode']
			Source = json_data['Source']
			local_run_id = json_data['Local Run ID']
			time_stamp = json_data['Time Stamp']

			message = {
			'Code' : 'VRDCT', 
			'Client Username' : username,
			'Client ID' : client_id,
			'Status' : 'AC',
			'Run ID' : run_id,
			'Message' : 'No Error',
			'Local Run ID' : local_run_id,
			'PCode' : PCode,
			'Time Stamp' : time_stamp
			}
			message = json.dumps(message)
			print('\nRunning....')
			time.sleep(3)

			ch.basic_publish(exchange = 'judge_manager', routing_key = 'judge_verdicts', body = message)
			print('[ JUDGE ] Sent ' + message + "\n\n")
			
		
		elif code =='VALID':
			client_id = json_data['Client ID']
			message = json_data['Message']
			print('[ ' + code + ' ] ::: ' + str(client_id) + ' ::: ' + message  )
			ch.stop_consuming()

		elif code == 'INVLD':
			print("[ INVALID LOGIN ]")
			ch.stop_consuming()

		elif code == 'LRJCT':
			print('Login rejected!')

		ch.basic_ack(delivery_tag = method.delivery_tag)
		return
	except Exception as error:
		print('Error : ' + str(error))



def listen(queue_name):
	global username
	global password
	print("[ LISTEN ] " + queue_name)
	channel.basic_qos(prefetch_count = 1)
	channel.basic_consume(queue = queue_name, on_message_callback = handler)
	try:
		channel.start_consuming()
	except (KeyboardInterrupt, SystemExit):
		return

def main():
	global channel, connectio
	print('1.Login\n2.Start judging\n3.Exit')
	while True:
		a = input('> ')
		if a == '':
			continue
		a = int(a)
		if a == 1:
			login()
			listen(username)
		elif a == 2:
			listen('judge_requests')
		else:
			break;

	channel.stop_consuming()
	print('[ DELETE ] Queue ' + username + ' deleted...')
	channel.queue_delete(username)
	connectio.close()
	print("[ STOP ] Keyboard interrupt")
	return
main()