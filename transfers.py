#!/usr/bin/env python3

import os
import mout
from api import FPL_API
from player import Player
from manager import Manager
from squad import Squad
import random
import sys

def main():

	if len(sys.argv) > 1:
		lookforward = int(sys.argv[1])
	else:
		lookforward = 5

	# extra cash for any pre-booked but not executed transfers
	extra = 0.0

	consider_best11 = True

	use_official = False
	if lookforward == 1:
		use_official = True

	api = FPL_API()

	gw = api._current_gw

	man = Manager("Max Winokan", 780664, api, authenticate=True)

	liquid = sum([p.selling_price for p in man.players])
	# liquid = sum([p.selling_price for p in man.players])

	mout.varOut("liquid",f'£{liquid+man._bank_balance[-1]:.1f}')

	mout.varOut("current squad next5",f'{man.squad.next5_expected():.1f}',unit="xPts")

	mout.headerOut("\nSuggested Multipliers:")

	mout.headerOut(f"\nGW{gw}:")
	man.squad.set_best_multipliers(gw,summary=True,use_official=use_official)
	mout.headerOut(f"\nGW{gw+1}:")
	man.squad.set_best_multipliers(gw+1,summary=True,use_official=use_official)
	mout.headerOut(f"\n")
	# mout.headerOut(f"\nGW{gw+2}:")
	# man.squad.set_best_multipliers(gw+2,summary=True,use_official=False)
	# mout.headerOut(f"\nGW{gw+3}:")
	# man.squad.set_best_multipliers(gw+3,summary=True,use_official=False)

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
	
	gkps = [p for p in players if p.position_id == 1]
	defs = [p for p in players if p.position_id == 2]
	mids = [p for p in players if p.position_id == 3]
	fwds = [p for p in players if p.position_id == 4]

	names = [p.name for p in man.players]

	options = []
	
	if consider_best11:

		for i,p in enumerate(man.players):

			if p.position_id == 1:
				affordable = [q for q in gkps if q.price <= p.selling_price + man._bank_balance[-1] + extra and q.name not in names and q.next_expected(lookforward,use_official) > p.next_expected(lookforward,use_official)]
			elif p.position_id == 2:
				affordable = [q for q in defs if q.price <= p.selling_price + man._bank_balance[-1] + extra and q.name not in names and q.next_expected(lookforward,use_official) > p.next_expected(lookforward,use_official)]
			elif p.position_id == 3:
				affordable = [q for q in mids if q.price <= p.selling_price + man._bank_balance[-1] + extra and q.name not in names and q.next_expected(lookforward,use_official) > p.next_expected(lookforward,use_official)]
			elif p.position_id == 4:
				affordable = [q for q in fwds if q.price <= p.selling_price + man._bank_balance[-1] + extra and q.name not in names and q.next_expected(lookforward,use_official) > p.next_expected(lookforward,use_official)]

			for q in affordable:

				total = 0

				for j in range(gw,gw+lookforward):

					total += man.squad.expected_transfer_return(j,p,q)

				j._temp = total

			replacement = sorted(affordable, key=lambda x: x._temp, reverse=True)

			if len(replacement) < 1:
				continue

			replacement = replacement[0]

			options.append(dict(index=i,replacement=replacement,gain=replacement.next_expected(lookforward,use_official)-p.next_expected(lookforward,use_official)))

	else:

		for i,p in enumerate(man.players):

			# get best affordable replacement

			if p.position_id == 1:
				affordable = [q for q in gkps if q.price <= p.selling_price + man._bank_balance[-1] + extra and q.name not in names and q.next_expected(lookforward,use_official) > p.next_expected(lookforward,use_official)]
			elif p.position_id == 2:
				affordable = [q for q in defs if q.price <= p.selling_price + man._bank_balance[-1] + extra and q.name not in names and q.next_expected(lookforward,use_official) > p.next_expected(lookforward,use_official)]
			elif p.position_id == 3:
				affordable = [q for q in mids if q.price <= p.selling_price + man._bank_balance[-1] + extra and q.name not in names and q.next_expected(lookforward,use_official) > p.next_expected(lookforward,use_official)]
			elif p.position_id == 4:
				affordable = [q for q in fwds if q.price <= p.selling_price + man._bank_balance[-1] + extra and q.name not in names and q.next_expected(lookforward,use_official) > p.next_expected(lookforward,use_official)]

			replacement = sorted(affordable, key=lambda x: x.next_expected(lookforward,use_official)-p.next_expected(lookforward,use_official), reverse=True)

			if len(replacement) < 1:
				continue

			replacement = replacement[0]

			options.append(dict(index=i,replacement=replacement,gain=replacement.next_expected(lookforward,use_official)-p.next_expected(lookforward,use_official)))

	mout.headerOut("\nSuggested Transfers:")

	sorted_options = sorted(options, key=lambda x: x['gain'], reverse=True)

	str_buffer = "From,To,"
	for i in range(gw+1,gw+1+lookforward):
		str_buffer += f"GW{i},"
	str_buffer += f"Total,"
	str_buffer += f"Budget\n"
	
	for option in sorted_options:
		str_buffer += f'{man.players[option["index"]]},{option["replacement"].name},'
		for i in range(gw+1,gw+1+lookforward):
			str_buffer += f'{option["replacement"].expected_points(gw=i)-man.players[option["index"]].expected_points(gw=i):.1f},'
		str_buffer += f'+{option["gain"]:.1f},'
		str_buffer += f'+{man.players[option["index"]].selling_price-option["replacement"].price:.1f}'
		str_buffer += '\n'

	result = os.popen(f'echo "{str_buffer}" | table.sh -s ","').read()

	print(result)

	api.finish()

if __name__ == '__main__':
	main()
