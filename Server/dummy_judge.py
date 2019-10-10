import pika
import time
import threading
import sys
rabbitmq_username = 'judge1'
rabbitmq_password = 'judge1'
host = 'localhost'

global client_id
client_id = 'Nul'

username = ''
password = ''

try:
	connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
	channel = connection.channel()
	channel.queue_declare(queue = username, durable = True)
	channel.queue_bind(exchange = 'connection_manager', queue = 'client_requests')
	channel.queue_bind(exchange = 'connection_manager', queue = username)
except:
	print("Error")

def login():
	global username
	global password
	username = input('Enter judge username: ') or 'judge1'
	password = input('Enter judge password: ') or 'judge1'
	print("Sending")
	channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = 'LOGIN ' + username + ' ' + password + ' ' + client_id + ' JUDGE')
	print("Sent")


def handler(ch, method, properties, body):
	global client_id
	server_data = str(body.decode("utf-8"))
	status = server_data[0:5]
	if status == "VALID" :
		print('LOGGED IN')
		ch.basic_ack(delivery_tag = method.delivery_tag)
		channel.stop_consuming()
	elif status == "INVLD":
		print("Invalid creds")
		ch.basic_ack(delivery_tag = method.delivery_tag)
		channel.stop_consuming()
		sys.exit()
	elif status == 'JUDGE':
		run_id = server_data[6:11]
		message = 'VRDCT+' + str(run_id) + '+AC+No_error'
		ch.basic_publish(exchange = 'judge_manager', routing_key = 'judge_verdicts', body = message)
		print('[ JUDGE ] Sent ' + message)
		return
	
	
def listen():
	global username
	global password
	print("[ LISTEN ]")
	channel.basic_consume(queue = 'judge_requests', on_message_callback = handler)
	try:
		channel.start_consuming()
	except (KeyboardInterrupt, SystemExit):
		channel.stop_consuming()
		connection.close()
		print("[ STOP ] Keyboard interrupt")
		sys.exit()

def listen1():
	global username
	global password
	print("[ LISTEN ]")
	channel.basic_consume(queue = username, on_message_callback = handler)
	try:
		channel.start_consuming()
	except (KeyboardInterrupt, SystemExit):
		channel.stop_consuming()
		connection.close()
		print("[ STOP ] Keyboard interrupt")
		sys.exit()


def main():
	print('1.Login\n2.Start judging\n3.Exit')
	while True:
		a = input('> ')
		if a == '':
			continue
		a = int(a)
		if a == 1:
			login()
			listen1()
		elif a == 2:
			listen()
		else:
			break;
	
	print('[ DELETE ] Queue ' + username + ' deleted...')
	channel.queue_delete(username)


main()