#!/usr/bin/env python3

'''

dash_FPL:

- take a dataframe of the players

- Filter based on position, price, team, etc.

- if clicking on a player get graphs of previous and future results/predictions

'''

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

from api import FPL_API

api = FPL_API()

elements = api._bootstrapjson['elements']
df = pd.DataFrame.from_records(elements)

df = df.astype({'now_cost': float})
df = df.astype({'total_points': int})
df = df.astype({'element_type': int})
df = df.astype({'selected_by_percent': float})

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Dash FPL', style={'textAlign':'center'}),
    dcc.Dropdown(['All'] + list(df.team.unique()), 'All', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
        
    if value == 'All':
        dff = df
    else:
        dff = df[df.team==value]

    return px.scatter(dff, x='now_cost', y='total_points',color='element_type',size='selected_by_percent')

if __name__ == '__main__':
    app.run_server(debug=True)
    