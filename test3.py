import analisador
import pandas as pd
import pathlib
from dash import Dash, html, dcc, dash_table, State
from dash.dependencies import Input,Output
import plotly.express as px


def gerarTable(tdiv, valor):
    dadosTable = analisador.distribuirAporte(tdiv.copy(), valor)
    dadosTable.reset_index(inplace=True)

    return dadosTable



app = Dash(__name__)

actual_dir = pathlib.Path().absolute()

path = f'{actual_dir}/data/statusinvest02062022.csv'

data = analisador.lerCsv(path)

tdiv = analisador.processarAnalise(data)

#dadosTable = analisador.distribuirAporte(tdiv.copy(), 1000)
#dadosTable.reset_index(inplace=True)
padrao = gerarTable(tdiv, 1000)


app.layout = html.Div(children=[
    html.H1(children='DATA FINANCE RENE2'),
    html.Br(),
    html.Div(['valor :',
            dcc.Input(id='botaoValor', value='1234', type='text')
              ]),
            #html.Button('Submit', id='submit-val', n_clicks=0)
            #,

    html.Div(id='dataframe_output'),


    ])

@app.callback(
    Output('dataframe_output', 'children'),
    Input('botaoValor', 'value'),
    State('botaoValor', 'value')
)
def update_table(value, n_clicks):

    if(len(value)>0):

        newTable = gerarTable(tdiv, float(value))

        child = html.Div([
            dash_table.DataTable(
                id='table',
                data=newTable.to_dict('records'),
                columns=[{"name": i, "id": i} for i in newTable.columns],

            )
        ])

    else:

        child = html.Div([
            dash_table.DataTable(
                id='table',
                data=padrao.to_dict('records'),
                columns=[{"name": i, "id": i} for i in padrao.columns],

            )
        ])

    return child

if __name__ == '__main__':

    app.run_server(debug=True, port=8052)
