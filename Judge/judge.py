from file_creation import file_manager
from connection import manage_connection
from login_request import login

rabbitmq_username = "judge1"
rabbitmq_password = "judge1"
host = "localhost"


channel,connection = manage_connection.initialize_connection(rabbitmq_username,rabbitmq_password,host)


while (True):
    status = authenticate_judge.login()


manage_connection.terminate_connection(connection)







