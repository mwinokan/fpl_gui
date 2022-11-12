#!/usr/bin/env python

from manager import Manager
import api as fpl_api
import plot

def main():

	api = fpl_api.FPL_API()

	managers = [
				{"name":"Max","id":1448993},
				{"name":"Iain","id":1804273},
				{"name":"Jonah","id":647640},
				{"name":"Minh","id":3966264},
				{"name":"Sean","id":4953153},
				{"name":"Ash","id":2048541},
				{"name":"Karim","id":3240501},
				]

	league = []

	for manager in managers:
		league.append(Manager(manager['name'],manager['id'],api))

	show = False
	plot.event_points(league,api,show=show)
	plot.event_points(league,api,show=show,relative=True)
	plot.total_points(league,api,show=show)
	plot.total_points(league,api,show=show,relative=True)
	plot.overall_rank(league,show=show)
	plot.gameweek_rank(league,show=show)
	plot.squad_value(league,show=show)

if __name__ == '__main__':
	main()
