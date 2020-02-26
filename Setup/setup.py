from startup import init_setup
from interface import main_window
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, os

def create_directory(dir_name):
	try:
		os.mkdir(dir_name)
	except FileExistsError:
		print('[ PASS ] Directory ', dir_name, ' exists.')
		pass
	except Exception as error:
		print(error)
		print(
			'[ ERROR ] Could not create ' + dir_name + '\n' + 
			'[ ERROR ] The current directory requires sudo elevation to create folders.' + 
			'\nRestart Setup with sudo privileges.'
		)
		return

def main():
	# Make needed directories
	create_directory("Contest_Data")
	create_directory('Contest_Data/Server')
	create_directory('Contest_Data/Server/Problem Data')
	create_directory('Contest_Data/Client')
	create_directory('Contest_Data/Client/Problems')
	create_directory('Contest_Data/Judge')
	create_directory('Contest_Data/Judge/problems')
	create_directory('Problems')

	# Read configuration file
	config = init_setup.read_config()
	# Start main GUI
	app = QApplication(sys.argv)
	app.setStyleSheet(open('Elements/style.qss', "r").read())
	app.setAttribute(Qt.AA_EnableHighDpiScaling)

	screen = app.primaryScreen()
	rect = screen.availableGeometry()
	available_width = rect.width()
	available_height = rect.height()
	key = 'haSCgWdWjF13W2F1WbWshAWgC7W3C1W1CjWbC1dW7CgWvGR7THYYgJYyNb2Nb72gbcwh'
	wizard = main_window(
		config, 
		available_width, 
		available_height, 
		key
	)
	wizard.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
