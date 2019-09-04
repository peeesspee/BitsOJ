
class submission():
	def new_submission(client_id, problem_code, language, time_stamp, source_code):
		print("[ SUBMIT ] "+ client_id + " for problem " + problem_code)
		run_id = generate_run_id()
		file_name = "Client Submissions/" + client_id + '_' + problem_code + '_' + run_id
		print ("[ FILE ] "+ client_id + " : " + file_name)
		make_source_file(file_name, source_code, language)

		return

	def make_source_file(file_name, source_code, language):
		if language == "cpp":
			ext = ".cpp"
		elif language == "gcc":
			ext = ".c"
		elif language == "py2":
			ext = ".py"
		elif language == "py3":
			ext = ".py"
		elif language == "jva":
			ext = ".java"

		# w : Write mode, + : Create file if not exists
		client_local_file = open(file_name, "w+")
		client_local_file.write(source_code)
		client_local_file.close()
		return

	def generate_run_id():
		return '0001'

	def judge_submission(source_code, language, problem_code):
		return

	