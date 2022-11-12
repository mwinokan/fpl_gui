#!/usr/bin/env python

''' 

if player has DGW
	if still has gw==event fixture then has outstanding fixture


'''

from player import Player
from squad import Squad
from manager import Manager

import api as fpl_api

api = fpl_api.FPL_API()

player = Player("Bowen",api)

print(player)
print(player.fixtures)
print(player.fixtures.keys())

print()

for event,team_h,team_a,is_home in zip(player.fixtures['event'],
									   player.fixtures['team_h'],
									   player.fixtures['team_a'],
									   player.fixtures['is_home']
									   ):
	if is_home:
		print(event,api.team_name(team_a))
	else:
		print(event,api.team_name(team_h))

print()

print(player.outstanding_gwfix)
