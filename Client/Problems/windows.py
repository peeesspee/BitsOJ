import os
os.startfile(filename)



# For decrypting pdf file
import PyPDF2
try:
			with open('Problems/Problem_'+str(i)+'.pdf', mode ='rb') as problem:
				print('file opened')
				reader = PyPDF2.PdfFileReader(problem)
				print('done 1')
				if reader.isEncrypted:
					print('done 2')
					# reader.decrypt('papa')
					# print('decrypted')
					try:
						reader.decrypt('papa')
						print('file decrypted')
					except Exception as Error:
						print(str(Error))
						command = ("cp " + "Problems/Problem_"+str(i)+".pdf temp.pdf; qpdf --password='papa' --decrypt temp.pdf Problems/Problem_" + str(i) + ".pdf; rm temp.pdf")
						os.system(command)
						print('file Decrypted')
						fp = open('Problems/Problem_'+str(i)+'.pdf', 'rb')
						print('pls check')
						reader = PyPDF2.PdfFileReader(fp)
					print('finally done')
				page = reader.getPage(0)
				print(page)
				print(page.extractText())
		except Exception as Error:
			print(str(Error))