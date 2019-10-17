class file_manager():


	def create_file(source_code, language, file_name):
		# if code is in C++
	    if language == 'C++':
	        with open("./A/test/file_name" , "w") as file:
	            file.write(source_code)
	            return file_name

		# if code is in C
	    if language == 'GCC':
	        with open(file_name, 'w') as file:
	            file.write(source_code)
	            return file_name

		# if code is in Java
	    if language == 'JVA':
	        with open(file_name, 'w') as file:
	            file.write(source_code)
	            return file_name

		# if code is in Python2
	    if language == 'PY2':
	        with open(file_name, 'w') as file:
	            file.write(source_code)
	            return file_name

	    # if code is in Python3
	    if language == 'PY3':
	        with open(file_name, 'w') as file:
	            file.write(source_code)
	            return file_name



	def file_name(run_id, problem_code, language, source_code ):

	    if language == 'C++':
	        file_name = run_id + '.cpp'

	    if language == 'GCC':
	        file_name = run_id + '.c'

	    if language == 'JVA':
	        file_name = run_id + '.java'

	    if language == 'PY2':
	        file_name = run_id + 'P2' + '.py'

	    if language == 'PY3':
	        file_name = run_id + 'P3' + '.py'


	    return file_name

