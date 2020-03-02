import sqlite3, string
def generate_clients(no_of_clients, max_so_far):
	print(type(no_of_clients))
	print(type(max_so_far))

	client_list = list()
	for i in range(max_so_far + 1, max_so_far + no_of_clients + 1):
		team_number = "{:05d}".format(i)
		client_list.append('team' + str(team_number))

	return client_list

def generate_judges(no_of_judges, max_so_far):
	judge_list = list()
	for i in range(max_so_far+1, max_so_far+no_of_judges+1):
		judge_number = "{:05d}".format(i)
		judge_list.append('judge' + str(judge_number))
	return judge_list
	
def generate_passwords(prev, number, type):
	password_list = list()
	chars=string.ascii_uppercase + string.digits+string.ascii_lowercase
	for i in range(0, number):
		if type == 'Simple':
			password = 'bits'+str(i + prev + 1)
		elif type == 'Random':
			password = ''.join(random.choice(chars) for _ in range(6))

		password_list.append(password)
	return password_list

def generate_n_users(no_of_clients, no_of_judges, password_type, conn):
	cur = conn.cursor()
	
	max_client_username = 0
	max_judge_username = 0
	
	client_list = generate_clients(no_of_clients, max_client_username)
	judge_list = generate_judges(no_of_judges, max_judge_username)
	client_pass_list = generate_passwords(max_client_username, no_of_clients, password_type)
	judge_pass_list = generate_passwords(max_judge_username, no_of_judges, password_type)

	# Generate list of tuples for client
	final_client_list = []
	for i in range(0, no_of_clients):
		client_tuple = (client_list[i], client_pass_list[i], 'CLIENT')
		final_client_list.append(client_tuple)
	# Generate list of tuples for judge
	final_judge_list = []
	for i in range(0, no_of_judges):
		judge_tuple = (judge_list[i], judge_pass_list[i], 'JUDGE')
		final_judge_list.append(client_tuple)

	try:
		conn.executemany("INSERT into accounts values (?, ?, ? )", final_client_list)
		conn.executemany("INSERT into accounts values (?, ?, ? )", final_judge_list)
		conn.commit()
	except Exception as error:
		print('[ CRITICAL ] Database insertion error: ' + str(error))
		cur.close()
		return 0
	finally:
		cur.close()
		return 1
	

conn = sqlite3.connect(
	'server_database.db'
)

conn.execute('DELETE FROM accounts')

number_of_clients = input('Enter number of Clients: ') or 500
number_of_judges = input('Enter number of Judges: ') or 0

generate_n_users(int(number_of_clients), int(number_of_judges), 'Simple', conn)
conn.close()