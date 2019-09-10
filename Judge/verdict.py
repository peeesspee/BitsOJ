from file_creation import file_manager
import subprocess

class verdict():


	x = '#include<stdio.h> \nusing namespace std; \nint main() \n { \n printf("hello world!"); \n }'
	code = x
	problem_code = 'ARCT'
	run_id = '112' 
	client_id = '1' 
	language = 'C++'

	file_name = file_manager.file_name(code, problem_code, run_id, client_id, language)

	file = file_manager.create_file(code, language, file_name)

	tmp = subprocess.call(["g++",file])
	tmp = subprocess.call("./a.out")

	print(tmp)

	





