import analisador
import datetime
import pandas as pd
import pathlib
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import graphViewer as gv
import plotly.graph_objs as go


def gerarTable(tdiv, valor):
    dadosTable = analisador.distribuirAporte(tdiv.copy(), valor)
    dadosTable.reset_index(inplace=True)

    return dadosTable


def gerarTdiv():
    data = analisador.lerCsv(path)

    return analisador.processarAnalise(data)


def viewTableAll(tdiv):
    return gerarTable(tdiv, 1000)


def viewTableTop(tdiv):
    tdiv2 = tdiv.head(len(tdiv) // 2)

    return gerarTable(tdiv2, 1000)


app = Dash(__name__)

actual_dir = pathlib.Path().absolute()

path = f'{actual_dir}/data/statusinvest02062022.csv'


def serve_layout():
    fig = px.line(gv.generateGraphMonth())

    tdiv = gerarTdiv()
    tableAll = viewTableAll(tdiv)
    tableTop = viewTableTop(tdiv)

    return html.Div(children=[
        html.Div([html.H1(children='DATA FINANCE')]
                 , className='banner'

                 )
        ,

        html.Div([html.H3(children='Top {}'.format(len(tableAll)))]
                 , className='banner1'),

        dash_table.DataTable(id='table',
                             data=tableAll.to_dict('records'),
                             columns=[{"name": i, "id": i} for i in tableAll.columns]
                             ),
        html.Br(),
        html.Div([html.H3(children='Top {}'.format(len(tableTop)))]
                 , className='banner1'),

        dash_table.DataTable(id='table2',
                             data=tableTop.to_dict('records'),
                             columns=[{"name": i, "id": i} for i in tableTop.columns]
                             ),
        html.Br(),
        html.Div([html.H3(children='Gráfico - Cotações nos últimos 30 dias')]
                 , className='banner1'),

        dcc.Graph(figure=fig)

    ])


app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

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

        html.H2(children=str(datetime.datetime.now())),
'''
