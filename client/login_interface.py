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
		self.resize(400, 300)
		#self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		self.connection_object  = connection
	
		# Widget for taking username 
		username_label = QLabel(self)
		username_label.setText('USERNAME : ')

		self.username = QLineEdit(self)
		self.username.setFixedWidth(100)

		
		password_label = QLabel(self)
		password_label.setText('PASWORD : ')

		self.password = QLineEdit(self)
		self.password.setFixedWidth(100)


		self.button_login = QPushButton('Login', self)
		self.button_login.setFixedWidth(200)
		self.button_login.clicked.connect(self.handle_login)

		layout = QFormLayout(self)
		layout.addRow(username_label, self.username)
		layout.addRow(password_label, self.password)
		layout.addRow(self.button_login)
		layout.setContentsMargins(100, 50, 100, 50)
		self.setLayout(layout)
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
		app.setStyleSheet(open('Elements/style.qss', "r").read())
		app.aboutToQuit.connect(self.closeEvent)
		# Login.channel = channel
		# Login.host = host
		# make a reference of App class
		login_app = Login(connection)
		
		# Close the server as soon as close button is clicked
		app.exec_()

	