class file_manager():


	def create_file(source_code, language, file_name):
		# if code is in C++
	    if language == 'CPP':
	        with open("./submission_files/"+file_name , "w") as file:
	            file.write(source_code)
	            return file_name

		# if code is in C
	    if language == 'GCC':
	        with open("./submission_files/"+file_name, 'w') as file:
	            file.write(source_code)
	            return file_name

		# if code is in Java
	    if language == 'JVA':
	        with open("./submission_files/"+file_name, 'w') as file:
	            file.write(source_code)
	            return file_name

		# if code is in Python2
	    if language == 'PY2':
	        with open("./submission_files/"+file_name, 'w') as file:
	            file.write(source_code)
	            return file_name

	    # if code is in Python3
	    if language == 'PY3':
	        with open("./submission_files/"+file_name, 'w') as file:
	            file.write(source_code)
	            return file_name



	def file_name(run_id, problem_code, language, source_code ):
		file_name = 'Nul'

		if language == 'CPP':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + '.cpp'

		if language == 'GCC':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + '.c'

		if language == 'JVA':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + '.java'

		if language == 'PY2':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + 'P2' + '.py'

		if language == 'PY3':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + 'P3' + '.py'

		if file_name == 'Nul':
			print("File Name not well-defined")
			return "INVALID FILENAME"

		return file_name,file_with_ext

