from file_creation import file_manager
from connection import manage_connection
from login_request import authenticate_judge 

rabbitmq_username = "judge1"
rabbitmq_password = "judge1"
host = "192.168.43.239"


channel,connection = manage_connection.initialize_connection(rabbitmq_username,rabbitmq_password,host)

print(type (channel))


while (True):
    status = authenticate_judge.login(channel, host)




manage_connection.terminate_connection(connection)







