import subprocess
import os,sys



class judge():

	pwd = '.'
	ERROR = False
	VERDICT = 'Nul'
	result = 'Nul'

	def main(language, problem_code, time_limit, file_path):
		file_name = file_path.split('/')
		file_name_1 = file_path.split('/')
		file_name = file_name[len(file_name) - 1].split('.')[0]
		file_name_ext = './Problems/' + problem_code + '/' + file_name_1[len(file_name_1) - 1]

		classfile,runfile = judge.lang_compiler(file_name_ext,language)
		try:
			e = judge.compile_file(classfile,problem_code, language)
		except Exception as error:
			print("error in compiling")
			result = ''
			error = 'Compilation Error'

		if e == True:
			return judge.VERDICT

		if e == False:
			time_limit = str(time_limit) + 's '
			e = judge.run_file(runfile, problem_code, time_limit)

		judge.remove_object(file_name, file_name_ext, language)
		result = judge.compare_outputs(problem_code)

		return result



	def lang_compiler(file_name_ext,language):

		classfile = ''
		runfile = ''
		file_name = '.' + file_name_ext.split('.')[1]
		if language == 'C++':
			classfile = 'g++ -o ' + file_name + ' ' + file_name_ext
			runfile = file_name

		if language == 'C':
			classfile = 'gcc -o ' + file_name + ' ' + file_name_ext
			runfile = file_name

		if language == 'JAVA':
			classfile = 'javac ' + file_name_ext
			runfile = 'java' + file_name

		if language == 'PYTHON 2':
			classfile = 'python'
			runfile = 'python2 ' + file_name_ext

		if language == 'PYTHON 3':
			classfile = 'python'
			runfile = 'python3 ' + file_name_ext

		
		return classfile, runfile


	def compile_file(classfile,language,problem_code):
		if language != 'PYTHON 2' or language != 'PYTHON 3':
			process = subprocess.run(classfile, capture_output=True, text=True, shell=True)
			exit_code = process.returncode
			output = process.stdout
			error = process.stderr
			if exit_code == 0:
				judge.ERROR = False
				print("COMPILATION SUCCESSFUL")
				return judge.ERROR
			else :
				judge.ERROR = True
				judge.VERDICT = 'CMPL'
				judge.result = error
				print("COMPILATION ERROR !!!")
				return judge.ERROR
		else:
			pass
		

	def run_file(runfile,problem_code,time_limit):

		INPUT_PATH = './Problems/' + problem_code + '/'
		SUBM_PATH = './Problems/' + problem_code + '/' 

		if judge.ERROR == False:
			list_of_inputfiles = os.listdir(INPUT_PATH)
			list_of_inputfiles.sort()

			for file in list_of_inputfiles:
				try:
					pos = file.index('.')
					ext = file[pos+1:]
					if ext == 'in':
						command = 'timeout ' + time_limit + runfile + ' < ' + INPUT_PATH + file + ' > ' + SUBM_PATH + 'output_' + file[:pos]
						process = subprocess.run(command, capture_output=True, text=True, shell=True)


						if process.returncode != 0 and process.stderr == '':
							judge.ERROR = True
							judge.VERDICT = 'TLE'
							judge.result = 'Time Limit Exceeded !!!'
							os.remove(SUBM_PATH+'output_' + file[:pos]  + '_'+ run_id)
							return judge.ERROR


						if process.returncode != 0:
							judge.ERROR = True
							judge.VERDICT = 'RE'
							judge.result = process.stderr
							os.remove(SUBM_PATH+'output_' + file[:pos]  + '_'+ run_id)
							return judge.ERROR


						if process.returncode == 0:
							pass

				except:
					pass

			return judge.ERROR


	def remove_object(file_name, file_with_ext, language):
		cwd = os.getcwd()
		if language == 'C' or language == 'CPP':
			for files in os.listdir(cwd):
				if files == file_with_ext:
					os.remove(file_name)

	def compare_outputs(problem_code):
		i = 1
		passed = 0
		cwd = './Problems/SAC/'
		list_0f_files = os.listdir(cwd)
		list_0f_files.sort()
		for files in list_0f_files:
			if files[len(files)-3:] == 'ans':
				f = open(cwd + 'output_input' + files[len(files)-6:len(files)-4] , 'r')
				data = f.read()

				g = open(cwd + files, 'r')
				datacmp = g.read()

				if(judge.remove_white_space(data) == judge.remove_white_space(datacmp)):
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

	def remove_white_space(data):
		return data.strip()

