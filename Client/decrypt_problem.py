import os
import PyPDF2
import json



class decrypt():

	def decrypting():
		with open('config.json', 'r') as read_file:
			data = json.load(read_file)
		with open('contest.json', 'r') as contest:
			psswd = json.load(contest)
		for i in range(data["No_of_Problems"]):
			try:
				with open('Problems/Problem_'+str(i+1)+'.pdf', mode ='rb') as problem:
					reader = PyPDF2.PdfFileReader(problem)
				command = ("cp " + "Problems/Problem_"+str(i+1)+".pdf temp.pdf; qpdf --password=" + psswd["Problem Key"] + " --decrypt temp.pdf Problems/Problem_" + str(i+1) + ".pdf; rm temp.pdf")
				os.system(command)
			except Exception as Error:
				print(str(Error))