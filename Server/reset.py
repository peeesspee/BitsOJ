from database_management import manage_database
from judge_connections import manage_judges
import pika

superuser_username = 'BitsOJ'
superuser_password = 'root'
host = 'localhost'

conn, cur = manage_database.initialize_database()
manage_database.reset_database(conn)
conn, cur = manage_database.initialize_database()

connection = pika.BlockingConnection(pika.URLParameters("amqp://" + superuser_username + ":" + superuser_password + "@" + host + "/%2f"))
channel = connection.channel()
