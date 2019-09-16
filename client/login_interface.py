import sys
from PyQt5.QtWidgets import * 
from login import authenticate_login
from PyQt5.QtCore import Qt

class Login(QWidget):
	# channel = None
	# host = None
	def __init__(self, connection):
		super().__init__()
		self.setWindowTitle('BitsOJ v1.0.1 [ LOGIN ]')
		self.resize(700, 600)

		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

		self.title = QLabel('<<BitsOJ>>')
		self.title.setFixedWidth(400)
		self.title.setFixedHeight(150)
		
		self.username = QLineEdit(self)
		self.username.setFixedWidth(400)
		self.username.setFixedHeight(50)
		self.username.setPlaceholderText('Username')

		self.password = QLineEdit(self)
		self.password.setFixedWidth(400)
		self.password.setFixedHeight(50)
		self.password.setPlaceholderText('Password')
		self.password.setEchoMode(QLineEdit.Password)

		self.button_login = QPushButton('Login', self)
		self.button_login.setFixedWidth(300)
		self.button_login.setFixedHeight(80)
		self.button_login.clicked.connect(self.handle_login)
		self.button_login.setDefault(True)

		layout = QVBoxLayout(self)

		layout.addWidget(self.title)
		layout.addWidget(self.username)
		layout.addWidget(self.password)
		layout.addWidget(self.button_login)

		
		layout.setContentsMargins(150, 0, 0, 50)

		self.setLayout(layout)
		self.setObjectName('main')
		self.show()
		return

	
	def handle_login(self):
		if (self.username.text() != '' and self.password.text() != ''):
			a = authenticate_login.login(self.username.text(),self.password.text())
			# Call client window here
			print("[ SUCCESS ] ")
			if(a):
				try:
					QApplication.quit()
				except Exception as error:
					print('[ ERROR ] Could not exit properly : ' + str(error) )
			else:
				QMessageBox.warning(self, 'Error', 'Wrong credentials')
		elif (self.username.text() == ''):
			QMessageBox.warning(self, 'Error', 'Username cannot be empty')
		elif (self.password.text() == ''):
			QMessageBox.warning(self, 'Error', 'Password cannot be empty')
		else:
			QMessageBox.warning(self, 'Error', 'Wrong credentials')

	def closeEvent(self, event):
		# If user clicks on close button on login form, exit the whole application
		self.connection_object.close()
		sys.exit()
	

class start_interface(Login):
	def __init__(self, connection):
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('Elements/login.qss', "r").read())
		app.aboutToQuit.connect(self.closeEvent)
		# make a reference of App class
		login_app = Login(connection)
		
		# Close the server as soon as close button is clicked
		app.exec_()

	