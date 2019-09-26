from database_management import manage_database
from judge_connections import manage_judges
import pika

superuser_username = 'BitsOJ'
superuser_password = 'root'
host = 'localhost'

conn, cur = manage_database.initialize_database()
manage_database.reset_database(conn)
conn, cur = manage_database.initialize_database()

manage_database.insert_user("team1", "abcd", cur, conn)
manage_database.insert_user("dummy", "dummy", cur, conn)
manage_database.insert_user("judge1", "judge1", cur, conn)

connection = pika.BlockingConnection(pika.URLParameters("amqp://" + superuser_username + ":" + superuser_password + "@" + host + "/%2f"))
channel = connection.channel()
