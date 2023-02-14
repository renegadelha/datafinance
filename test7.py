import analisador
import datetime
import dash
import pandas as pd
import pathlib
from dash import Dash, html, dcc, dash_table, State, exceptions
from dash.dependencies import Input, Output
import plotly.express as px
import graphViewer as gv
import plotly.graph_objs as go
from pages import secondPage, firstPage

import manipulatecsv

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server #server heroku reconhecer a app


def serve_layout():

    return html.Div(children=[
        html.Div([html.H1(children='DATA FINANCE')]
                 , className='banner'
                 )
        ,

        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div([
                dcc.Link('Analise|', href='/pages/firstPage'),
                dcc.Link('Teste|', href='/pages/secondPage'),
            ], className="banner2"),

        ]),

        html.Div(id='page-content', children=[]),

    ])


app.layout = serve_layout

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/secondPage':
        return secondPage.layout
    elif pathname == '/pages/firstPage':
        return firstPage.layout

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

@app.callback(
    Output('figuradiv', 'children'),
    Input('botaoGraph', 'n_clicks'),
    State('option_graph', 'value'),
    prevent_initial_call=True

)
def update_graph(n_clicks, valor):
    global tdiv
    global figura
    global data_cias
    figura = gv.generateGraphMonth(valor)

    return html.Div([dcc.Graph(figure=px.line(figura))])


'''

    actual_dir = pathlib.Path().absolute()

    path = f'{actual_dir}/data/statusinvest02062022.csv'

    data = analisador.lerCsv(path)
    tdiv = analisador.processarAnalise(data)

    print(tdiv)
    
    app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children=
        Dash: A web application framework for your data.
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

    html.Div(children=[html.H4(children=str(time))]),
'''
