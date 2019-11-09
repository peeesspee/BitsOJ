from database_management import manage_database
from judge_connections import manage_judges
from init_server import save_status
import pika

superuser_username = 'BitsOJ' 
superuser_password = 'root'
host = 'localhost'

conn, cur = manage_database.initialize_database()
manage_database.reset_database(conn)
conn, cur = manage_database.initialize_database()

connection = pika.BlockingConnection(
	pika.URLParameters("amqp://" + superuser_username + ":" + superuser_password + "@" + host + "/%2f")
	)
channel = connection.channel()

save_status.write_config(
		'BitsOJ', 
		'root', 
		'judge1', 
		'judge1', 
		'localhost', 
		'True', 
		'True',
		'True', 
		'True',
		'000000000000000', 
		'000000000000000', 
		'papa', 
		'02:00:00',
		'SETUP',
		'00:00:00',
		'00:00:00',
		0
		)

