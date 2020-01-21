import sys
from PyQt5.QtWidgets import * 
from login import authenticate_login
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QPixmap

class Login(QWidget):
	def __init__(self, queue):
		super().__init__()
		try:
			# Sets window title
			self.setWindowTitle('BitsOJ v1.0.1 [ LOGIN ]')
			# Resize Size of the window 
			self.resize(700, 600)
			# Window Icon
			self.setWindowIcon(QIcon("Elements\\logo.png"))

			# Frame Geometry
			qtRectangle = self.frameGeometry()
			centerPoint = QDesktopWidget().availableGeometry().center()
			qtRectangle.moveCenter(centerPoint)
			self.move(qtRectangle.topLeft())

			# Title of the login window
			self.title = QLabel('<<BitsOJ>>')
			self.title.setObjectName('label')
			self.title.setFixedWidth(400)
			self.title.setFixedHeight(150)
			
			# Text Box for taking username input
			self.username = QLineEdit(self)
			self.username.setFixedWidth(400)
			self.username.setFixedHeight(50)
			self.username.setPlaceholderText('Username')

			# Text Box for taking password input
			self.password = QLineEdit(self)
			self.password.setFixedWidth(400)
			self.password.setFixedHeight(50)
			self.password.setPlaceholderText('Password')
			self.password.setEchoMode(QLineEdit.Password)

			# Creating Login button for sending authenticaion request to the Server
			self.button_login = QPushButton('Login', self)
			self.button_login.setFixedWidth(300)
			self.button_login.setFixedHeight(80)
			self.button_login.clicked.connect(lambda:self.handle_login(queue))
			self.button_login.setDefault(True)
			self.button_login.setObjectName('login')

			# Creating a layout for adding the widgets
			layout = QVBoxLayout(self)

			# Adding the widgets in the layout
			layout.addWidget(self.title)
			layout.addWidget(self.username)
			layout.addWidget(self.password)
			layout.addWidget(self.button_login)

			
			layout.setContentsMargins(150, 0, 0, 50)

			self.setLayout(layout)
			self.setObjectName('main') 
			# self.show()
			# self.connection_object = connection 
		except Exception as Error:
			print(str(Error))
		return 

	# Function for handling the login of the user  
	def handle_login(self,queue):
		# QApplication.quit()
		# Username and Password are not empty the check credentials
		if (self.username.text() != '' and self.password.text() != ''):

			# login function to send the username and password to the server for authentication
			authenticate_login.login(self.username.text(),self.password.text(),queue)
			

			# If authentication is successful then close login window and open main window 
			if( authenticate_login.login_status == 'VALID'):
				try:
					print('[ VALID ] Login')
					QApplication.quit()
				except Exception as error:
					print('[ ERROR ] Could not exit properly : ' + str(error) )

			# If server is not accepting login request then show an alert
			elif( authenticate_login.login_status == 'LRJCT' ):
				message = queue.get()
				# QMessageBox.warning(self, 'Error', 'Login Rejected by admin.')
				QMessageBox.warning(self, 'Error', message)
			else:
				QMessageBox.warning(self, 'Error', 'Wrong credentials')

		# If username is empty then show an alert
		elif (self.username.text() == ''):
			QMessageBox.warning(self, 'Error', 'Username cannot be empty')

		# If password is empty then show an alert
		elif (self.password.text() == ''):
			QMessageBox.warning(self, 'Error', 'Password cannot be empty')
			
		# If authentication failed 
		else:
			QMessageBox.warning(self, 'Error', 'Wrong credentials')

	def closeEvent(self, event):
		# If user clicks on close button on login form, exit the whole application
		self.connection_object.close()
		sys.exit()
	

class start_interface(Login):
	def __init__(self, data_changed_flag,queue):
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open("Elements\\login.qss", "r").read())
		app.aboutToQuit.connect(self.closeEvent)
		# make a reference of App class
		# login_app = Login(connection,queue)

		splash = QSplashScreen(QPixmap("./Elements/banner.png"), Qt.WindowStaysOnTopHint)
		login_app = Login(queue)

		splash.show()
		splash.showMessage("Loading modules...")
		t = 0
		while(t < 10000):
			t += 0.01
			app.processEvents()

		splash.finish(login_app)
		login_app.show()
		
		# Close the server as soon as close button is clicked
		app.exec_()

	