#!/usr/bin/env python3

import api as fpl_api
from PyQt5 import QtWidgets, QtCore, QtGui

def main():
	print("main()")

	api = fpl_api.FPL_API()

	window = FixtureWindow(api)

	window.show()

class FixtureWindow():
	def __init__(self, api, nextGWcount=20):
		self._api = api
		self._current_gw = api.current_gw
		
		self._nextGWcount = nextGWcount
		self._winWidth = 800
		self._winHeight = 600
		self._textSizeGlobal = 15
		self._textSizeFixs = 13
		self._rowHeightGlobal = 17

		self.app = QtWidgets.QApplication([])
		self.window = QtWidgets.QWidget()
		self.layout = QtWidgets.QVBoxLayout()

		self.window.setWindowTitle("Max's FPL Planner")
		self.app.setFont(QtGui.QFont('Courier', self._textSizeGlobal))

		self.layout.addLayout(self.make_layout())

		self.window.setLayout(self.layout)

	def make_layout(self):

		layout = QtWidgets.QGridLayout()

		self.create_headers(layout,row_index=0)

		for i,team in enumerate(self._api.teams):

			self.create_team_row(layout,team,1+i,attacker=False)
		
		self.create_headers(layout,row_index=21)

		for i,team in enumerate(self._api.teams):

			self.create_team_row(layout,team,22+i,attacker=True)
		
		return layout

	def create_team_row(self,layout,team,row_index,attacker):
		widget = QtWidgets.QLabel(" "+team.name.ljust(15))
		self.recolor_by_team(widget,team)
		layout.addWidget(widget,row_index,0,alignment=QtCore.Qt.AlignHCenter)

		for i in range(self._nextGWcount):

			gw = self._current_gw+i+1

			widget = QtWidgets.QLabel(" "+team.get_fixture_str(gw)+" ")

			difficulty = team.get_fixture_diff(gw,attacker=attacker)
			self.adjust_colour_by_diff(widget,difficulty,old=False)

			widget.setFont(QtGui.QFont('Courier', self._textSizeFixs))

			layout.addWidget(widget,row_index,1+i,alignment=QtCore.Qt.AlignHCenter)

	def create_headers(self,layout,row_index=0):
		layout.addWidget(QtWidgets.QLabel("Team"),row_index,0,alignment=QtCore.Qt.AlignHCenter)

		for i in range(self._nextGWcount):
			layout.addWidget(QtWidgets.QLabel("GW"+str(self._current_gw+i+1)),row_index,1+i,alignment=QtCore.Qt.AlignHCenter)

	def recolor_by_team(self,widget,team):

		style = team._style

		if style is None:
			return

		widget.setStyleSheet(f"background-color: {style['background-color']}; color: {style['color']}")

	def adjust_colour_by_diff(self,widget,difficulty,old=False):

		if old:
			if difficulty == 5:
				widget.setStyleSheet("background-color: darkred;""color: white")
			elif difficulty == 4:
				widget.setStyleSheet("background-color: red")
			elif difficulty == 2:
				widget.setStyleSheet("background-color: lightgreen")
			elif difficulty == 1:
				widget.setStyleSheet("background-color: darkgreen;""color: white")
			return

		else:

			# ranges from -4 to +4

			if not isinstance(difficulty,float):
				widget.setStyleSheet("background-color: black;""color: white")
				return

			if abs(difficulty) < 1.0:
				return
			elif difficulty > 0.0:
				if difficulty < 2.0:
					widget.setStyleSheet("background-color: lightgreen")
				else:
					widget.setStyleSheet("background-color: darkgreen;""color: white")
			elif difficulty < 0.0:
				if difficulty > -2.0:
					widget.setStyleSheet("background-color: red")
				else:
					widget.setStyleSheet("background-color: darkred;""color: white")

	def show(self):
		self.window.show()
		self.app.exec()

def widget_row():
	pass

if __name__ == '__main__':
	main()
