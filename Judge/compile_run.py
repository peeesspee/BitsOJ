from file_creation import file_manager
import subprocess
import os,sys

class verdict():

	PATH = "./A/test"

	# x = open("./A/gen.cpp", 'r')
	# print(x.read())
	# source_code = x.read()
	# problem_code = 'ARCT'
	# run_id = '112'
	# client_id = '1' 
	# language = 'C++'

	# file_name = file_manager.file_name(run_id, problem_code, language, source_code )

	# file = file_manager.create_file(source_code, language, file_name)

	def find_file():

		for (roots, dirs, files) in os.walk(verdict.PATH):
			for file in files:
				pos = file.count('.')
				if pos == 1:
					pos = file.index('.')
					lang = file[pos+1:]
					if lang == 'c' or lang == 'cpp' or lang == 'java' or lang == 'py':
						return (file, pos, lang)

	def lang_compiler(file, pos, lang):

		classfile = ''
		runfile = ''

		if lang == 'cpp':
			classfile = 'g++ -o ' + file[:pos] + ' ' + file
			runfile = './' + file[:pos]

		if lang == 'c':
			classfile = 'gcc -o ' + file[:pos] + ' ' + file
			runfile = './' + file[:pos]

		if lang == 'java':
			classfile = 'javac ' + file
			runfile = 'java' + file[:pos]

		if lang == 'py':
			if file.split('.')[0][-1] == '2':
				classfile = 'python'
				runfile = 'python2 ' + file

			if file.split('.')[0][-1] == '3':
				classfile = 'python'
				runfile = 'python3 ' + file

		return(classfile, runfile)

	def compile_file(classfile):

		print(os.listdir(verdict.PATH))
		cwd = os.getcwd()
		# print(cwd)
		if classfile != 'python':
			try:
				os.chdir(verdict.PATH)
			except Exception as error:
				print(str(error))
			try:
				os.system(classfile)
			except Exception as error:
				print(str(error))
			
			os.chdir(cwd)

	def run_file(runfile):

		i = 1
		# print(os.listdir(verdict.PATH))
		cwd = os.getcwd()
		print("CUrrent->",cwd)
		os.chdir(verdict.PATH)
		pwd = os.getcwd()
		for file in os.listdir(pwd):
			print(file)
			try:	# in try block because name of the file which does'nt contain '.' will throw error
				pos = file.index('.')
				ext = file[pos+1:]
				if ext == 'in':
					os.system(runfile + ' < ' + file + ' > ' + 'output_' + file[:pos])
					i = i + 1
			except:
				pass
			
			




	# if  file_name.split('.')[1] == 'cpp':
	# 	try:
	# 		tmp = subprocess.call(["g++",file])
	# 		tmp = subprocess.call("./a.out")
	# 		print(tmp)
		
	# 	except Exception as e :
	# 		print(e)


	# if  file_name.split('.')[1] == 'c':
	# 	try:
	# 		tmp = subprocess.call(["gcc",file])
	# 		tmp = subprocess.call("./a.out")
	# 		print(tmp)
		
	# 	except Exception as e :
	# 		print(e)


	# if  file_name.split('.')[1] == 'java':
	# 	try:
	# 		tmp = subprocess.call(["g++",file])
	# 		tmp = subprocess.call("./a.out")
	# 		print(tmp)
		
	# 	except Exception as e :
	# 		print(e)


	# if  file_name.split('.')[1] == 'py':

	# 	if file_name.split('.')[0][-1] == '2':
	# 		try:
	# 			tmp = subprocess.call(["python2",file])
	# 			print(tmp)
			
	# 		except Exception as e :
	# 			print(e)

	# 	if file_name.split('.')[0][-1] == '3':
	# 		try:
	# 			tmp = subprocess.call(["python3",file])
	# 			print(tmp)
			
	# 		except Exception as e :
	# 			print(e)