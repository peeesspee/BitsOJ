import json
from verdict import verdict
from file_creation import file_manager
from communicate_server import *
from init_judge import *

class server():

	data = {
	"Code": "JUDGE", 
	"Client ID": "999", 
	"Client Username": "team99999", 
	"Run ID": 999, 
	"Language": "JAVA", 
	"PCode": "TFG", 
	"Source": "#include<iostream>\n int main(void){ std::cout<<\"Hello\"; return 0; }",
	"Local Run ID": 12,
	"Time Stamp": '00:00'
	 }

	def makejson():
		code = server.read()
		server.data["Source"] = code
		x = json.dumps(server.data)
		# print(x)
		return x

	def perform(server_data):
		
		message = json.loads(server_data)

		run_id = str(message["Run ID"])
		problem_code = message["PCode"]
		language = message["Language"]
		source_code = message["Source"]
		client_id = message["Client ID"]
		client_username = message["Client Username"]
		local_run_id = message["Local Run ID"]
		time_stamp = message['Time Stamp']

		# print(run_id ,problem_code,language ,source_code ,client_id ,client_username ,local_run_id,time_stamp )
		
		file_name,file_with_ext = communicate_server.make_submission_file(run_id, problem_code, language, source_code)
		# main(file_name, file_with_ext, lang, problem_code, run_id, timelimit):
		print(file_name, file_with_ext, language, problem_code, run_id)
		result,error = verdict.main(file_name, file_with_ext, language, problem_code, run_id, '1')

		print("\n\n\n")
		print(result)
		print(error)

		try:
			if language == "JAVA":
				os.remove('bitsoj.java')
		except Exception as error:
			print("[JAVA FILE DELETION ERROR] :",error)

	def read():
		with open("./submission_files/java/temporary", "r") as f:
			read = f.read()
			return read

if __name__ == '__main__':
	initialize_judge.read_config()
	x = server.makejson()
	server.perform(x)
	