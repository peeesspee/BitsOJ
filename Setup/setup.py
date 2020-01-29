from startup import init_setup
from interface import main_window
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys

def main():
	config = init_setup.read_config()

	app = QApplication(sys.argv)
	app.setAttribute(Qt.AA_EnableHighDpiScaling)
	wizard = main_window(config)
	wizard.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()