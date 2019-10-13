import pika
import time
import threading
import sys
import json
rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'

global client_id
client_id = 'Nul'

username = 'team00005'
password = 'rq3bvS'

try:
	connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
	channel = connection.channel()
except:
	print("Error")

def login():
	global username, password, client_id
	username = input('Enter username: ') or username
	password = input('Enter password: ') or password
	print("Sending")
	channel.queue_declare(queue = username, durable = True)
	channel.queue_bind(exchange = 'connection_manager', queue = 'client_requests')
	channel.queue_bind(exchange = 'connection_manager', queue = username)

	message = {
		'Code' : 'LOGIN', 
		'Username' : username, 
		'Password' : password,
		'ID' : client_id,
		'Type' : 'CLIENT'
		}
	
	message = json.dumps(message)

	channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = message)
	print("Sent")

def send():
	global client_id
	print("Sending code")
	code = '#include<iostream>\n int main(void){ std::cout<<"Hello"; return 0; }'

	message = {
		'Code' : 'SUBMT', 
		'ID' : client_id,
		'PCode' : 'ABCD',
		'Language' : 'CPP',
		'Time' : '04:05:06',
		'Source' : code
		}
	message = json.dumps(message)
	
	channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = message)
	print("sent code")



def handler(ch, method, properties, body):
	global client_id
	server_data = str(body.decode("utf-8"))

	json_data = json.loads(server_data)
	code = json_data["Code"]
	if code == 'VRDCT':
		status = json_data['Status']
		run_id = json_data['Run ID']
		message = json_data['Message']
		print("[ Status ] " + status + "\n[ Run ID ] : " + run_id + "\n[ Message ] : " + message)
	elif code =='VALID':
		client_id = json_data['Client ID']
		message = json_data['Message']
		print("[ Response ] " + code + "\n[ Client ID ] : " + client_id + "\n[ Message ] : " + message)

	elif code == 'INVLD':
		print("Invalid creds")

	elif code == 'REJCT' : 
		print('Login Rejected')
		
	elif code == 'SRJCT':
		print('Submission Rejected')

	print("[ ACK ]")
	ch.basic_ack(delivery_tag = method.delivery_tag)
	channel.stop_consuming()
		

def listen():
	print("[ LISTEN ]")
	global username
	channel.basic_consume(queue = username, on_message_callback = handler)
	try:
		print("[ CONSUME ] on " + username)
		channel.start_consuming()
	except (KeyboardInterrupt, SystemExit):
		channel.stop_consuming()
		#channel.queue_delete(username)
		connection.close()
		print("[ STOP ] Keyboard interrupt")
		sys.exit()


def main():
	print('1.Login\n2.Send solution\n3.Send Query\n4.Exit')
	while True:
		a = input('> ')
		if(a == ''):
			continue
		a = int(a)
		if a == 1:
			login()
			listen()
		elif a == 2:
			send()
			listen()
		elif a == 3:
			pass
		else:
			break;
	
	print('[ DELETE ] Queue ' + username + ' deleted...')
	channel.queue_delete(username)


main()