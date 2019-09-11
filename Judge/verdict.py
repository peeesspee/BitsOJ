from file_creation import file_manager
import subprocess


class verdict():


	x = 'x = "ram.123"\ninr = x.split(".")[1]\nprint(inr)'
	source_code = x
	problem_code = 'ARCT'
	run_id = '112'
	client_id = '1' 
	language = 'PY2'
 
	# x = open("123.cpp", "r")
	# print(x.read())
	# print("................. \n ..................")

	file_name = file_manager.file_name(run_id, problem_code, language, source_code )

	file = file_manager.create_file(source_code, language, file_name)

	if  file_name.split('.')[1] == 'cpp':
		try:
			tmp = subprocess.call(["g++",file])
			tmp = subprocess.call("./a.out")
			print(tmp)
		
		except Exception as e :
			print(e)


	if  file_name.split('.')[1] == 'c':
		try:
			tmp = subprocess.call(["g++",file])
			tmp = subprocess.call("./a.out")
			print(tmp)
		
		except Exception as e :
			print(e)


	if  file_name.split('.')[1] == 'java':
		try:
			tmp = subprocess.call(["g++",file])
			tmp = subprocess.call("./a.out")
			print(tmp)
		
		except Exception as e :
			print(e)


	if  file_name.split('.')[1] == 'py':
		try:
			tmp = subprocess.call(["python2",file])
			print(tmp)
		
		except Exception as e :
			print(e)

	





