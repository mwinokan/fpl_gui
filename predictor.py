#!/usr/bin/env python

# for all the players in the game (filter by selection)
# for each gameweek 6 -> current
# can we correlate their form to the fixture difficulty ranking

from player import Player
from squad import Squad

import api as fpl_api

import mplot
import mout

import matplotlib.pyplot as plt
from scipy import stats
from scipy import optimize
import numpy as np

import json as js

test = False

def linear(x,a,b):
	return a*x + b

def knee(x,a,b,c):
	if len(x) > 1:

		d = (a-b)*c

		firsthalf = [a*v for v in x if v < c]
		secondhalf = [b*v+d for v in x if v >= c]

		return np.array(firsthalf+secondhalf)

def main():

	api = fpl_api.FPL_API()

	names = [
				"Trent",
				"Salah",
				"Díaz",
				"Darwin",
				"Robertson",
				"Firmino",
			]

	# create a player test case

	fig,ax = plt.subplots()

	# print(api._elements.keys())

	if test:
		# for name in names:
		p = Player("Reece James", api)
		p.expected_points(gw=5,debug=True,fit_ratio=0.8,use_official=False)
		p.expected_points(gw=5,debug=True,fit_ratio=0.8)
		# p.expected_total_points(debug=True)

		p = Player("Saliba", api)
		p.expected_points(gw=5,debug=True,fit_ratio=0.8,use_official=False)
		p.expected_points(gw=5,debug=True,fit_ratio=0.8)
		# p.expected_total_points(debug=True)

		exit()

	# for all known results in the game compare predicted result to actual

	error = 0
	count = 0

	for team in api.teams:

		for fix_d in team.fixtures:

			if not fix_d['started']:
				continue

			count += 1

			opponent = team.get_opponent(fix_d['event'])	
			exp = team.expected_clean_sheet(opponent)

			if fix_d['team_h'] == team.id:
				if fix_d['team_a_score'] == 0:
					diff = exp - 1
				else:
					diff = exp - 0
			elif fix_d['team_a'] == team.id:
				if fix_d['team_h_score'] == 0:
					diff = exp - 1
				else:
					diff = exp - 0
			error += abs(diff)

	mout.varOut("Average clean sheet error",error/count)

	defender_xdata = []
	defender_ydata = []
	midfielder_xdata = []
	midfielder_ydata = []
	forward_xdata = []
	forward_ydata = []

	actual_total_points = []
	expected_total_points = []

	player_ids = api._elements['id']
	for pid in player_ids:
		index = api.get_player_index(pid)
		if index%50 == 0:
			print(index)
		p = Player(None, api, index=index)

		# plt.scatter(p.history['creativity'],p.history['assists'],label=p.name)
		# plt.scatter(p.history['threat'],p.history['goals_scored'],label=p.name)
		# plt.scatter(p.history['ict_index'],p.attacking_history,label=p.name)

		expected, actual = p.expected_total_points(return_actual=True,fit_ratio=0.8,use_official=False)

		actual_total_points.append(actual)
		expected_total_points.append(expected)

		# if expected > 50:
		# 	print(p.name,expected,actual)

		if p.position_id == 1:
			continue
		elif p.attacking_points_per90 == 0:
			continue
		elif p.position_id == 2:
			# defender_xdata += p.ct_history_scaled
			# defender_ydata += p.attacking_history
			defender_xdata.append(p.ct_total_scaled)
			defender_ydata.append(p.attacking_points_per90)
		elif p.position_id == 3:
			midfielder_xdata.append(p.ct_total_scaled)
			midfielder_ydata.append(p.attacking_points_per90)
		elif p.position_id == 4:
			forward_xdata.append(p.ct_total_scaled)
			forward_ydata.append(p.attacking_points_per90)
	
	plt.scatter(defender_xdata,defender_ydata,label=p.name,color='r')
	plt.scatter(midfielder_xdata,midfielder_ydata,label=p.name,color='g')
	plt.scatter(forward_xdata,forward_ydata,label=p.name,color='b')

	x_min = 0
	x_max = max(defender_xdata+midfielder_xdata+forward_xdata)
	x = np.linspace(x_min, x_max,200)

	# defenders
	def_popt,_ = optimize.curve_fit(linear,defender_xdata, defender_ydata,bounds=([0,0],[np.inf,0.1]))
	plt.plot(x, def_popt[1] + def_popt[0]*x, 'r')
	mout.headerOut("Defenders")
	mout.varOut("slope",f"{def_popt[0]:.6f}")
	mout.varOut("intercept",f"{def_popt[1]:.6f}")
	
	# popt,_ = optimize.curve_fit(knee,defender_xdata, defender_ydata,bounds=([0,0,400],[np.inf,np.inf,np.inf]))
	# plt.plot(x, knee(x,popt[0],popt[1],popt[2]), 'r')

	# midfielder
	mid_popt,_ = optimize.curve_fit(linear,midfielder_xdata,midfielder_ydata,bounds=([0,0],[np.inf,0.1]))
	plt.plot(x, mid_popt[1] + mid_popt[0]*x, 'g')
	mout.headerOut("Midfielders")
	mout.varOut("slope",f"{mid_popt[0]:.6f}")
	mout.varOut("intercept",f"{mid_popt[1]:.6f}")

	# popt,_ = optimize.curve_fit(knee,midfielder_xdata, midfielder_ydata,bounds=([0,0,400],[np.inf,np.inf,np.inf]))
	# plt.plot(x, knee(x,popt[0],popt[1],popt[2]), 'g')

	# forward
	fwd_popt,_ = optimize.curve_fit(linear,forward_xdata,forward_ydata,bounds=([0,0],[np.inf,0.1]))
	plt.plot(x, fwd_popt[1] + fwd_popt[0]*x, 'b')
	mout.headerOut("Forwards")
	mout.varOut("slope",f"{fwd_popt[0]:.6f}")
	mout.varOut("intercept",f"{fwd_popt[1]:.6f}")

	# popt,_ = optimize.curve_fit(knee,forward_xdata, forward_ydata,bounds=([0,0,400],[np.inf,np.inf,np.inf]))
	# plt.plot(x, knee(x,popt[0],popt[1],popt[2]), 'b')
	
	data = {'def':{"slope":def_popt[0],"intercept":def_popt[1]},'mid':{"slope":mid_popt[0],"intercept":mid_popt[1]},'fwd':{"slope":fwd_popt[0],"intercept":fwd_popt[1]}}

	js.dump(data,open('ct_total_fit.json','wt'), indent="\t")

	ax.set_ylabel("G+A Points")
	ax.set_xlabel("ict_index")

	# plt.legend(loc='best')
	
	plt.savefig("images/ct_total_fit.pdf")
	plt.show()
	plt.close()

	fig,ax = plt.subplots()

	plt.scatter(expected_total_points, actual_total_points)

	ax.set_ylabel("Actual Points")
	ax.set_xlabel("Expected Points")

	x_min = 0
	x_max = max(expected_total_points)
	x = np.linspace(x_min, x_max,200)

	# all
	res = stats.linregress(expected_total_points, actual_total_points)
	plt.plot(x, res.intercept + res.slope*x, 'b')
	mout.headerOut("All")
	mout.varOut("R-squared",f"{res.rvalue**2:.6f}")
	mout.varOut("slope",f"{res.slope:.6f}")
	mout.varOut("intercept",f"{res.intercept:.6f}")

	plt.savefig("images/expected_vs_actual.pdf")
	plt.show()
	plt.close()

	# print(res)

if __name__ == '__main__':
	main()
