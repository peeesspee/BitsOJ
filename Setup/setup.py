from startup import init_setup
from interface import main_window
from PyQt5.QtWidgets import *
import sys

def main():
	config = init_setup.read_config()

	app = QApplication(sys.argv)
	wizard = main_window(config)
	wizard.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()