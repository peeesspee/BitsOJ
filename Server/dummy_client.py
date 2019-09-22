import pika
import time
import threading
import sys
rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'

global client_id
client_id = 'Nul'

username = input('Enter username: ') or 'team1'
password = input('Enter password: ') or 'abcd'

try:
	connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
	channel = connection.channel()
	channel.queue_declare(queue = username, durable = True)
	channel.queue_bind(exchange = 'connection_manager', queue = 'client_requests')
	channel.queue_bind(exchange = 'connection_manager', queue = username)
except:
	print("Error")

def login():
	print("Sending")
	channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = 'LOGIN ' + username + ' ' + password + ' ' + client_id + ' CLIENT')
	print("Sent")

def send():
	global client_id
	print("Sending code")
	code = '#include<iostream>\n int main(void){ std::cout<<"Hello"; return 0; }'
	message = 'SUBMT ' + client_id + ' '  + 'ABCD' + ' ' + 'CPP' + ' ' + '04:05:06' + code
	print ( message)
	channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = message)
	print("sent code")



def handler(ch, method, properties, body):
	global client_id
	server_data = str(body.decode("utf-8"))
	status = server_data[0:5]
	if status == "VALID" :
		status, client_id, server_message = server_data.split('+')
		print("[ Status ] " + status + "\n[ ClientID ] : " + client_id + "\n[ Server ] : " + server_message)
	elif status == "INVLD":
		print("Invalid creds")
	elif status == 'VRDCT':
		print(server_data)
	elif status == 'REJCT' : 
		print(server_data[6:])
	elif status == 'SRJCT':
		print(server_data[6:])
	
	ch.basic_ack(delivery_tag = method.delivery_tag)
	channel.stop_consuming()
		

def listen():
	print("[ LISTEN ]")
	channel.basic_consume(queue = username, on_message_callback = handler)
	try:
		channel.start_consuming()
	except (KeyboardInterrupt, SystemExit):
		channel.stop_consuming()
		#channel.queue_delete(username)
		connection.close()
		print("[ STOP ] Keyboard interrupt")
		sys.exit()


def main():
	login()
	listen()
	
	send()
	listen()
	print('[ DELETE ] Queue ' + username + ' deleted...')
	channel.queue_delete(username)


main()