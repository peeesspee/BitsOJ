from file_creation import file_manager
import subprocess


class verdict():


	x = open("./A/sol.cpp", 'r')
	print(x.read())
	source_code = x.read()
	problem_code = 'ARCT'
	run_id = '112'
	client_id = '1' 
	language = 'C++'
 
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
			tmp = subprocess.call(["gcc",file])
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

		if file_name.split('.')[0][-1] == '2':
			try:
				tmp = subprocess.call(["python2",file])
				print(tmp)
			
			except Exception as e :
				print(e)

		if file_name.split('.')[0][-1] == '3':
			try:
				tmp = subprocess.call(["python3",file])
				print(tmp)
			
			except Exception as e :
				print(e)

	





