import pika
from connection import manage_connection

class communicate_server():
	message = ''

	print("\n......Judge is Communicating with Server.......\n")

	def listen_server():

		channel = manage_connection.connect_me()
		channel.queue_declare( queue = 'judge_requests', durable=True )
		channel.exchange_declare( exchange = 'judge_manager', exchange_type = 'direct', durable = True)
		channel.queue_bind( exchange = 'judge_manager', queue = 'judge_verdicts')


		channel.queue_declare( queue = 'judge_verdicts', durable=True )
		channel.exchange_declare( exchange = 'judge_manager', exchange_type = 'direct', durable = True)
		channel.queue_bind( exchange = 'judge_manager', queue = 'judge_verdicts')


		# message = 'VRDCT' + '+AC+' + 'NO-ERROR'
		# communicate_server.message = 'VRDCT+' + communicate_server.message + '+AC+' + 'NO-ERROR'

		
		channel.basic_consume(queue = 'judge_requests', on_message_callback = communicate_server.server_response_handler, auto_ack = True)
		
		channel.start_consuming()

	
	def server_response_handler(ch, method, properties, body):
		message = body.decode('utf-8')
		print(message)
		x = message[6:11]
		print(x)
		communicate_server.message = 'VRDCT+' + x + '+AC+' + 'NO-ERROR'

		ch.basic_publish(
			exchange = 'judge_manager',
			routing_key = 'judge_verdicts',
			body = communicate_server.message
			)

		





