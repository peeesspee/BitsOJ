# Special thanks to www.pythonspot.com for this!
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, pyqtProperty
from ui_widgets import *

class main_window(QWizard):
	def __init__(self, config, parent=None):
		super(main_window, self).__init__(parent)
		self.setStyleSheet(open('Elements/style.qss', "r").read())
		self.config = config
		self.home_page = wizard_page(config, 1)
		self.rabbitmq_page = wizard_page(config, 2)

		self.addPage(self.home_page)
		self.addPage(self.rabbitmq_page)
		
		self.setWindowTitle("BitsOJ v1.1 [ CONTEST SETUP ]")
		self.setFixedSize(1366, 768)
