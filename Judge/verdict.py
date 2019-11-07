from file_creation import file_manager
import subprocess
import os
# import filecmp
import multiprocessing
import time

class verdict():

	pwd = os.getcwd()
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

		if lang == 'CPP':
			classfile = 'g++ -o ' + PATH + file_name + ' ' + PATH + file_with_ext
			runfile = PATH + file_name

		if lang == 'C':
			classfile = 'gcc -o ' + PATH + file_name + ' ' + PATH + file_with_ext
			runfile = PATH + file_name

		if lang == 'JVA':
			classfile = 'javac ' + PATH + file_with_ext
			runfile = 'java' + PATH + file_name

		if lang == 'PY':
			if file.split('.')[0][-1] == '2':
				classfile = 'python'
				runfile = 'python2 ' + PATH + file_with_ext

			if file.split('.')[0][-1] == '3':
				classfile = 'python'
				runfile = 'python3 ' + PATH + file_with_ext

		return classfile,runfile

	def compile_file(classfile, lang):

		if lang != 'PY2' or lang != 'PY3':
			print("COMPILING...")
			exit_code = os.system(classfile)
			if exit_code == 0:
				print("COMPILATION SUCCESSFUL")
				return verdict.ERROR
			else :
				verdict.ERROR = True
				verdict.VERDICT = 'CMPL'
				verdict.result = 'COMPILATION ERROR'
				print("SEEMS COMPILATION ERROR")
				return verdict.ERROR
			

	def run_file(runfile, problem_code, run_id):

		INPUT_PATH = './problems/' + problem_code + '/'
		SUBM_PATH = './submission_files/' 

		if verdict.ERROR == False:
			list_of_inputfiles = os.listdir(INPUT_PATH)

			for file in list_of_inputfiles:
				try:
					pos = file.index('.')
					ext = file[pos+1:]
					if ext == 'in':
						print("STARTED RUNNING SUBMITTED FILE")
						start = time.time()
						# command = [runfile , '<' , INPUT_PATH + file , '>' , SUBM_PATH + 'output_' + file[:pos]  + '_' ,run_id]
						x = os.system(runfile + '<' + INPUT_PATH + file + '>' + SUBM_PATH + 'output_' + file[:pos]  + '_'+ run_id)
						end = time.time()
						print("time taken to execute submitted file --->",end-start)
						print(x)
						if x != 0:
							verdict.ERROR = True
							verdict.result = 'Runtime Error'
							verdict.VERDICT = 'RE'
							print("RUNTIME ERROR")
						if x == 0:
							print("NO RUNTIME ERROR")
				except:
					pass

	def remove_object(file_name, file_with_ext, lang):
		# print(PATH)
		# print(verdict.ERROR )
		if (lang == 'C' or lang == 'CPP'):
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
						print(verdict.result)
						print("[TEST CASES PASSED] "+str(cases_passed))	
						verdict.VERDICT = 'WA'
						return verdict.result,verdict.VERDICT

					g.close()
					f.close()

			print("ALL TEST CASES PASSED")
			verdict.result = "All Correct"
			verdict.VERDICT = "AC"
			return verdict.result, verdict.VERDICT

		return verdict.result, verdict.VERDICT

	def main(file_name, file_with_ext, lang, problem_code, run_id,timelimit):

		result = ''
		verd = ''
		classfile = ''
		runfile = ''

		# Process initialised
		# p = multiprocessing.Process(target=verdict.run_file, args=(runfile, problem_code, run_id,))

		classfile,runfile = verdict.lang_compiler(file_name, file_with_ext, lang)

		e = verdict.compile_file(classfile, lang)

		if e == True: #  if there is compilation error
			result = verdict.result
			verd = verdict.VERDICT
			return verd,result
		if e == False:
			p = multiprocessing.Process(target=verdict.run_file, args=(runfile, problem_code, run_id,))
			start = time.time()
			# verdict.run_file(runfile, problem_code, run_id)
			p.start()
			p.join(int(timelimit))
			end = time.time()
			if p.is_alive():
				p.terminate()
				print("Process terminated")
				verdict.ERROR = True
				verdict.result = "Time Limit Exceeded"
				verdict.VERDICT = "TLE"
				print("time taken to execute file",end-start)

			e = verdict.ERROR
			verdict.remove_object(file_name, file_with_ext, lang)

			if e == True:  # if there is run time error
				result = verdict.result
				verd = verdict.VERDICT
				return verd,result
			if e == False: # if there is no compilation error and no run time error  
				result,verd = verdict.compare_outputs(problem_code, run_id)
				print(result)
				print(verd)
				return verd,result


v,r=verdict.main("ABCD1234", "ABCD1234.cpp", "CPP", "ABCD", "1234","3")
print("verdict is --->",v)
print("result is ---->",r)

# _main_ = verdict.trial("ABCD1234", "ABCD1234.cpp")