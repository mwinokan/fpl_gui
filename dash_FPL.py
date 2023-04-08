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

df = api.parse_bootstrap()

print(df.columns)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
        


    # dff = df[df.country==value]


    return px.line(df, x='year', y='pop')

if __name__ == '__main__':
    app.run_server(debug=True)
    