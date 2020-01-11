import subprocess
import os,sys





def verdict_of_submission(problem_code, language, file_with_ext, time_limit):

	# file,pos,lang = verdict.find_file()
	result = ''
	error = ''
	file_name = file_with_ext.split('.')[0]
	classfile,runfile = verdict.lang_compiler(file_name, file_with_ext, language)
	try:
		verdict.compile_file(classfile,language,problem_code)
	except Exception as error:
		print("error in compiling")
		result = ''
		error = 'Compilation Error'
	verdict.run_file(runfile, problem_code time_limit)
	verdict.remove_object(file_name, file_with_ext, language)
	result = verdict.compare_outputs(problem_code, run_id)
	# print(file,pos,lang)
	# print(classfile,runfile)
	print(result)

	return result,error




class verdict():

	PATH = "./Problems/"

	def find_file():

		for (roots, dirs, files) in os.walk(verdict.PATH):
			for file in files:
				pos = file.count('.')
				if pos == 1:
					pos = file.index('.')
					lang = file[pos+1:]
					if lang == 'c' or lang == 'cpp' or lang == 'java' or lang == 'py':
						return (file, pos, lang)		


	def lang_compiler(file_name, file_with_ext, lang):

		#############################################
		#              example 						# 
		# 		file_name = ABCD18					#
		# 		file_with_ext = ABCD18            	#
		#############################################

		classfile = ''
		runfile = ''

		if lang == 'C++':
			classfile = 'g++ -o ' + file_name + ' ' + file_with_ext
			runfile = './' + file_name

		if lang == 'C':
			classfile = 'gcc -o ' + file_name + ' ' + file_with_ext
			runfile = './' + file_name

		if lang == 'JAVA':
			classfile = 'javac ' + file_with_ext
			runfile = 'java' + file_name

		if lang == 'PYTHON 2':
			classfile = 'python'
			runfile = 'python2 ' + file_with_ext

		if lang == 'PYTHON 3':
			classfile = 'python'
			runfile = 'python3 ' + file_with_ext

		# print(classfile,runfile)
		return(classfile, runfile)

	def compile_file(classfile, lang, problem_code):

		if lang != 'PY2' or lang != 'PY3':
			print("COMPILING...")
			process = subprocess.run(classfile, capture_output=True, text=True, shell=True)
			exit_code = process.returncode
			output = process.stdout
			error = process.stderr
			if exit_code == 0:
				print("COMPILATION SUCCESSFUL")
				return verdict.ERROR
			else :
				verdict.ERROR = True
				verdict.VERDICT = 'CMPL'
				verdict.result = error
				print("COMPILATION ERROR !!!")
				return verdict.ERROR

	def run_file(runfile, problem_code, time_limit):

		INPUT_PATH = './Problems/' + problem_code + '/'
		SUBM_PATH = './submission_files/' 

		if verdict.ERROR == False:
			list_of_inputfiles = os.listdir(INPUT_PATH)

			for file in list_of_inputfiles:
				try:
					pos = file.index('.')
					ext = file[pos+1:]
					if ext == 'in':
						print("STARTED RUNNING SUBMITTED FILE")
						# start = time.time()
						command = 'timeout ' + time_limit + runfile + ' < ' + INPUT_PATH + file + ' > ' + SUBM_PATH + 'output_' + file[:pos]  + '_'+ run_id
						process = subprocess.run(command, capture_output=True, text=True, shell=True)
						print("I am RUNNING")
						print(process)


						if process.returncode != 0 and process.stderr == '':
							print("there is no stderr in run time therefore it is tle")
							verdict.ERROR = True
							verdict.VERDICT = 'TLE'
							verdict.result = 'Time Limit Exceeded !!!'
							os.remove(SUBM_PATH+'output_' + file[:pos]  + '_'+ run_id)
							return verdict.ERROR


						if process.returncode != 0:
							print("there is some Runtime error as returncode is not 0")
							verdict.ERROR = True
							verdict.VERDICT = 'RE'
							verdict.result = process.stderr
							os.remove(SUBM_PATH+'output_' + file[:pos]  + '_'+ run_id)
							return verdict.ERROR


						if process.returncode == 0:
							print("NO RUN TIME ERROR")
							pass

				except:
					pass

			return verdict.ERROR


	def remove_object(file_name, file_with_ext, lang):

		cwd = os.getcwd()
		if lang == 'C' or lang == 'CPP':
			for files in os.listdir(cwd):
				if files == file_with_ext:
					os.remove(file_name)

		# elif lang == 'java':
		# 	for files in os.listdir(verdict.PATH):
		# 		if files == file[:pos] + '.class':
		# 			os.remove(file[:pos] + '.class')

	def remove_white_space(data):
		return data.strip()



	def compare_outputs(problem_code, run_id):

		i = 1
		passed = 0
		cwd = os.getcwd()
		print("I am in compare_outputs->",cwd)
		list_0f_files = os.listdir(cwd)
		print(list_0f_files)
		list_0f_files.sort()
		print(list_0f_files)
		for files in list_0f_files:
			if files[len(files)-3:] == 'ans':
				f = open('output_' + run_id , 'r')
				data = f.read()

				g = open(files, 'r')
				datacmp = g.read()

				if(verdict.remove_white_space(data) == verdict.remove_white_space(datacmp)):
					passed = passed + 1
					

				g.close()
				f.close()
				i = i + 1

		result = ''
				

		if passed + 1 == i and passed != 0:
			print("\nAll test cases passed")
			result = 'AC'
			return result

		else :
			print("No of passed test cases ->", passed)
			result = 'WA'
			return result

	def main(file_name, file_with_ext, lang, problem_code, run_id, timelimit):

		result = 'Nul'
		verd = 'Nul'
		classfile = 'Nul'
		runfile = 'Nul'

		classfile,runfile = verdict.lang_compiler(file_name, file_with_ext, lang)

		e = verdict.compile_file(classfile, lang)
		print(verdict.ERROR)
		print(verdict.VERDICT)
		print(verdict.result)

		if e == True:
			return verdict.VERDICT,verdict.result

		if e == False:
			time_limit = timelimit + 's '
			e = verdict.run_file(runfile, problem_code, run_id, time_limit)

			print(verdict.ERROR)
			print(verdict.VERDICT)
			print(verdict.result)
			verdict.remove_object(file_name, file_with_ext, lang)
			if e == True:
				return verdict.VERDICT,verdict.result

			if e == False:
				result,verd = verdict.compare_outputs(problem_code, run_id)
				return verd,result
