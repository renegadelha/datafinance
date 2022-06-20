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


def gerarTdiv(option, csv):
    return analisador.processarAnalise(csv, option)


def viewTableAll(tdiv):
    return gerarTable(tdiv, 1000)


def viewTableTop(tdiv):
    tdiv2 = tdiv.head(len(tdiv) // 2)

    return gerarTable(tdiv2, 1000)


app = Dash(__name__)
server = app.server #server heroku reconhecer a app


actual_dir = pathlib.Path().absolute()

path = f'{actual_dir}/data/dados.csv'
datacsv = analisador.lerCsv(path)
tdiv = pd.DataFrame()
padrao = pd.DataFrame()
figura = gv.generateGraphMonth()

def serve_layout():
    global tdiv
    global padrao
    global figura
    global datacsv

    tdiv = gerarTdiv(3, datacsv)
    padrao = viewTableAll(tdiv)
    fig = px.line(figura)

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
        html.Div(id='figuradiv', children=[dcc.Graph(figure=fig)]),

        html.Div([html.H3(children='Admin')]
                 , className='banner1'),
        html.Div(['Senha:',
                  dcc.Input(id='inputSenha', value='******', type='password'),
                  html.Button(id='botaoSenha', n_clicks=0, children='Atualizar Dados')
                  ,
                  html.Br(),
                  dcc.RadioItems(
                      ['1', '2', '3', '4'],
                      '1',
                      id='option_tdiv',
                      inline=True
                  )
                  ])

        ,

        html.Div(id='hiddendiv', style={'display': 'none'})

    ])


app.layout = serve_layout

@app.callback(
    Output('figuradiv','children'),
    Input('botaoSenha', 'n_clicks'),
    State('inputSenha', 'value'),
    State('option_tdiv', 'value'),
    prevent_initial_call=True

)
def update_tdiv_and_graph(n_clicks, value, radiovalue):
    global tdiv
    global figura
    global datacsv
    if value == 'rnsg':
        tdiv = gerarTdiv(int(radiovalue), datacsv)
        figura = gv.generateGraphMonth()

        return html.Div([dcc.Graph(figure=px.line(figura))])

    elif len(value) == 0:
        raise exceptions.PreventUpdate


@app.callback(
    Output('dataframe_output', 'children'),
    Input('botaoInput', 'n_clicks'),
    State('botaoValor', 'value'),
    prevent_initial_call=True

)
def update_table(n_clicks, value):
    global tdiv

    if len(value) > 0:
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

    html.Div(children=[html.H4(children=str(time))]),
'''
