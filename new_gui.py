#!/usr/bin/env python

from player import Player
from squad import Squad
from manager import Manager

import api as fpl_api

old_diff = False
overall_diff = False

from PyQt5 import QtWidgets, QtCore, QtGui

'''

	To-Do's

		+ blank GW fixture should be black
		+ highlight GW number for specials: DGW, blank, etc.
		+ add selected %
		+ add injury/flag to player name
		- Chip availability
		
		+ Differentiate between did not play, too early and no fixture
		- Current game score in tooltip
		+ difficulty in future gw tooltip
		- Future fixture tooltips
		+ deal with double game week support
		
		+ Add total squad value and buying power (sum[selling prices])
		+ checkbox to select transfers in watchlist

'''


# from gui import FPL_Window

# import plot

def main():

	print("main()")

	api = fpl_api.FPL_API()

	watchlist = [
				# "Callum Wilson",
				# "Dasilva",
				# "Malacia",
				# "Botman",
				# "Barnes",
				# "Darwin",
				"Trippier",
				"Zinchenko",
				"Reece",
				"Kyle Walker",
				"Luis D",
				"Haaland",
				"Kane",
				"Mount",
				"Ederson",
				"Lloris",
				"Alisson",
				"Pedro Neto",
				"Rashford",
				]

	manager = Manager("Max",780664,api,authenticate=True)

	manager.get_current_squad()

	window = NewFPL_Window(manager,api,watchlist=watchlist)
	window.show()

	# squad = Squad()

	# for player in players:
	# 	player = Player(player,api)
	# 	# print(player)
	# 	squad.add_player(player)

	# league = []

	# for manager in managers:
	# 	league.append(Manager(manager['name'],manager['id'],api))

class NewFPL_Window():

	def __init__(self,manager,api,watchlist=None):

		## prefs

		self._prevGWcount = 5
		self._nextGWcount = 10
		self._winWidth = 800
		self._winHeight = 600
		self._textSizeGlobal = 15
		self._textSizeScores = 13
		self._textSizeFixs = 13
		self._rowHeightGlobal = 17

		##

		self._api = api
		self._current_gw = api.current_gw

		self._manager = manager

		self._watchlist = watchlist
		if self._watchlist:
			squad = Squad()
			for name in self._watchlist:
				squad.add_player(Player(name,api))
			self._watchlist = squad

		self.app = QtWidgets.QApplication([])
		self.window = QtWidgets.QWidget()
		self.layout = QtWidgets.QVBoxLayout()

		self.window.setWindowTitle("Max's FPL Planner")
		self.app.setFont(QtGui.QFont('Courier', self._textSizeGlobal))

		self.layout.addLayout(self.current_squad_layout())

		# self.create_connections()

		self.window.setLayout(self.layout)

	def current_squad_layout(self):

		layout = QtWidgets.QGridLayout()

		if self._current_gw < self._prevGWcount:
			self._prevGWcount = self._current_gw

		# create the header widgets
		self.create_headers(layout,row_index=0)

		for i,player in enumerate(self._manager.squad.sorted_players):
			self.add_player_row(layout,i+1,player)
		
		layout.addWidget(QtWidgets.QLabel(""),16,1,alignment=QtCore.Qt.AlignHCenter)

		layout.addWidget(QtWidgets.QLabel("Squad"),17,1,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Bank"),17,2,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Liquid"),17,3,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("#T Free"),17,5,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("#T Made"),17,7,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Chips"),17,9,alignment=QtCore.Qt.AlignHCenter)

		layout.addWidget(QtWidgets.QLabel(str(self._manager._squad_value[-1])),18,1,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel(str(self._manager._bank_balance[-1])),18,2,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel(str(self._manager.purchase_power)),18,3,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel(str(self._manager._transfers_available)),18,5,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel(str(self._manager._transfers_made)),18,7,alignment=QtCore.Qt.AlignHCenter)
		
		layout.addWidget(QtWidgets.QLabel(""),19,1,alignment=QtCore.Qt.AlignHCenter)

		if self._watchlist:

			self.create_headers(layout,row_index=20)

			for i,player in enumerate(self._watchlist.sorted_players):
				self.add_player_row(layout,i+21,player)

		return layout

	def add_player_row(self,layout,row_index,player):

		layout.addWidget(QtWidgets.QLabel(["GK","DEF","MID","FWD"][player.position_id-1]),row_index,0,alignment=QtCore.Qt.AlignHCenter)
		
		widget = QtWidgets.QLabel(" "+player.shortteam.ljust(14))
		self.recolor_by_team(widget,player.team_obj)
		layout.addWidget(widget,row_index,1,alignment=QtCore.Qt.AlignHCenter)

		layout.addWidget(QtWidgets.QLabel(player.name),row_index,2,alignment=QtCore.Qt.AlignLeft)
		
		pp = player.purchase_price
		sp = player.selling_price

		widget = QtWidgets.QLabel(str(pp))
		layout.addWidget(widget,row_index,3,alignment=QtCore.Qt.AlignHCenter)

		widget = QtWidgets.QLabel(str(sp))
		if isinstance(sp,float):
			if sp > pp:
				widget.setStyleSheet("color: green")
			elif sp < pp:
				widget.setStyleSheet("color: red")
		layout.addWidget(widget,row_index,4,alignment=QtCore.Qt.AlignHCenter)
		
		widget = QtWidgets.QLabel(str(player.price))
		if isinstance(sp,float):
			if pp < player.price:
				widget.setStyleSheet("color: green")
			elif pp > player.price:
				widget.setStyleSheet("color: red")
		layout.addWidget(widget,row_index,5,alignment=QtCore.Qt.AlignHCenter)

		layout.addWidget(QtWidgets.QLabel(str(player.total_points)),row_index,6,alignment=QtCore.Qt.AlignHCenter)
		
		widget = QtWidgets.QLabel(str(player.net_transfers))
		widget.setFixedHeight(self._rowHeightGlobal)
		if widget.text().startswith("-"):
			widget.setStyleSheet("color: red")
		else:
			widget.setStyleSheet("color: green")
		layout.addWidget(widget,row_index,7,alignment=QtCore.Qt.AlignHCenter)

		# previous and current weeks
		for i in range(self._prevGWcount):
			last = self._prevGWcount == i+1

			gw = self._current_gw-self._prevGWcount+i+1

			if player.num_gwfix(gw) > 1:
				print("XXX")
				print(f'{player} has {player.num_gwfix(gw)} fixtures in GW{gw}')

			score, summary = player.get_event_score(gw,summary=True)

			if score is None:
				widget = QtWidgets.QLabel(" -- ")
			else:
				widget = QtWidgets.QLabel(" "+str(score).rjust(2)+" ")

				if score < 1:
					widget.setStyleSheet("background-color: darkred;""color: white")
				elif score == 2:
					widget.setStyleSheet("background-color: orange")
				elif score > 9:
					widget.setStyleSheet("background-color: darkgreen;""color: white")
				elif score > 5:
					widget.setStyleSheet("background-color: lightgreen")
				elif score > 2:
					widget.setStyleSheet("background-color: yellow")
				elif score > 0:
					widget.setStyleSheet("background-color: red")
			
			widget.setToolTip(summary)

			widget.setFont(QtGui.QFont('Courier', self._textSizeScores))

			layout.addWidget(widget,row_index,8+i,alignment=QtCore.Qt.AlignHCenter)

		# form
		score = float(player.form)
		widget = QtWidgets.QLabel(" "+str(score).rjust(4)+" ")

		if score < 1:
			widget.setStyleSheet("background-color: darkred;""color: white")
		elif score == 2:
			widget.setStyleSheet("background-color: orange")
		elif score > 9:
			widget.setStyleSheet("background-color: darkgreen;""color: white")
		elif score > 5:
			widget.setStyleSheet("background-color: lightgreen")
		elif score > 2:
			widget.setStyleSheet("background-color: yellow")
		elif score > 0:
			widget.setStyleSheet("background-color: red")
		
		widget.setFont(QtGui.QFont('Courier', self._textSizeScores))

		layout.addWidget(widget,row_index,9+self._prevGWcount,alignment=QtCore.Qt.AlignHCenter)

		# future weeks
		for i in range(self._nextGWcount):

			gw = self._current_gw+i+1

			if player.num_gwfix(gw) > 1:
				print(f'{player} has {player.num_gwfix(gw)} fixtures in GW{gw}')
				
				if player.num_gwfix(gw) == 2:

					fix_strs = player.get_fixture_str(gw,short=True)
					diffs = player.get_fixture_diff(gw,old=old_diff,overall=overall_diff)

					widget1 = QtWidgets.QLabel(fix_strs[0])
					widget2 = QtWidgets.QLabel(fix_strs[1])
					
					widget1.setFont(QtGui.QFont('Courier', self._textSizeFixs))
					widget2.setFont(QtGui.QFont('Courier', self._textSizeFixs))

					self.adjust_colour_by_diff(widget1,diffs[0],old=old_diff)
					self.adjust_colour_by_diff(widget2,diffs[1],old=old_diff)

					sublayout = QtWidgets.QHBoxLayout()
					sublayout.addWidget(widget1)
					sublayout.addWidget(widget2)

					layout.addLayout(sublayout,row_index,10+self._prevGWcount+i,alignment=QtCore.Qt.AlignHCenter)

			else:
				widget = QtWidgets.QLabel(" "+player.get_fixture_str(gw,short=True)+" ")

				difficulty = player.get_fixture_diff(gw,old=old_diff,overall=overall_diff)
				self.adjust_colour_by_diff(widget,difficulty,old=old_diff)

				widget.setFont(QtGui.QFont('Courier', self._textSizeFixs))

				layout.addWidget(widget,row_index,10+self._prevGWcount+i,alignment=QtCore.Qt.AlignHCenter)
		
		diff = sum([player.get_fixture_diff(self._current_gw+i+1,old=old_diff,overall=overall_diff) for i in range(self._nextGWcount) 
				if isinstance(player.get_fixture_diff(self._current_gw+i+1,old=old_diff,overall=overall_diff),float)])/self._nextGWcount
		widget = QtWidgets.QLabel(' '+f'{diff:4.1f} ')
		self.adjust_colour_by_diff(widget,diff,old=old_diff)
		layout.addWidget(widget,row_index,11+self._prevGWcount+self._nextGWcount,alignment=QtCore.Qt.AlignHCenter)

	def create_headers(self,layout,row_index=0):

		layout.addWidget(QtWidgets.QLabel("Pos."),row_index,0,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Team"),row_index,1,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Player"),row_index,2,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Purc. £"),row_index,3,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Sell. £"),row_index,4,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Curr. £"),row_index,5,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Tot. Pts."),row_index,6,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Trans."),row_index,7,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Form"),row_index,9+self._prevGWcount,alignment=QtCore.Qt.AlignHCenter)
		layout.addWidget(QtWidgets.QLabel("Diff."),row_index,11+self._prevGWcount+self._nextGWcount,alignment=QtCore.Qt.AlignHCenter)

		for i in range(self._prevGWcount):
			layout.addWidget(QtWidgets.QLabel("GW"+str(self._current_gw-self._prevGWcount+i+1)),row_index,8+i,alignment=QtCore.Qt.AlignHCenter)

		for i in range(self._nextGWcount):
			layout.addWidget(QtWidgets.QLabel("GW"+str(self._current_gw+i+1)),row_index,10+self._prevGWcount+i,alignment=QtCore.Qt.AlignHCenter)

	def show(self):
		self.window.show()
		self.app.exec()

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

	def recolor_by_team(self,widget,team):

		style = team._style

		if style is None:
			return

		widget.setStyleSheet(f"background-color: {style['background-color']}; color: {style['color']}")

if __name__ == '__main__':
	main()