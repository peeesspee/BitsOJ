import os
import PyPDF2
import json
from init_client import handle_config


# Class to handle the decryption process of the problems
class decrypt():

	# Function to decrypt
	def decrypting():
		# read config file
		data = handle_config.read_config_json()
		# read contest config file
		with open('config.json', 'r') as contest:
			psswd = json.load(contest) 

		# loop to traverse every problem 
		for i in range(data["No_of_Problems"]):
			try:
				with open('Problems/Problem_'+str(i+1)+'.pdf', mode ='rb') as problem:
					reader = PyPDF2.PdfFileReader(problem)
				# command to decrypt problem 
				command = ("cp " + "Problems/Problem_"+str(i+1)+".pdf temp.pdf; qpdf --password=" + psswd["Problem Key"] + " --decrypt temp.pdf Problems/Problem_" + str(i+1) + ".pdf; rm temp.pdf")
				os.system(command)
			except Exception as Error:
				print(str(Error))