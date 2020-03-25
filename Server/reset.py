from database_management import manage_database
from judge_connections import manage_judges
from init_server import save_status
import pika

superuser_username = 'BitsOJ' 
superuser_password = 'root'
host = 'localhost'

manage_database()
manage_database.reset_database()
manage_database.init_tables()
