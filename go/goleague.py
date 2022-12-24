#!/usr/bin/env python3

from league import League
# from ..league import League
import api as fpl_api
import plotly.io as pio 
import plotly.graph_objects as go
from plotly.offline import plot
import re
import mout

def main():

	api = fpl_api.FPL_API()

	league_id = 663873

	league = League(league_id,api)

	create_league_figure(api,league,show=True)

def create_league_figure(api,league,subset=None,show=False):
	gw = api._current_gw
	mout.debugOut(f"create_league_figure()")

	if subset:
		print(subset)

	fig = go.Figure()
	
	data = [(i+1,y) for i,y in enumerate(api.get_event_averages()) if i+1 not in api._skip_gws]

	x = [0]+[d[0] for d in data]
	y = [d[1] for d in data]
	y = [0]+[sum(y[:i+1]) for i,_ in enumerate(y)]

	data_dict = dict()
	for x,y in zip(x,y):
		data_dict[x] = y

	for i,man in enumerate(sorted(league.managers,key= lambda x: x.name)):

		pts = man._total_points

		text = [None]+man.chip_text_list(with_name=False)

		this_x = [i for i in man.active_gws if i not in api._skip_gws]
		this_y = [p-data_dict[i] for i,p in zip(man.active_gws,pts) if i not in api._skip_gws]

		if this_x[0] == 1:
			this_x = [0] + this_x
			this_y = [0] + this_y

		if subset and man.id not in subset:
			visible = 'legendonly'
		else:
			visible = True

		# print(man,visible)

		fig.add_trace(go.Scatter(name=man.name,opacity=1.0,x=this_x,text=text, y=this_y,visible=visible,textposition="bottom center",mode='markers+lines+text',customdata=[man._gui_url for x in this_x]))

	fig.update_traces(marker=dict(line=dict(width=1,color='Black')),selector=dict(mode='markers'))

	fig.update_layout(legend_title_text = f"{league.name}",autosize=True,margin=dict(l=20, r=20, t=20, b=20))
	fig.update_xaxes(title_text=f"Gameweek")
	fig.update_yaxes(title_text=f"Total points relative to global average",zeroline=True, zerolinewidth=2, zerolinecolor='Black')

	# Get HTML representation of plotly.js and this figure
	plot_div = plot(fig, output_type='div', include_plotlyjs=True)

	# Get id of html div element that looks like
	# <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
	res = re.search('<div id="([^"]*)"', plot_div)
	div_id = res.groups()[0]

	# Build JavaScript callback for handling clicks
	# and opening the URL in the trace's customdata 
	js_callback = """
	<script>
	var plot_element = document.getElementById("{div_id}");
	plot_element.on('plotly_click', function(data){{
	    console.log(data);
	    var point = data.points[0];
	    if (point) {{
	        console.log(point.customdata);
	        window.open(point.customdata);
	    }}
	}})
	</script>
	""".format(div_id=div_id)

	# Build HTML string
	html_str = """{plot_div}
	{js_callback}
	""".format(plot_div=plot_div, js_callback=js_callback)

	# # Write out HTML file
	# with open('go/value.html', 'w') as f:
	#     f.write(html_str)

	if show:
		pio.write_html(fig, file='go/value.html', auto_open=show)
		# fig.show()

	return html_str

if __name__ == '__main__':
	main()
