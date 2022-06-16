import analisador
import datetime
import pandas as pd
import pathlib
from dash import Dash, html, dcc, dash_table, State, exceptions
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
server = app.server #server heroku reconhecer a app



actual_dir = pathlib.Path().absolute()

path = f'{actual_dir}/data/statusinvest02062022.csv'
tdiv = gerarTdiv()
padrao = pd.DataFrame()
padrao2 = pd.DataFrame()

def serve_layout():
    global tdiv
    global padrao
    global padrao2

    padrao = viewTableAll(tdiv)
    fig = px.line(gv.generateGraphMonth())

    tableAll = viewTableAll(tdiv)
    tableTop = viewTableTop(tdiv)

    return html.Div(children=[
        html.Div([html.H1(children='DATA FINANCE')]
                 , className='banner'

                 )
        ,
        html.Div([html.H3(children='Top {}'.format(len(tableAll)))]
                 , className='banner1'),
        html.Div(['valor do Aporte:',
                  dcc.Input(id='botaoValor', value='1000', type='text'),
                  html.Button(id='botaoInput', n_clicks=0, children='Atualizar')
                  ])
        ,

        html.Div(id='dataframe_output',
                 children=html.Div([
            dash_table.DataTable(
                id='table',
                data=padrao.to_dict('records'),
                columns=[{"name": i, "id": i} for i in padrao.columns],

            )
        ])
                 )
        ,

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


@app.callback(
    Output('dataframe_output', 'children'),
    Input('botaoInput', 'n_clicks'),
    State('botaoValor', 'value'),
    prevent_initial_call=True

)
def update_table(n_clicks, value):
    global tdiv

    if len(value) > 0:
        tdiv = gerarTdiv()
        newtable = gerarTable(tdiv, float(value))
        child = html.Div([
            dash_table.DataTable(
                id='table',
                data=newtable.to_dict('records'),
                columns=[{"name": i, "id": i} for i in newtable.columns],

            )
        ])
        return child

    elif len(value) == 0:

        raise exceptions.PreventUpdate



if __name__ == '__main__':
    app.run_server(debug=True, port=8054)

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
