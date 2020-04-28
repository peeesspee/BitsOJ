class file_manager():
	def create_file(source_code, language, file_name):
		
		# if code is in C++
	    if language == 'C++':
	        with open("./submission_files/"+file_name , "w") as file:
	            file.write(source_code)
	            return file_name

		# if code is in C
	    if language == 'C':
	        with open("./submission_files/"+file_name, 'w') as file:
	            file.write(source_code)
	            return file_name

	    #if code is in Java
	    if language == 'JAVA':
	    	with open("bitsoj.java", 'w') as f:
	    		f.write(source_code)

	    	with open("./submission_files/"+file_name, 'w') as file:
	    		file.write(source_code)
	    		return file_name

		# if code is in Python2
	    if language == 'PYTHON-2':
	        with open("./submission_files/"+file_name, 'w') as file:
	            file.write(source_code)
	            return file_name

	    # if code is in Python3
	    if language == 'PYTHON-3':
	        with open("./submission_files/"+file_name, 'w') as file:
	            file.write(source_code)
	            return file_name



	def file_name(run_id, problem_code, language, source_code ):
		file_name = 'Nul'

		if language == 'C++':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + '.cpp'

		if language == 'C':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + '.c'

		if language == 'JAVA':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + '.java'

		if language == 'PYTHON-2':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + 'P2' + '.py'

		if language == 'PYTHON-3':
			file_name = problem_code + run_id
			file_with_ext = problem_code + run_id + 'P3' + '.py'

		if file_name == 'Nul':
			print("File Name not well-defined")
			return "INVALID FILENAME"

		return file_name,file_with_ext

