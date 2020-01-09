from file_creation import file_manager
import subprocess
import os,sys

class verdict():

	PATH = "./submission_files/"

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

		if lang == 'CPP':
			classfile = 'g++ -o ' + file_name + ' ' + file_with_ext
			runfile = './' + file_name

		if lang == 'C':
			classfile = 'gcc -o ' + file_name + ' ' + file_with_ext
			runfile = './' + file_name

		if lang == 'JVA':
			classfile = 'javac ' + file_with_ext
			runfile = 'java' + file_name

		if lang == 'PY':
			if file.split('.')[0][-1] == '2':
				classfile = 'python'
				runfile = 'python2 ' + file_with_ext

			if file.split('.')[0][-1] == '3':
				classfile = 'python'
				runfile = 'python3 ' + file_with_ext

		return(classfile, runfile)

	def compile_file(classfile,lang):

		print(os.listdir(verdict.PATH))
		cwd = os.getcwd()
		# print(cwd)
		if lang != 'PY2' or lang != 'PY3':
			try:
				os.chdir(verdict.PATH)
			except Exception as error:
				print(str(error))
			try:
				os.system(classfile)
				print(classfile)
			except Exception as error:
				print(str(error))
	
			os.chdir(cwd)

	def run_file(runfile, problem_code, run_id):

		# print(os.listdir(verdict.PATH))
		cwd = os.getcwd()
		print("in run file CUrrent->",cwd)
		os.chdir(verdict.PATH)
		pwd = os.getcwd()
		input_file_count = ''
		i = 1
		for file in os.listdir(pwd):
			print(file)
			try:	# in try block because name of the file which does'nt contain '.' will throw error
				pos = file.index('.')
				ext = file[pos+1:]
				if ext == 'in' and file == (problem_code + input_file_count  + '.in'):
					os.system(runfile + ' < ' + file + ' > ' + 'output_' + run_id )
					input_file_count = str(i)
					i = i + 1
			except:
				pass
		# os.chdir(cwd)
		cwd = os.getcwd()
		print("CUrrent->",cwd)


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

