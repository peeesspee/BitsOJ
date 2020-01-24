from file_creation import file_manager
from init_judge import initialize_judge
import subprocess
import os
import multiprocessing
import time
import signal
import resource

class verdict():

	pwd = os.getcwd()
	pwd = '.'
	ERROR = False
	VERDICT = 'Nul'
	result = 'Nul'

	def lang_compiler(file_name, file_with_ext, lang):

		#############################################
		#              example 						# 
		# 		file_name = ABCD18					#
		# 		file_with_ext = ABCD18.cpp         	#
		#############################################

		classfile = ''
		runfile = ''
		PATH = verdict.pwd + '/submission_files/'

		if lang == 'C++':
			classfile = 'g++ -o ' + PATH + file_name + ' ' + PATH + file_with_ext
			runfile = PATH + file_name

		if lang == 'C':
			classfile = 'gcc -o ' + PATH + file_name + ' ' + PATH + file_with_ext
			runfile = PATH + file_name

		if lang == 'JAVA':
			# classfile = 'javac ' + PATH + file_with_ext
			# runfile = 'java' + PATH + file_name
			
			classfile = 'javac ' + 'bitsoj.java'
			runfile = 'java ' + 'bitsoj'


		if lang == 'PYTHON-2':
			classfile = 'python'
			runfile = 'python2 ' + PATH + file_with_ext

		# if file.split('.')[0][-1] == '3':
		if lang == 'PYTHON-3': 
			classfile = 'python'
			runfile = 'python3 ' + PATH + file_with_ext

		# print(classfile)
		# print(runfile)
		return classfile,runfile

	def compile_file(classfile, lang):

		if lang != 'PYTHON-2' and lang != 'PYTHON-3':
			print("[ JUDGE ] Compiling...")
			process = subprocess.run(classfile, capture_output=True, text=True, shell=True)
			exit_code = process.returncode
			output = process.stdout
			error = process.stderr
			if exit_code == 0:
				print("[ JUDGE ] Compilation Successful")
				return verdict.ERROR
			else :
				verdict.ERROR = True
				verdict.VERDICT = 'CMPL'
				verdict.result = error
				print("[ JUDGE ] Compilation Error")
				return verdict.ERROR

		else:
			print("language is python")
			verdict.ERROR
			

	def run_file(runfile, problem_code, run_id, time_limit, language):

		INPUT_PATH = './problems/' + problem_code + '/'
		SUBM_PATH = './submission_files/' 

		if verdict.ERROR == False:
			################################################################################
			# code for java 
			if language == 'JAVA':
				list_of_inputfiles = os.listdir(INPUT_PATH)
				for file in list_of_inputfiles:
					try:
						pos = file.index('.')
						ext = file[pos+1:]
						if ext == 'in':
							print("[ JUDGE ] Running...")
							command = 'ulimit -p ' + initialize_judge.processlimit + ' && '
							command = command + 'timeout ' + time_limit + runfile + ' < ' + INPUT_PATH + file + ' > ' + SUBM_PATH + 'output_' + file[:pos]  + '_'+ run_id
							# print("command is ->", command)
							process = subprocess.run(command, capture_output=True, text=True, shell=True)
							# print(process)
							# if process.returncode != 0 and process.stderr == '':
							if process.returncode == 124:
								print("[ JUDGE ] Time Limit Exceeded")
								verdict.ERROR = True
								verdict.VERDICT = 'TLE'
								verdict.result = 'Time Limit Exceeded'
								os.remove(SUBM_PATH+'output_' + file[:pos]  + '_'+ run_id)
								return verdict.ERROR

							if process.returncode != 0:
								print("[ JUDGE ] Runtime Error")
								verdict.ERROR = True
								verdict.VERDICT = 'RE'
								verdict.result = process.stderr
								os.remove(SUBM_PATH + 'output_' + file[:pos]  + '_' + run_id)
								return verdict.ERROR

							if process.returncode == 0:
								print("[ JUDGE ] File Run Successful [ No RTE ]")
								pass
					except:
						pass

				return verdict.ERROR

			# For all other Languages, 
			list_of_inputfiles = os.listdir(INPUT_PATH)
			for file in list_of_inputfiles:
				try:
					pos = file.index('.')
					ext = file[pos+1:]
					if ext == 'in':
						print("[ JUDGE ] Running...")
						command = 'ulimit -p ' + initialize_judge.processlimit + ' && '
						command = command + 'timeout ' + time_limit + runfile + ' < ' + INPUT_PATH + file + ' > ' + SUBM_PATH + 'output_' + file[:pos]  + '_'+ run_id
						# print("command is ->", command)
						process = subprocess.run(command, capture_output=True, text=True, shell=True)
						# print(process)


						# if process.returncode != 0 and process.stderr == '':
						if process.returncode == 124:
							print("[ JUDGE ] Time Limit Exceeded")
							verdict.ERROR = True
							verdict.VERDICT = 'TLE'
							verdict.result = 'Time Limit Exceeded'
							os.remove(SUBM_PATH+'output_' + file[:pos]  + '_'+ run_id)
							return verdict.ERROR


						if process.returncode != 0:
							print("[ JUDGE ] Runtime Error")
							verdict.ERROR = True
							verdict.VERDICT = 'RE'
							verdict.result = process.stderr
							os.remove(SUBM_PATH+'output_' + file[:pos]  + '_'+ run_id)
							return verdict.ERROR

						if process.returncode == 0:
							print("[ JUDGE ] File Run Successful [ No RTE ]")
							pass

				except:
					pass

			return verdict.ERROR

	def remove_object(file_name, file_with_ext, lang):
		# print(PATH)
		# print(verdict.ERROR )
		if (lang == 'C' or lang == 'C++'):
			PATH = verdict.pwd + '/submission_files/' + file_name
			os.remove(PATH)

	def remove_white_space(data):
		return data.strip()

	def compare_outputs(problem_code, run_id):

		ANSW_PATH = verdict.pwd + '/problems/' + problem_code + '/' 
		SUBM_PATH = verdict.pwd + '/submission_files/'
		result = 'Nul'
		cases_passed = 0
		if verdict.ERROR == False:
			list_of_submfiles = os.listdir(SUBM_PATH)
			list_of_answfiles = os.listdir(ANSW_PATH)
			for file in list_of_answfiles:
				pos = file.index('.')
				ext = file[pos+1:]
				file_index = file[6:pos]
				if ext == 'ans':
					# Reading answer files
					f = open(ANSW_PATH + 'output' + file_index + '.ans', 'r')
					data = f.read()

					# Reading submitted files
					g = open(SUBM_PATH + 'output_' + 'input' + file_index + '_' + run_id)
					datacmp = g.read()

					if(verdict.remove_white_space(data) == verdict.remove_white_space(datacmp)):
						cases_passed = str(int(cases_passed) + 1)
					else:
						verdict.result = 'Wrong Answer !!!'
						# print(verdict.result)
						print("[ JUDGE ][ WA ] Test cases passed: " + str(cases_passed))	
						verdict.VERDICT = 'WA'
						return verdict.result,verdict.VERDICT

					g.close()
					f.close()

			print("[ JUDGE ][ AC ] All test cases passed")
			verdict.result = "All Correct"
			verdict.VERDICT = "AC"
			return verdict.result, verdict.VERDICT

		return verdict.result, verdict.VERDICT

	def main(file_name, file_with_ext, lang, problem_code, run_id, timelimit):

		result = 'Nul'
		verd = 'Nul'
		classfile = 'Nul'
		runfile = 'Nul'

		classfile,runfile = verdict.lang_compiler(file_name, file_with_ext, lang)

		if lang == 'PYTHON-2' or lang == 'PYTHON-3':
			time_limit = timelimit + 's '
			e = verdict.run_file(runfile, problem_code, run_id, time_limit, lang)
			if e == True:
				result = verdict.result
				verd = verdict.VERDICT
				verdict.VERDICT = 'Nul'
				verdict.result = 'Nul'
				verdict.ERROR = False
				return verd,result

			if e == False:
				result,verd = verdict.compare_outputs(problem_code, run_id)
				verdict.VERDICT = 'Nul'
				verdict.result = 'Nul'
				verdict.ERROR = False
				return verd,result


		e = verdict.compile_file(classfile, lang)
		# print(verdict.ERROR)
		# print(verdict.VERDICT)
		# print(verdict.result)

		if e == True:
			result = verdict.result
			verd = verdict.VERDICT

			verdict.VERDICT = 'Nul'
			verdict.result = 'Nul'
			verdict.ERROR = False
			return verd,result

		if e == False:
			time_limit = timelimit + 's '
			e = verdict.run_file(runfile, problem_code, run_id, time_limit, lang)
			# print(verdict.ERROR)
			# print(verdict.VERDICT)
			# print(verdict.result)
			verdict.remove_object(file_name, file_with_ext, lang)

			if e == True:
				result = verdict.result
				verd = verdict.VERDICT

				verdict.VERDICT = 'Nul'
				verdict.result = 'Nul'
				verdict.ERROR = False
				print(verd,result)
				return verd,result

			if e == False:
				result,verd = verdict.compare_outputs(problem_code, run_id)

				verdict.VERDICT = 'Nul'
				verdict.result = 'Nul'
				verdict.ERROR = False
				return verd,result