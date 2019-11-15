import subprocess
import os,sys


class judge():

	def main(language, problem_code, time_limit, file_path):
		file_name = file_path.split('/')
		file_name_1 = file_path.split('/')
		file_name = file_name[len(file_name) - 1].split('.')[0]
		file_name_ext = file_name_1[len(file_name_1) - 1]

		classfile,runfile = judge.lang_compiler(file_name_ext,language)

		try:
			judge.compile_file(classfile,language,problem_code)
		except Exception as error:
			print("error in compiling")
			result = ''
			error = 'Compilation Error'



	def lang_compiler(file_name_ext,language):

		classfile = ''
		runfile = ''
		file_name = file_name_ext.split('.')[0]

		if language == 'C++':
			classfile = 'g++ -o ' + file_name + ' ' + file_name_ext
			runfile = './' + file_name

		if language == 'C':
			classfile = 'gcc -o ' + file_name + ' ' + file_name_ext
			runfile = './' + file_name

		if language == 'JAVA':
			classfile = 'javac ' + file_name_ext
			runfile = 'java' + file_name

		if language == 'PYTHON 2':
			classfile = 'python'
			runfile = 'python2 ' + file_name_ext

		if language == 'PYTHON 3':
			classfile = 'python'
			runfile = 'python3 ' + file_name_ext

		# print(classfile,runfile)
		return classfile, runfile


judge.main('C++','SAC',1,'/home/sj1328/Desktop/sachinam/Kodeathon A3/Problem_1/correct.cpp')