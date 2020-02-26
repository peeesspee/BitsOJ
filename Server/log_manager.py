# This process handles logs
import datetime, time, sys

class handle_logs():
	def init_logs(data_changed_flags, log_queue):
		print('  [ START ] Log subprocess started.')
		handle_logs.data_changed_flags = data_changed_flags
		handle_logs.log_queue = log_queue

		file = open("./Reports/server_logs.txt", "a+")
		file2 = open("./Reports/latest_server_logs.txt", "w+")
		
		# Infinite Loop to Poll the log_queue every second
		while True:
			status = handle_logs.poll(file, file2, log_queue)
			if status == 1:
				break
			# Poll every half second
			time.sleep(0.5)

		file.close()
		file2.close()
		# Signal to MAIN for exit
		data_changed_flags[23] = 0
		sys.exit(0)

	def poll(file, file2, log_queue):
		# While there is data to process in the task_queue,
		try:
			while handle_logs.log_queue.empty() == False:
				# Data in the task queue is in JSON format
				data = handle_logs.log_queue.get()
				handle_logs.log(file, file2, data)
			return
		except Exception as error:
			print('[ ERROR ] Log error : ' + str(error)) 
		finally:
			# If sys exit is called, the following flag will be 1
			return handle_logs.data_changed_flags[23] 

	def log(file, file2, data):
		current_date_time = datetime.datetime.now()
		# print(current_date_time, '  :  ', data," ###\n") 
		write_data = str(current_date_time) + '  :  ' + str(data) + " ###\n"
		file.write(write_data)
		file2.write(write_data)
		return