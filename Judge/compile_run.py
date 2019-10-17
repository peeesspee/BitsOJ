from file_creation import file_manager
import subprocess
import os,sys

class verdict():

	PATH = "./A/test"

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

		# print(os.listdir(verdict.PATH))
		cwd = os.getcwd()
		print("in run file CUrrent->",cwd)
		os.chdir(verdict.PATH)
		pwd = os.getcwd()
		i = 1
		for file in os.listdir(pwd):
			print(file)
			try:	# in try block because name of the file which does'nt contain '.' will throw error
				pos = file.index('.')
				ext = file[pos+1:]
				if ext == 'in':
					os.system(runfile + ' < ' + file + ' > ' + 'output_' + file[:pos] )
					i = i + 1
			except:
				pass
		# os.chdir(cwd)
		cwd = os.getcwd()
		print("CUrrent->",cwd)


	def remove_object(file, lang, pos):

		cwd = os.getcwd()
		if lang == 'c' or lang == 'cpp':
			for files in os.listdir(cwd):
				if files == file[:pos]:
					os.remove(file[:pos])

		elif lang == 'java':
			for files in os.listdir(verdict.PATH):
				if files == file[:pos] + '.class':
					os.remove(file[:pos] + '.class')

	def remove_white_space(data):
		return data.strip()



	def compare_outputs():

		i = 1
		passed = 0
		cwd = os.getcwd()
		list_0f_files = os.listdir(cwd)
		print(list_0f_files)
		list_0f_files.sort()
		print(list_0f_files)
		for files in list_0f_files:
			if files[len(files)-3:] == 'ans':
				f = open('output_' + files[:len(files) - 4], 'r')
				data = f.read()

				g = open(files, 'r')
				datacmp = g.read()

				if(verdict.remove_white_space(data) == verdict.remove_white_space(datacmp)):
					passed = passed + 1
					

				g.close()
				f.close()
				i = i + 1

		verdict = ''
				

		if passed + 1 == i and passed != 0:
			print("\nAll test cases passed")
			verdict = 'AC'
			return verdict

		else :
			print("No of passed test cases ->", passed)
			verdict = 'WA'
			return verdict

