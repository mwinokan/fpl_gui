#!/usr/bin/env python3

import markdown
import mout

player_modals = {}
player_history_tables = {}

def md2html(md):
	html = markdown.markdown(md, extensions=['extra'])
	html = fix_image_links(html)
	html = fix_table_classes(html)
	html = fix_column_divs(html)
	return html

def fix_column_divs(html):
	# html = html.replace("<h1>_tag_div_class_row</h1>",'<div class="row">')
	# html = html.replace("<h1>_tag_div_class_column</h1>",'<div class="column">')
	# html = html.replace("<h1>_tag_enddiv</h1>",'</div>')

	html = html.replace("<h1>_tag_div_class_column</h1>",'<div class="w3-col s12 m6">')
	html = html.replace("<h1>_tag_enddiv</h1>",'</div>')
	return html

def fix_image_links(html):
	'''
	[[https://github.com/mwinokan/FPL_GUI/blob/main/kits/Newcastle.png]] 
					
					|
					V

	<img class="w3-image" src="/w3images/jane.jpg" alt="Fashion Blog" width="1600" height="1060">
	'''
	html = html.replace("[[https://",'<img class="w3-image" src="https://')
	html = html.replace(".png]]",'.png?raw=true" alt="Kit Icon" width="22" height="29">')
	return html

	# https://github.com/mwinokan/FPL_GUI/blob/main/kits/Newcastle.png?raw=true

def fix_table_classes(html):
	# https://www.w3schools.com/w3css/w3css_tables.asp

	'''
	<table>    --> 		<table class="w3-table-all w3-hoverable">
	'''

	html = html.replace('<table>','<div class="w3-responsive">\n<table class="w3-table-all w3-hoverable">')
	html = html.replace('</table>','</table>\n</div>')
	return html

def html_page(target,mdfile=None,title="FPL_GUI",sidebar_content=None,gw=None,html=None,showtitle=True,bar_html=None,extra_style=None):
	mout.debugOut(f"html_page({target})")
	
	'''			
				Max's FPL GUI
		---------------------------
					 		|
			MARKDOWN		| SIDE
			CONTENT	 		| -BAR
					 		|
	'''

	if mdfile is None:
		html_content = html
	else:
		with open(mdfile,'rt') as fin:
			html_content = md2html(fin.read())

	sidebar_html = ""
	if sidebar_content is not None:
		sidebar_html = md2html(sidebar_content)

	fout = open(target,'wt')

	fout.write('<!DOCTYPE html>\n')
	fout.write('<html>\n')
	fout.write('<head>\n')
	fout.write(f'<title>{title}</title>\n')
	fout.write('<meta charset="UTF-8">\n')
	fout.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')
	fout.write('<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\n')
	fout.write('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Oswald">\n')
	fout.write('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open Sans">\n')
	fout.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">\n')
	fout.write('<style>\n')
	fout.write('h1,h2,h3,h4,h5,h6 {font-family: "Oswald"}')
	fout.write('body {font-family: "Open Sans"}\n')
	fout.write('h5.double {line-height: 2}\n')
	if extra_style is not None:
		fout.write(extra_style)
	fout.write('</style>\n')
	fout.write('</head>\n')
	# fout.write('<body class="w3-light-grey">\n') ### COMMENT
	fout.write('<!-- w3-content defines a container for fixed size centered content, ')
	fout.write('and is wrapped around the whole page content, except for the footer in this example -->\n')
	fout.write('<div class="w3-content" style="max-width:2000px">\n')
	fout.write('<!-- Header -->\n')
	fout.write('<header class="w3-container w3-center w3-padding-48 w3-white">\n')
	fout.write('<h1 class="w3-xxxlarge"><b>FPL <span class="w3-tag">GUI</span></b></h1>\n')
	fout.write('<h6>Max Winokan</h6>\n')
	fout.write('</header>\n')
	if bar_html is not None:
		fout.write(bar_html)
	fout.write('<!-- Grid -->\n')
	fout.write('<div class="w3-row w3-border">\n')
	fout.write('<!-- Content -->\n')
	# fout.write('<div class="w3-col l8 s12">\n')
	fout.write('<div class="w3-col l12 s12">\n') 
	# fout.write('<div class="w3-container w3-white">\n')
	fout.write('<div class="w3-container w3-white w3-padding">\n')
	# fout.write('<div class="w3-container w3-white w3-margin w3-padding-large">\n')
	if showtitle:
		fout.write('<div class="w3-center">\n')
		fout.write(f'<h1>{title}</h1>\n')
		fout.write('</div>\n')
	fout.write('<div class="w3-justify">\n')
	fout.write(html_content)
	fout.write('</div>\n')
	fout.write('</div>\n')
	fout.write('<hr>\n')
	fout.write('</div>\n')
	# if bar_html is None:
	# 	fout.write('<!-- Sidebar -->\n')
	# 	fout.write('<div class="w3-col l4">\n')
	# 	fout.write('<div class="w3-white w3-margin">\n')
	# 	fout.write('<div class="w3-container w3-black">\n')
	# 	fout.write('<h4>FPL_GUI</h4>\n')
	# 	fout.write(sidebar_html)
	# 	fout.write('</div>\n')
	# 	fout.write('</div>\n')
	# 	# fout.write('<hr>\n')
	# 	fout.write('</div>\n')
	fout.write('<!-- END GRID -->\n')
	fout.write('</div>\n')
	fout.write('<!-- END w3-content -->\n')
	# fout.write('</div>\n') ### COMMENT
	fout.write('<!-- Footer -->\n')
	fout.write('<footer class="w3-container w3-dark-grey" style="padding:32px">\n')
	if sidebar_html is not None:
		fout.write(sidebar_html)
	fout.write('<a href="#" class="w3-button w3-black w3-padding-large w3-margin-bottom"><i class="fa fa-arrow-up w3-margin-right"></i>Back to top</a>\n')
	fout.write('<div class="w3-center">\n')

	from datetime import datetime
	timestamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

	fout.write(f'<p>Accurate as of {timestamp}, (GW{gw})</p>\n')
	fout.write('<p>Max Winokan <span class="w3-tag">mwinokan@me.com</span></a></p>\n')
	fout.write('</div>\n')
	fout.write('</footer>\n')
	# fout.write('</body>\n') ### COMMENT
	fout.write('</html>\n')

	fout.close()

def player_summary_cell_modal(player,gw):

	global player_modals

	if player.id not in player_modals.keys():
		player_modals[player.id] = {}

	if gw not in player_modals[player.id].keys():

		score, summary = player.get_event_score(gw,summary=True,md_bold=False,return_str=True)

		summary = summary.replace("\n","</p>\n<p>")
		summary = '<p>' + summary + '</p>'

		html_buffer = ""
		
		status = None
		if score in ["Did not play","Bench","Yet to play"]:
			status = score
			score = None

		if score is not None:
			style_str = get_style_from_event_score(score)
		if gw == player._api.current_gw and player.multiplier == 0:
			stag = "<s>"
			etag = "</s>"
		else:
			stag = ""
			etag = ""

		id = f'id{player.id}_{gw}'
		
		html_buffer += """<td onclick="document.getElementById('"""
		html_buffer += f'{id}'
		html_buffer += """').style.display='block'" class="w3-center" """

		if score is None:
			if status == 'Did not play':
				html_buffer += f' style="border:2px solid white;border-collapse:collapse;">x'
			elif status == 'Bench':
				html_buffer += f' style="border:2px solid white;border-collapse:collapse;">🪑'
			elif status == 'Yet to play':
				html_buffer += f' style="border:2px solid white;border-collapse:collapse;">-'
			else:
				html_buffer += f' style="border:2px solid white;border-collapse:collapse;">o'
		else:
			html_buffer += f' style={style_str}>'
			html_buffer += f'{stag}{score}{etag}'

		html_buffer += f'</td>'
		html_buffer += f'<div id="{id}" class="w3-modal">'
		html_buffer += f'<div class="w3-modal-content">'
		html_buffer += f'<div class="w3-container">'
		html_buffer += """<span onclick="document.getElementById('"""
		html_buffer += f'{id}'
		html_buffer += """').style.display='none'" class="w3-button w3-display-topright">&times;</span>"""
		html_buffer += f'<h3>{player.name} in GW{gw}</h3>'
		html_buffer += f'{summary}'

		# history table

		html_buffer += f'</div>'
		html_buffer += f'</div>'
		html_buffer += f'</div>'

		player_modals[player.id][gw] = html_buffer

	return player_modals[player.id][gw]

def get_player_history_table(player):

	''' Add fixture scores/results '''

	global player_history_tables

	if player.id not in player_history_tables.keys():

		html_buffer = ""
		
		html_buffer += '<div class="w3-responsive">\n'
		html_buffer += '<table class="w3-table-all w3-hoverable">\n'
		html_buffer += '<thead>\n'
		html_buffer += '<tr>\n'
		html_buffer += '<th class="w3-center">GW</th>\n'
		html_buffer += '<th class="w3-center">Opponent</th>\n'
		html_buffer += '<th class="w3-center">xPts.</th>\n'
		html_buffer += '<th class="w3-center">Score</th>\n'
		html_buffer += '<th>Summary</th>\n'
		html_buffer += '</tr>\n'
		html_buffer += '</thead>\n'
		html_buffer += '<tbody>\n'

		now_gw = player._api._current_gw
		# start_gw = max(1,now_gw-prev_gw_count)
		# end_gw = min(38,now_gw+next_gw_count)

		# for gw in range(1,now_gw+1):
		for gw in range(1,38):

			if gw == now_gw:
				html_buffer += f'<tr class="w3-green">\n'
			else:
				html_buffer += f'<tr>\n'

			html_buffer += f'<td class="w3-center">'
			html_buffer += f'{gw}'
			html_buffer += f'</td>\n'

			# difficulty = player.get_fixture_diff(gw,old=True,overall=False)
			# style_str = get_style_from_difficulty(difficulty,old=True)
			# if style_str is None:
				# style_str == ""
			style_str = ""
			flag_str = ""
			chance = player.get_playing_chance(gw)
			if chance < 0.25:
				flag_str = '⛔️ '
			elif chance < 1:
				flag_str = '⚠️ '
			html_buffer += f'<td class="w3-center" style={style_str}>'
			opp = player.team_obj.get_opponent(gw)
			if opp is not None:
				is_home = player.team_obj.get_gw_fixtures(gw)['team_a'] == opp.id
				opp_str = opp.shortname
				if is_home:
					opp_str += " (H)"
				else:
					opp_str += " (A)"
				html_buffer += f'<img class="w3-image" src="{opp._badge_url}" alt="{opp.shortname}" width="20" height="20"> '
				html_buffer += f'{opp_str}{flag_str}'
			else:
				html_buffer += f'-'
			html_buffer += '</td>\n'

			# html_buffer += f'<td class="w3-center">'
			# html_buffer += f'{player.expected_points(gw=gw)}'
			# html_buffer += f'</td>\n'

			html_buffer += """<td class="w3-center" """
			exp = player.expected_points(gw=gw,fit_ratio=0.8)
			style_str = get_style_from_event_score(exp)
			html_buffer += f' style={style_str}>'
			html_buffer += f'{exp:.1f}'
			html_buffer += f'</td>\n'

			if gw <= now_gw:

				score, summary = player.get_event_score(gw,summary=True,md_bold=True,return_str=True,pts_line=False,team_line=False)

				# summary = summary.replace("\n","<br>")
				summary = summary.replace("\n"," ")
				
				status = None
				if score in ["Did not play","Bench","Yet to play"]:
					status = score
					score = None

				if score is not None:
					style_str = get_style_from_event_score(score)

				html_buffer += """<td class="w3-center" """

				if score is None:
					if status == 'Did not play':
						html_buffer += f' style="border:2px solid white;border-collapse:collapse;">x'
					elif status == 'Bench':
						html_buffer += f' style="border:2px solid white;border-collapse:collapse;">🪑'
					elif status == 'Yet to play':
						html_buffer += f' style="border:2px solid white;border-collapse:collapse;">-'
					else:
						html_buffer += f' style="border:2px solid white;border-collapse:collapse;">o'
				else:
					html_buffer += f' style={style_str}>'
					html_buffer += f'{score}'
				html_buffer += f'</td>\n'

				html_buffer += '<td>'
				html_buffer += f'{summary}'
				html_buffer += '</td>\n'

			# else:
			# 	html_buffer += '<td class="w3-center">'
			# 	html_buffer += '-'
			# 	html_buffer += '</td>\n'
			# 	html_buffer += '<td class="w3-center">'
			# 	html_buffer += '-'
			# 	html_buffer += '</td>\n'

			html_buffer += f'</tr>\n'
		
		html_buffer += f'</tbody>\n'
		html_buffer += f'</table>\n'
		html_buffer += f'</div>\n'

		# print(player.fixtures)

		player_history_tables[player.id] = html_buffer

	return player_history_tables[player.id]

def get_style_from_event_score(score):
	style_str = '"border:2px solid white;border-collapse:collapse;'
	if score < 1:
		style_str += 'background-color:darkred;color:white'
	elif score == 2:
		style_str += 'background-color:orange;color:black'
	elif score > 9:
		style_str += 'background-color:darkgreen;color:white'
	elif score > 5:
		style_str += 'background-color:lightgreen;color:black'
	elif score > 2:
		style_str += 'background-color:yellow;color:black'
	elif score > 0:
		style_str += 'background-color:red;color:black'	
	style_str += '"'
	return style_str
