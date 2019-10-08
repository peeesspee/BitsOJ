# import time
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
# from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
# from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
# from interface_packages.ui_classes import *
# from init_server import initialize_server

from  database import manage_database

# import sqlite3
# conn = sqlite3.connect(":memory:")
# print((conn))	
# c = conn.cursor()
# print(c)

a="132"
b="BDSM"
c="PYTHON2"
d="AC"

manage_database.initialize_database()
# manage_database.insert_record(a, b, c, d)
# x = manage_database.get_record()
print(x)
manage_database.reset_database()

manage_database.close_db()
