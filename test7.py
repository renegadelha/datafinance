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
    tdiv = tdiv[tdiv['margemGordon'] > -10]
    return gerarTable(tdiv, 1000)


def viewTableTop(tdiv):
    tdiv = tdiv[tdiv['margemGordon'] > 0]
    tdiv.sort_values(by=['margemGordon'], ascending=False, inplace=True)

    return gerarTable(tdiv, 1000)
    #return gerarTable(tdiv.head(int(len(tdiv) // 1.5)), 1000)


app = Dash(__name__)
server = app.server #server heroku reconhecer a app


actual_dir = pathlib.Path().absolute()

path = f'{actual_dir}/data/statusinvest-busca-avancada.csv'
data_cias = analisador.lerCsv(path)
tdiv = pd.DataFrame()
figura = None

def serve_layout():
    global tdiv
    global figura
    global data_cias

    tdiv = gerarTdiv(4, data_cias)
#    fig = px.line(figura)

    tableAll = viewTableAll(tdiv)
    tableTop = viewTableTop(tdiv)

    return html.Div(children=[
        html.Div([html.H1(children='DATA FINANCE')]
                 , className='banner'
                 )
        ,
        html.Div([html.H3(children='Top')]
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
                                        data=tableAll.to_dict('records'),
                                        columns=[{"name": i, "id": i} for i in tableAll.columns],
                                    )
                                    ])
                 )
        ,
        html.Br(),
        html.Div([html.H3(children='Top +')]
                 , className='banner1'),
        dash_table.DataTable(id='table2',
                             data=tableTop.to_dict('records'),
                             columns=[{"name": i, "id": i} for i in tableTop.columns]
                             ),

        html.Br(),
        html.Div([html.H3(children='Gráfico - Retorno % no período')]
                 , className='banner1'),
        dcc.RadioItems(
            ['diário', '30 dias', '180 dias', 'no Ano'],
            'diário',
            id='option_graph',
            inline=True
        ),
        html.Button(id='botaoGraph', n_clicks=0, children='Gerar Gráfico'),
        html.Div(id='figuradiv', children=[]),
        #html.Div(id='figuradiv', children=[dcc.Graph(figure=fig)]),

        html.Br(),
        html.Div([html.H3(children='Tweets')]
                 , className='banner1'),

        html.Div([
            dcc.Dropdown(id='tweetDropdown', options=['SIMH3','EGIE3','ALUP11','TAEE11','ENBR3','BBSE3','PSSA3','VBBR3','ITSA4','BBAS3','BRSR6','JBSS3','VIVT3','JHSF3'], multi=True)
        ]),
        html.Button(id='botaoTweets', n_clicks=0, children='Exibir Tweets'),
        html.Div(id='tweetsdiv', children=[]),

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
                  ),
                  ])
        ,

        html.Div(id='hiddendiv', children=[], style={'display': 'none'})

    ])


app.layout = serve_layout

@app.callback(
    Output('figuradiv','children'),
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


@app.callback(
    Output('hiddendiv','children'),
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
        tdiv = tdiv[tdiv['margemGordon'] > -10]
        tdiv = gerarTdiv(int(radiovalue), data_cias)

        return html.Div(['Done!'])

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

        tdiv = tdiv[tdiv['margemGordon'] > -10]
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

@app.callback(
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
        saida = str(t.day) + "/" + str(t.day) + ' - ' + str(t.hour) + ':' + str(t.minute)
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
