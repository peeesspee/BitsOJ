from database_management import manage_database

rabbitmq_username = 'client'
rabbitmq_password = 'client'
host = 'localhost'

conn, cur = manage_database.initialize_table()
manage_database.reset_database(conn)
