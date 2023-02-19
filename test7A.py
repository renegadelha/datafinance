import analisador
import datetime
import dash
import pandas as pd
import pathlib
from dash import Dash, html, dcc, dash_table, State, exceptions, callback
from dash.dependencies import Input, Output
import plotly.express as px
import graphViewer as gv
import plotly.graph_objs as go
from pages import secondPage, firstPage

import manipulatecsv

def gerarTable(tdiv, valor):
    dadosTable = analisador.distribuirAporte(tdiv.copy(), valor)
    dadosTable.reset_index(inplace=True)
    return dadosTable


def gerarTdiv(option, csv):
    return analisador.processarAnalise(csv, option)


def viewTableAll(tdiv):
    tdiv = tdiv[tdiv['margemGordon'] > -5]
    return gerarTable(tdiv, 1000)


def viewTableTop(tdiv):
    tdiv = tdiv[tdiv['margemGordon'] > 0]
    tdiv.sort_values(by=['margemGordon'], ascending=False, inplace=True)

    return gerarTable(tdiv, 1000)
    #return gerarTable(tdiv.head(int(len(tdiv) // 1.5)), 1000)


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

@callback(
    Output('hiddendiv', 'children'),
    Input('botaoSenha', 'n_clicks'),
    State('inputSenha', 'value'),
    State('option_tdiv', 'value'),
    prevent_initial_call=True

)
def update_tdiv_and_graph(n_clicks, value, radiovalue):
    global tdiv
    global figura
    global data_cias
    if value == 'rnsg':
        tdiv = tdiv[tdiv['margemGordon'] > -5]
        tdiv = gerarTdiv(int(radiovalue), data_cias)

        # manipulatecsv.testarArquivo(f'{actual_dir}/data/teste.txt')

        return html.Div(['Done!'])

    elif len(value) == 0:
        raise exceptions.PreventUpdate

@callback(
    Output('dataframe_output', 'children'),
    Input('botaoInput', 'n_clicks'),
    State('botaoValor', 'value'),
    prevent_initial_call=True

)
def update_table(n_clicks, value):
    global tdiv

    if len(value) > 0:

        tdiv = tdiv[tdiv['margemGordon'] > -5]
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

@callback(
    Output('tweetsdiv', 'children'),
    Input('botaoTweets', 'n_clicks'),
    State('tweetDropdown', 'value'),
    prevent_initial_call=True
)
def update_output2(n_clicks, value):

    tweets = analisador.capturarTweets(value)
    lista = list()
    for status in tweets:
        t = status.created_at
        saida = "dia " + str(t.day) + ' - ' + str(t.hour) + ':' + str(t.minute)
        lista.append([saida, str(status.text)])

    dataTw = pd.DataFrame(lista)
    dataTw.columns = ['Criado em', 'Tweet']

    child = html.Div([

        dash_table.DataTable(
            id='table',
            data=dataTw.to_dict('records'),
            columns=[{"name": i, "id": i} for i in dataTw.columns],
        )
    ])
    return child
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
