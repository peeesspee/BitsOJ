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


save_status.write_config()

