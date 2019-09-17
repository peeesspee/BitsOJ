from database_management import previous_data
global run_id_counter

class submission():
	# Manage a new submission
	def new_submission(client_id, problem_code, language, time_stamp, source_code):
		print("[ SUBMIT ] "+ client_id + " for problem " + problem_code)
		run_id = submission.generate_run_id()
		temp_file_name = run_id
		file_name = submission.make_local_source_file(temp_file_name, source_code, language)
		print ("[ FILE ] New file created for client : "+ client_id + " File name:  " + file_name)
		return run_id, file_name

	# Make a local backup file for the client run id
	def make_local_source_file(file_name, source_code, language):

		if language == "CPP":
			file_extension = ".cpp"
		elif language == "GCC":
			file_extension = ".c"
		elif language == "PY2":
			file_extension = ".py"
		elif language == "PY3":
			file_extension = ".py"
		elif language == "JVA":
			file_extension = ".java"
		else:
			file_extension = ".temp"

		# w : Write mode, + : Create file if not exists
		new_file_name = file_name + file_extension
		print("[ WRITE ] Wrote a new file : " + new_file_name)
		client_local_file = open("Client_Submissions/" + new_file_name, "w+")
		client_local_file.write(source_code)
		client_local_file.close()
		return new_file_name

	def generate_run_id():
		global run_id_counter
		run_id = str("{:05d}".format(run_id_counter))
		run_id_counter = run_id_counter + 1
		return run_id

	def init_run_id():
		global run_id_counter
		# Get max run_id from submissions and add 1 to it, to initialize run_id counter
		run_id_counter = int(previous_data.get_last_run_id()) + 1
		
	
	
