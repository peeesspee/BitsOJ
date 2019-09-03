import subprocess
import os
Language = ['C', 'C++', 'Python', 'Java']

def self_judgement():
	file_path = input('Enter File path : ')
	for i in Language:
		print(i)
	language = input('Select Language : ')
	if(language == 'C'):
		os.system('g++ -o a ' + file_path)
		os.system('./a')
	else:
		pass

self_judgement()