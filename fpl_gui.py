#!/usr/bin/env python

'''

	To-Do's

	+	Show chip usage on graphs
	
	+	Rework JSON I/O to include player names
	+	Fix totals
	+	Fix set_checkboxes()

'''

# from .gui import FantasyGui

from player import Player
from squad import Squad
from manager import Manager

import api as fpl_api

from gui import FPL_Window

import plot

def main():

	print("main()")

	api = fpl_api.FPL_API()

	players = [
				"Sánchez",
				"Steele",
				"Alexander-Arnold",
				"Shaw",
				"White",
				"Tsimikas",
				"Amartey",
				"Jota",
				"Havertz",
				"Fernandes",
				"Benrahma",
				"Son",
				"Ings",
				"Iheanacho",
				"Toney",
				"Rowe",
				"Saka",
				"Buendía",
				"Raphinha",
				"Greenwood",
				"Kane",
				"Ziyech",
				"Bailey",
				"Coufal",
				"Rüdiger",
				"Antonio",
				"Ayling",
				"Salah"
				]

	players = [
				"Bachman",
				"Foster",
				"Alexander-Arnold",
				"Veltman",
				"White",
				"Ayling",
				"Tsimikas",
				"Gündogan",
				"Harvey Barnes",
				"Fernandes",
				"Benrahma",
				"Salah",
				"Ings",
				"Wood",
				"Toney",
				"Michail Antonio",
				"Bissouma",
				"Livramento",
				"Dier",
				"Ismaila Sarr",
				"Bailey",
				"Jota",
				"Havertz",
				"Rowe",
				"Saka",
				"Buendía",
				"Raphinha",
				"Greenwood",
				"Kane",
				"Amartey",
				"Ziyech",
				"Coufal",
				"Rüdiger",
				"Emmanuel Dennis",
				"Son",
				"Lukaku"
				]

	managers = [
					{"name":"Max","id":1448993},
					{"name":"Iain","id":1804273},
					{"name":"Jonah","id":647640},
					{"name":"Minh","id":3966264},
					{"name":"Sean","id":4953153},
					{"name":"Ash","id":2048541},
					{"name":"Karim","id":3240501},
					]

	squad = Squad()

	for player in players:
		player = Player(player,api)
		# print(player)
		squad.add_player(player)

	league = []

	for manager in managers:
		league.append(Manager(manager['name'],manager['id'],api))

	# squad.players[0].get_event_score(gw=1)

	# print(squad.value)

	show = False
	plot.event_points(league,api,show=show)
	plot.event_points(league,api,show=show,relative=True)
	plot.total_points(league,api,show=show)
	plot.total_points(league,api,show=show,relative=True)
	plot.overall_rank(league,show=show)
	plot.gameweek_rank(league,show=show)
	plot.squad_value(league,show=show)
	# plot.bank_balance(league)

	# window = FPL_Window(squad.players,api)

	# window.set_checkboxes(first_15_true=True)

	# window.show()

if __name__ == '__main__':
	main()
