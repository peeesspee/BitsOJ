import pika
from connection import manage_connection
from init_judge import initialize_judge
from login_request import authenticate_judge
from verdict import verdict
from file_creation import file_manager
import time, json, os

class communicate_uni_server():
	message = ''
	key = initialize_judge.key()
	my_ip = initialize_judge.my_ip()
	

	def listen_server(judge_username, channel):
		channel.queue_declare( queue = judge_username, durable=True )
		channel.exchange_declare( 
			exchange = 'judge_manager', 
			exchange_type = 'direct', 
			durable = True
		)
		channel.exchange_declare( 
			exchange = 'judge_broadcast_manager', 
			exchange_type = 'fanout', 
			durable = True
		)
		channel.queue_bind( exchange = 'judge_manager', queue = 'judge_verdicts')
		channel.queue_bind( exchange = 'judge_broadcast_manager', queue = judge_username)

		channel.queue_declare( queue = 'judge_verdicts', durable=True )
		channel.exchange_declare( exchange = 'judge_manager', exchange_type = 'direct', durable = True)
		channel.queue_bind( exchange = 'judge_manager', queue = 'judge_verdicts')

		channel.basic_qos(prefetch_count = 1)
				
		channel.basic_consume(queue = 'judge_requests', on_message_callback = communicate_server.server_response_handler, auto_ack = True)
		# print("[ERROR]" + "error in consuming") 
		channel.start_consuming()


	
	def server_response_handler(ch, method, properties, body):
		server_data = body.decode('utf-8')
		print(server_data)
