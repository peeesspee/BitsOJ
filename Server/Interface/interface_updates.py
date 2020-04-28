import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler, QPoint

class interface_updates:
	def update_table_contained(self):
		while not self.update_queue.empty():
			data = self.update_queue.get()
			code = data.get('Code', 'None')
			if code == 'None':
				pass
			elif code == 'AddNewUser':
				table = data['Table']
				if table == 'connected_clients':
					row_count = self.client_model.rowCount()
					self.client_model.setRowCount(row_count + 1)
					self.client_model.setItem(row_count, 0, QTableWidgetItem(str(data['ID'])))
					self.client_model.setItem(row_count, 1, QTableWidgetItem(data['Username']))
					self.client_model.setItem(row_count, 2, QTableWidgetItem(data['Password']))
					self.client_model.setItem(row_count, 3, QTableWidgetItem(data['IP']))
					self.client_model.setItem(row_count, 4, QTableWidgetItem(data['State']))
				elif table == 'connected_judges':
					row_count = self.judge_model.rowCount()
					self.judge_model.setRowCount(row_count + 1)
					self.judge_model.setItem(row_count, 0, QTableWidgetItem(str(data['ID'])))
					self.judge_model.setItem(row_count, 1, QTableWidgetItem(data['Username']))
					self.judge_model.setItem(row_count, 2, QTableWidgetItem(data['Password']))
					self.judge_model.setItem(row_count, 3, QTableWidgetItem(data['IP']))
					self.judge_model.setItem(row_count, 4, QTableWidgetItem(data['State']))

			elif code == 'RefreshUsers':
				account_data = data['Data']
				self.account_model.setRowCount(len(account_data))
				for i in range (len(account_data)):
					for j in range(len(account_data[i])):
						self.account_model.setItem(i, j, QTableWidgetItem(account_data[i][j]))

			elif code == 'DelUsr':
				username = data['Client']
				row_count = self.account_model.rowCount()
				for i in range (row_count):
					item = self.account_model.item(i, 0).text()
					if item == username:
						self.account_model.removeRow(i)
						break

			elif code == 'UpUserPwd':
				username = data['Username']
				password = data['New Password']
				ctype = data['Type']

				row_count = self.account_model.rowCount()
				for i in range (row_count):
					item = self.account_model.item(i, 0).text()
					if item == username:
						self.account_model.setItem(i, 1, QTableWidgetItem(password))
						break

				if ctype == 'CLIENT':
					row_count = self.client_model.rowCount()
					for i in range (row_count):
						item = self.client_model.item(i, 0).text()
						if item == username:
							self.client_model.setItem(i, 2, QTableWidgetItem(password))
							break
							
				elif ctype == 'JUDGE':
					row_count = self.judge_model.rowCount()
					for i in range (row_count):
						item = self.judge_model.item(i, 0).text()
						if item == username:
							self.judge_model.setItem(i, 2, QTableWidgetItem(password))
							break

			elif code == 'AddNewSub':
				row_count = self.sub_model.rowCount()
				self.sub_model.setRowCount(row_count + 1)
				self.sub_model.setItem(row_count, 0, QTableWidgetItem(str(data['Run ID'])))
				self.sub_model.setItem(row_count, 1, QTableWidgetItem(str(data['Client ID'])))
				self.sub_model.setItem(row_count, 2, QTableWidgetItem(data['Problem Code']))
				self.sub_model.setItem(row_count, 3, QTableWidgetItem(data['Language']))
				self.sub_model.setItem(row_count, 4, QTableWidgetItem(data['Time']))
				self.sub_model.setItem(row_count, 5, QTableWidgetItem(data['Verdict']))
				self.sub_model.setItem(row_count, 6, QTableWidgetItem(data['Status']))
				self.sub_model.setItem(row_count, 7, QTableWidgetItem(data['Judge']))

			elif code == 'UpSubStat':
				run_id  = int(data['Run ID'])
				verdict = data['Verdict']
				sent_status = data['Status']
				judge = data['Judge']
				
				row_count = self.sub_model.rowCount()
				for i in range(row_count):
					item = int(self.sub_model.item(i, 0).text())
					if item == run_id:
						self.sub_model.setItem(i, 5, QTableWidgetItem(verdict))
						self.sub_model.setItem(i, 6, QTableWidgetItem(sent_status))
						self.sub_model.setItem(i, 7, QTableWidgetItem(judge))
						break

			elif code == 'UpSCBD':
				scbd_data = data['Data']
				username = scbd_data[0]
				score = str(scbd_data[1])
				problems_solved = str(scbd_data[2])
				total_time = scbd_data[3]
				row_count = self.score_model.rowCount()
				for i in range(row_count):
					item = self.score_model.item(i, 0).text()
					if item == username:
						self.score_model.setItem(i, 1, QTableWidgetItem(problems_solved))
						self.score_model.setItem(i, 2, QTableWidgetItem(score))
						self.score_model.setItem(i, 3, QTableWidgetItem(total_time))
						break
				self.score_model.sortItems(2, order = Qt.DescendingOrder)
				
			elif code == 'AddNewScore':
				username = data['Username' ]
				client_id = data['ID']
				score = str(data['Score'])
				problems_solved = str(data['Problems Solved'])
				total_time = data['Total Time']				
				row_count = self.score_model.rowCount()
				self.score_model.setRowCount(row_count + 1)
				self.score_model.setItem(row_count, 0, QTableWidgetItem(username))
				self.score_model.setItem(row_count, 1, QTableWidgetItem(problems_solved))
				self.score_model.setItem(row_count, 2, QTableWidgetItem(score))
				self.score_model.setItem(row_count, 3, QTableWidgetItem(total_time))

			elif code == 'UpJudgeStat':
				username = data['Username']
				state = data['State']
				judge_ip = data['IP']
				row_count = self.judge_model.rowCount()
				for i in range(row_count):
					item = self.judge_model.item(i, 1).text()
					if item == username:
						self.judge_model.setItem(i, 3, QTableWidgetItem(judge_ip))
						self.judge_model.setItem(i, 4, QTableWidgetItem(state))
						break

			elif code == 'UpUserStat':
				username = data['Username']
				state = data['State']
				client_ip = data['IP']
				row_count = self.client_model.rowCount()
				for i in range(row_count):
					item = self.client_model.item(i, 1).text()
					if item == username:
						self.client_model.setItem(i, 3, QTableWidgetItem(client_ip))
						self.client_model.setItem(i, 4, QTableWidgetItem(state))
						break

			elif code == 'AddQuery':
				row_count = self.query_model.rowCount()
				self.query_model.setRowCount(row_count + 1)
				self.query_model.setItem(row_count, 0, QTableWidgetItem(str(data['Query ID'])))
				self.query_model.setItem(row_count, 1, QTableWidgetItem(str(data['Client ID'])))
				self.query_model.setItem(row_count, 2, QTableWidgetItem(data['Query']))
				self.query_model.setItem(row_count, 3, QTableWidgetItem(data['Response']))

			elif code == 'QUERY':
				# Handle query response
				client_id = data['Client ID']
				response = data['Response']
				row_count = self.query_model.rowCount()
				for i in range(row_count):
					item = self.query_model.item(i, 1).text()
					if int(item) == int(client_id):
						self.query_model.setItem(i, 3, QTableWidgetItem(response))
						break
			
			elif code == 'ERROR':
				message = data['Message']
				info_box = QMessageBox()
				info_box.setIcon(QMessageBox.Critical)
				info_box.setWindowTitle('Error')
				info_box.setText(message)
				info_box.setStandardButtons(QMessageBox.Ok)
				info_box.exec_()

			elif code == 'INFO':
				message = data['Message']
				info_box = QMessageBox()
				info_box.setIcon(QMessageBox.Information)
				info_box.setWindowTitle('Alert')
				info_box.setText(message)
				info_box.setStandardButtons(QMessageBox.Ok)
				info_box.exec_()

			elif code == 'JDscntAll':
				pass
