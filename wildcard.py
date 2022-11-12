#!/usr/bin/env python3

import mout
from api import FPL_API
from player import Player
from manager import Manager
from squad import Squad
import random

def main():

	api = FPL_API()

	gw = api._current_gw

	man = Manager("Max Winokan", 780664, api, authenticate=True)

	liquid = sum([p.selling_price for p in man.players])
	# liquid = sum([p.selling_price for p in man.players])

	mout.varOut("liquid",f'£{liquid:.1f}')

	mout.varOut("current squad next5",f'{man.squad.next5_expected():.1f}',unit="xPts")

	man.squad.set_best_multipliers(gw,summary=True,use_official=False)

	# exit()

	players = []

	player_ids = api._elements['id']
	for i,pid in enumerate(player_ids):
		if api._elements['minutes'][i] < 90:
			continue
		mout.progress(i,len(player_ids))
		index = api.get_player_index(pid)
		p = Player(None, api, index=index)
		p.next5_expected
		players.append(p)
	mout.progress(len(player_ids),len(player_ids))

	# sorted_players = sorted(players, key=lambda x: x.next5_expected, reverse=True)

	gkps = [p for p in players if p.position_id == 1]
	defs = [p for p in players if p.position_id == 2]
	mids = [p for p in players if p.position_id == 3]
	fwds = [p for p in players if p.position_id == 4]

	trials = 1000000
	best_score = 0

	xdata = []
	ydata = []

	for i in range(trials):
		mout.progress(i,trials)

		try_players = []
		try_players += random.sample(gkps,2)
		try_players += random.sample(defs,5)
		try_players += random.sample(mids,5)
		try_players += random.sample(fwds,3)

		if sum([p.price for p in try_players]) > liquid:
			continue

		try_sqd = Squad(api=api)
		for p in try_players:
			try_sqd.add_player(p)

		next5_score = try_sqd.next5_expected()
		if next5_score > best_score:
			best = try_sqd
			best_score = next5_score

		xdata.append(i)
		ydata.append(next5_score)
	
	mout.progress(trials,trials)

	print(best)

	mout.varOut("wc squad next5",f'{best.next5_expected():.1f}',unit="xPts")

def squad_next5(players):
	return sum([p.next5_expected for p in players])

# def squad_setmultipliers(players):


if __name__ == '__main__':
	main()
