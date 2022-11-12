
# from Pyside2 import QtGui
# from Pyside2 import QtWidgets
# from Pyside2 import QtCore

from PyQt5 import QtWidgets, QtCore, QtGui

from widget import ComboWidget

import mout

# app = QApplication([])

# label = QLabel("Hello World")

# label.show()

# app.exec_()

class FPL_Window():

	_winWidth = 800
	_winHeight = 600

	_checkboxes = []
	_values = []
	_numbers = []
	_transfers = []
	_num_def = []
	_num_mid = []
	_num_fwd = []

	_players = []

	_current_gw = 0
	_gw_max = 19

	_num_head_columns = 3

	_json_file = "data.json"

	def __init__(self,players,api):
		# super(FPL_Window, self).__init__()

		self._api = api
		self._current_gw = api.current_gw

		self._players = players
		
		self.app = QtWidgets.QApplication([])
		self.window = QtWidgets.QWidget()
		self.layout = QtWidgets.QVBoxLayout()

		self.window.setWindowTitle("Max's FPL Planner")


		# self.layout.addWidget(QtWidgets.QPushButton('Top'))
		# self.layout.addWidget(QtWidgets.QPushButton('Bottom'))

		self.layout.addLayout(self.central_layout())

		self.create_connections()

		self.window.setLayout(self.layout)

		try:
			bool_array = self.get_latest_json()
			self.set_checkboxes(bool_array)
		except:
			mout.warningOut("Problem reading json file")
		
	def central_layout(self):

		sublayout = QtWidgets.QGridLayout()

		# headers
		sublayout.addWidget(QtWidgets.QLabel("Player"),0,0,alignment=QtCore.Qt.AlignHCenter)
		sublayout.addWidget(QtWidgets.QLabel("Price"),0,1,alignment=QtCore.Qt.AlignHCenter)
		sublayout.addWidget(QtWidgets.QLabel("Net Tr."),0,2,alignment=QtCore.Qt.AlignHCenter)

		for i in range(self._gw_max):
			sublayout.addWidget(QtWidgets.QLabel("GW "+str(i+1)),0,i+self._num_head_columns,alignment=QtCore.Qt.AlignHCenter)

		# player rows
		for j,player in enumerate(self._players):
			sublayout.addWidget(QtWidgets.QLabel(player.name),j+1,0)
			sublayout.addWidget(QtWidgets.QLabel("£"+str(player.price)),j+1,1,alignment=QtCore.Qt.AlignRight)
			net_widget = QtWidgets.QLabel(player.net_transfers)
			if net_widget.text().startswith("-"):
				net_widget.setStyleSheet("color: red")
			else:
				net_widget.setStyleSheet("color: green")
			sublayout.addWidget(net_widget,j+1,2,alignment=QtCore.Qt.AlignRight)

			# sublayout.addWidget(QtWidgets.QLabel(player.name+", £"+str(player.price)+" "+player.team),j+1,0)

		for j,player in enumerate(self._players):
			checkbox_row = []

			for i in range(self._gw_max):

				if i < self._current_gw:

					score = player.get_event_score(i+1)

					combowidget = ComboWidget(text=str(score).rjust(2),
											  isChecked=False,
											  showCheckbox=False)
					if score < 1:
						combowidget.setStyleSheet("background-color: darkred;""color: white")
					elif score == 2:
						combowidget.setStyleSheet("background-color: orange")
					elif score > 9:
						combowidget.setStyleSheet("background-color: darkgreen;""color: white")
					elif score > 5:
						combowidget.setStyleSheet("background-color: lightgreen")
					elif score > 2:
						combowidget.setStyleSheet("background-color: yellow")
					elif score > 0:
						combowidget.setStyleSheet("background-color: red")

				else:

					combowidget = ComboWidget(text=player.get_fixture_str(i+1,short=True),
											  isChecked=False,
											  showCheckbox=True)

					difficulty = player.get_fixture_diff(i+1)
					if difficulty == 5:
						combowidget.setStyleSheet("background-color: darkred;""color: white")
					elif difficulty == 4:
						combowidget.setStyleSheet("background-color: red")
					elif difficulty == 2:
						combowidget.setStyleSheet("background-color: lightgreen")
					elif difficulty == 1:
						combowidget.setStyleSheet("background-color: darkgreen;""color: white")

				combowidget.setFont(QtGui.QFont('Courier', 12))
				combowidget.init_widget()
				checkbox_row.append(combowidget)

			self._checkboxes.append(checkbox_row)

		for j,checkbox_row in enumerate(self._checkboxes):
			for i,checkbox in enumerate(checkbox_row):
				sublayout.addWidget(checkbox.widget,j+1,i+self._num_head_columns,alignment=QtCore.Qt.AlignLeft)

		sublayout.addWidget(QtWidgets.QLabel("Value"),   len(self._players)+1,0,alignment=QtCore.Qt.AlignHCenter)
		sublayout.addWidget(QtWidgets.QLabel("Players"), len(self._players)+2,0,alignment=QtCore.Qt.AlignHCenter)
		sublayout.addWidget(QtWidgets.QLabel("Transfer"),len(self._players)+3,0,alignment=QtCore.Qt.AlignHCenter)
		sublayout.addWidget(QtWidgets.QLabel("# defs"),len(self._players)+4,0,alignment=QtCore.Qt.AlignHCenter)
		sublayout.addWidget(QtWidgets.QLabel("# mids"),len(self._players)+5,0,alignment=QtCore.Qt.AlignHCenter)
		sublayout.addWidget(QtWidgets.QLabel("# fwds"),len(self._players)+6,0,alignment=QtCore.Qt.AlignHCenter)

		sum_lists = [self._values,self._numbers,self._transfers,self._num_def,self._num_mid,self._num_fwd]

		for i in range(self._gw_max):

			for j,this_list in enumerate(sum_lists):
				widget = QtWidgets.QLabel("")
				this_list.append(widget)
				sublayout.addWidget(widget,len(self._players)+1+j,i+self._num_head_columns,alignment=QtCore.Qt.AlignHCenter)

		self.refresh_totals()

		return sublayout

	def create_connections(self):

		# connect the checkboxes
		for checkbox_row in self._checkboxes:
			for i,checkbox in enumerate(checkbox_row):
				if i > self._current_gw:
					checkbox.widget.stateChanged.connect(self.checkbox_changed)

	def get_latest_json(self):

		print("get_latest_json()")

		import json

		file = open(self._json_file, "r")
		bool_array = json.loads(file.read())
		file.close()

		return bool_array

	def write_json(self,bool_array):

		import json

		file = open(self._json_file,"w")
		file.write(json.dumps(bool_array,indent=True))
		file.close()

	def checkbox_changed(self):

		bool_array = []

		for i,checkbox_row in enumerate(self._checkboxes):
			this_row = []
			for checkbox in checkbox_row:
				this_row.append(checkbox.isChecked())
			bool_array.append(this_row)

		self.write_json(bool_array)
		self.refresh_totals()

	def refresh_totals(self):

		for i in range(self._gw_max):

			# if i > self._current_gw:

			squad_value = 0
			for j,player in enumerate(self._players):
				if self._checkboxes[j][i].isChecked():
					if i >= self._current_gw:
						squad_value += player.price
					else:
						squad_value += player.get_event_score(i+1)
			if i >= self._current_gw:
				# self._values[i].setText(str(squad_value))
				self._values[i].setText(str(f"{squad_value:.1f}"))
			else:
				self._values[i].setText(str(int(squad_value)))

			numbers = 0
			for j,player in enumerate(self._players):
				if self._checkboxes[j][i].isChecked():
					numbers += 1
			self._numbers[i].setText(str(numbers))

			if i > 0:
				transfers = 0
				for j,player in enumerate(self._players):
					if self._checkboxes[j][i].isChecked() != self._checkboxes[j][i-1].isChecked():
						transfers += 1
				self._transfers[i].setText(str(transfers))
			else:
				self._transfers[i].setText(str(0))

			defs = 0
			for j,player in enumerate(self._players):
				if self._checkboxes[j][i].isChecked() and player.position_id == 2:
					defs += 1
			self._num_def[i].setText(str(defs))

			mids = 0
			for j,player in enumerate(self._players):
				if self._checkboxes[j][i].isChecked() and player.position_id == 3:
					mids += 1
			self._num_mid[i].setText(str(mids))

			fwds = 0
			for j,player in enumerate(self._players):
				if self._checkboxes[j][i].isChecked() and player.position_id == 4:
					fwds += 1
			self._num_fwd[i].setText(str(fwds))

	def set_checkboxes(self,bool_array=None,first_15_true=False):

		if first_15_true:
			for i,checkbox_row in enumerate(self._checkboxes):
				if not i < 15:
					return
				for checkbox in checkbox_row:
					checkbox.setCheckState(QtCore.Qt.CheckState(2))
		else:
			for j,checkbox_row in enumerate(self._checkboxes):
				for i,checkbox in enumerate(checkbox_row):

					# if i > self._current_gw:

					try:
						if bool_array[j][i]:
							checkbox.setCheckState(QtCore.Qt.CheckState(2))
						else:
							checkbox.setCheckState(QtCore.Qt.CheckState(0))
					except:
						checkbox.setCheckState(QtCore.Qt.CheckState(0))

	def show(self):
		self.window.show()
		self.app.exec()
