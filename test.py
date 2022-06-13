import analisador
import pandas as pd
import pathlib
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input,Output
import plotly.express as px

app = Dash(__name__)

actual_dir = pathlib.Path().absolute()

path = f'{actual_dir}/data/statusinvest02062022.csv'

data = analisador.lerCsv(path)

tdiv = analisador.processarAnalise(data)

dadosTable = analisador.distribuirAporte(tdiv.copy(), 1000)
dadosTable.reset_index(inplace=True)

def gerarTable(tdiv, valor):
    dadosTable = analisador.distribuirAporte(tdiv.copy(), valor)
    dadosTable.reset_index(inplace=True)

    return dadosTable



app.layout = html.Div(children=[
    html.H1(children='DATA FINANCE RENE',className='banner'),
    html.Br(),
    html.Div([
        html.H3(children='Top aportes')
#        'valor :', dcc.Input(id='botaoValor', value='digite um valor',type='number'),
#            dcc.RadioItems(
#                ['1000', '5000'],
#                '1000',
#                id='valorRadio',
#                inline=True
#            )
              ], className='banner'),

    dash_table.DataTable(id='table',
                         data = dadosTable.to_dict('records'),
                         columns= [{"name": i, "id": i} for i in dadosTable.columns]
                         )

    ])

if __name__ == '__main__':

    app.run_server(debug=True)


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
'''
