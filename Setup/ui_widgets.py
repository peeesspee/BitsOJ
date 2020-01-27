from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, pyqtProperty

class wizard_page(QWizardPage):
	def __init__(self, config, page_id = 1, parent=None):
		super(wizard_page, self).__init__(parent)
		self.config = config

		self.top_bar = QWidget()
		self.top_bar_layout = QHBoxLayout(self.top_bar)
		self.logo = QLabel()
		self.logo.setPixmap(QPixmap('Elements/bitwise_header.png').scaledToWidth(104))
		self.top_bar_layout.addWidget(self.logo)
		
		# Based on page_id, return the corresponding widget
		if page_id == 1:
			self.main_widget = self.home()
		elif page_id == 2:
			self.main_widget = self.rabbitmq_page()

		self.top_layout = QVBoxLayout()
		self.top_layout.addWidget(self.top_bar)
		self.top_layout.addWidget(self.main_widget)
		self.top_layout.setStretch(0, 10)
		self.top_layout.setStretch(1, 90)
		self.setLayout(self.top_layout)

	def get_horizontal_widget(self, widget_1, widget_2):
		layout = QHBoxLayout()
		layout.addWidget(widget_1)
		layout.addWidget(widget_2)
		layout.addStretch(1)
		widget = QWidget()
		widget.setLayout(layout)
		return widget

	def home(self):
		self.title_label = QLabel('Home')
		self.title_label.setObjectName('main_screen_heading')
		self.welcome_label = QLabel('Welcome to BitsOJ!')
		self.welcome_label.setObjectName('main_screen_sub_heading')
		message = (
			"This utility will help you to generate configuration " +
			"files for the Client, Server, and the Judge, absolutely hassle free.\n" +
			"Many of the details will remain same if you are using the same setup to host " +
			"multiple contests ( Recommended! ).\nAll the Best for your contest, and many more to come!\n" + 
			" \t\t\t\t\t\t\t\t\t- Team Bitwise @ JUET, Guna"
		)
		self.message_label = QLabel(message)
		self.message_label.setObjectName('main_screen_content')
		self.bottom_label = QLabel(
			"BitsOJ is an Open Source project, and we would love to have your contributions!"
		)
		self.bottom_label.setObjectName('main_screen_content')
		self.contribute_label = QLabel("Contribute here: ")
		self.contribute_label.setObjectName('main_screen_sub_heading2')
		self.contribute_content = QLabel(
			"<a href='https://github.com/peeesspee/BitsOJ' style = 'color: #23B2EE'>github.com/peeesspee/BitsOJ</a>"
		)
		self.contribute_content.setObjectName('main_screen_content')
		self.contribute_content.setToolTip(
			'Opens github repository link in web browser.'
		)
		self.contribute_content.setTextInteractionFlags(Qt.TextBrowserInteraction)
		self.contribute_content.setOpenExternalLinks(True)
		self.contribute_widget = self.get_horizontal_widget(self.contribute_label, self.contribute_content)
		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.welcome_label)
		self.main_layout.addWidget(self.message_label)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.bottom_label)
		self.main_layout.addWidget(self.contribute_widget)
		return self.main_widget

	def rabbitmq_page(self):
		self.title_label = QLabel('RabbitMQ Connections')
		self.title_label.setObjectName('main_screen_heading')

		self.message_rabbitmq = QLabel('Fill in the account details of Server, Client and Judge, which were created in the RabbitMQ Management Portal: ')
		self.message_rabbitmq.setObjectName('main_screen_content')

		self.server_label = QLabel('Server')
		self.server_label.setObjectName('main_screen_sub_heading')
		self.server_username_label = QLabel('Username: ')
		self.server_username_label.setObjectName('main_screen_content')
		self.server_username_entry = QLineEdit()
		self.server_username_entry.setToolTip('RabbitMQ Server account username')
		self.server_username_entry.setPlaceholderText('Example: BitsOJ')
		self.server_username_entry.setText(self.config.get("Server Username", ""))
		self.server_username_widget = self.get_horizontal_widget(
			self.server_username_label,
			self.server_username_entry
		)
		self.server_password_label = QLabel('Password:  ')
		self.server_password_label.setObjectName('main_screen_content')
		self.server_password_entry = QLineEdit()
		self.server_password_entry.setEchoMode(QLineEdit.Password)
		self.server_password_entry.setToolTip('RabbitMQ Server account password')
		self.server_password_entry.setText(self.config.get("Server Password", ""))
		self.server_password_widget = self.get_horizontal_widget(
			self.server_password_label,
			self.server_password_entry
		)
		self.server_creds_widget = self.get_horizontal_widget(
			self.server_username_widget,
			self.server_password_widget
		)

		self.client_label = QLabel('Client')
		self.client_label.setObjectName('main_screen_sub_heading')
		self.client_username_label = QLabel('Username: ')
		self.client_username_label.setObjectName('main_screen_content')
		self.client_username_entry = QLineEdit()
		self.client_username_entry.setToolTip('RabbitMQ Client account username')
		self.client_username_entry.setPlaceholderText('Example: Client')
		self.client_username_entry.setText(self.config.get("Client Username", ""))
		self.client_username_widget = self.get_horizontal_widget(
			self.client_username_label,
			self.client_username_entry
		)
		self.client_password_label = QLabel('Password:  ')
		self.client_password_label.setObjectName('main_screen_content')
		self.client_password_entry = QLineEdit()
		self.client_password_entry.setEchoMode(QLineEdit.Password)
		self.client_password_entry.setToolTip('RabbitMQ Client account password')
		self.client_password_entry.setText(self.config.get("Client Password", ""))
		self.client_password_widget = self.get_horizontal_widget(
			self.client_password_label,
			self.client_password_entry
		)
		self.client_creds_widget = self.get_horizontal_widget(
			self.client_username_widget,
			self.client_password_widget
		)

		self.judge_label = QLabel('Judge')
		self.judge_label.setObjectName('main_screen_sub_heading')
		self.judge_username_label = QLabel('Username: ')
		self.judge_username_label.setObjectName('main_screen_content')
		self.judge_username_entry = QLineEdit()
		self.judge_username_entry.setToolTip('RabbitMQ Judge account username')
		self.judge_username_entry.setPlaceholderText('Example: Client')
		self.judge_username_entry.setText(self.config.get("Judge Username", ""))
		self.judge_username_widget = self.get_horizontal_widget(
			self.judge_username_label,
			self.judge_username_entry
		)
		self.judge_password_label = QLabel('Password:  ')
		self.judge_password_label.setObjectName('main_screen_content')
		self.judge_password_entry = QLineEdit()
		self.judge_password_entry.setEchoMode(QLineEdit.Password)
		self.judge_password_entry.setToolTip('RabbitMQ Judge account password')
		self.judge_password_entry.setText(self.config.get("Judge Password", ""))
		self.judge_password_widget = self.get_horizontal_widget(
			self.judge_password_label,
			self.judge_password_entry
		)
		self.judge_creds_widget = self.get_horizontal_widget(
			self.judge_username_widget,
			self.judge_password_widget
		)

		self.main_widget = QWidget()
		self.main_widget.setObjectName('content_box')
		self.main_layout = QVBoxLayout(self.main_widget)
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.message_rabbitmq)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.server_label)
		self.main_layout.addWidget(self.server_creds_widget)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.client_label)
		self.main_layout.addWidget(self.client_creds_widget)
		self.main_layout.addStretch(1)
		self.main_layout.addWidget(self.judge_label)
		self.main_layout.addWidget(self.judge_creds_widget)
		self.main_layout.addStretch(1)
		return self.main_widget



