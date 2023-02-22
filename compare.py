#!/usr/bin/env python3

import mout
from api import FPL_API
from player import Player

api = FPL_API()

gw_range = 3
gw_range = range(api.current_gw+1,api.current_gw+gw_range+1)

option1 = ['Salah','Tarkowski','Gomez']
option2 = ['Grealish','Gakpo','Robertson']

# all_players = option1 + option2

for i,p in enumerate(option1):
	option1[i] = Player(p, api)

for i,p in enumerate(option2):
	option2[i] = Player(p, api)

# print(all_players)
# print(option1)
# print(option2)

def header():
	print(f'{"NAME":12} {"PRICE":4}',end=' ')
	for gw in gw_range:
		print(f'GW{gw:2}',end=' ')
	print('')

mout.headerOut("\nOPTION 1")
header()
data1 = {}
for p in option1:
	print(f'{p.name:12} £{p.price:4}',end=' ')
	data1[p.id] = {}
	data1['total'] = {}
	for gw in gw_range:
		xpts = p.expected_points(gw=gw)
		if gw not in data1['total'].keys():
			data1['total'][gw] = 0.0
		else:
			data1['total'][gw] += xpts
		data1[p.id][gw] = xpts
		print(f'{xpts:4.1f}',end=' ')
	print('')
total = sum([p.price for p in option1])
mout.headerOut(f'{"TOTAL":12} £{total:4}',end=' ')
for gw in gw_range:
	total = sum([data1[p.id][gw] for p in option1])
	mout.headerOut(f'{total:4.1f}',end=' ')

print('')

mout.headerOut("\nOPTION 2")
header()
data2 = {}
for p in option2:
	print(f'{p.name:12} £{p.price:4}',end=' ')
	data2[p.id] = {}
	data2['total'] = {}
	for gw in gw_range:
		xpts = p.expected_points(gw=gw)
		if gw not in data2['total'].keys():
			data2['total'][gw] = 0.0
		else:
			data2['total'][gw] += xpts
		data2[p.id][gw] = xpts
		print(f'{xpts:4.1f}',end=' ')
	print('')
total = sum([p.price for p in option2])
mout.headerOut(f'{"TOTAL":12} £{total:4}',end=' ')
for gw in gw_range:
	total = sum([data2[p.id][gw] for p in option2])
	mout.headerOut(f'{total:4.1f}',end=' ')

print('')
