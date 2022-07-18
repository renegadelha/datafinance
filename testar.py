import pandas.core.frame
import yfinance as yf
import plotly.express as px
import analisador
import numpy as np
import pathlib
import pandas as pd

def gerarTable(tdiv, valor):
    dadosTable = analisador.distribuirAporte(tdiv.copy(), valor)
    dadosTable.reset_index(inplace=True)

    return dadosTable


def gerarTdiv(option, csv):
    return analisador.processarAnalise(csv, option)


def viewTableTop(tdiv: pandas.core.frame.DataFrame):
    tdiv.sort_values(by=['margemGordon'], ascending=False, inplace=True)

    return gerarTable(tdiv.head(len(tdiv) // 2), 1000)


def viewTableAll(tdiv):
    return gerarTable(tdiv, 1000)
'''
actual_dir = pathlib.Path().absolute()
path = f'{actual_dir}/data/dados.csv'
datacsv = analisador.lerCsv(path)

tdiv = gerarTdiv(3, datacsv)

#tableAll = viewTableAll(tdiv)
tableTop = viewTableTop(tdiv)

'''

stocks = ['brsr6.sa', 'bbas3.sa', 'VBBR3.sa', 'bbse3.sa', 'pssa3.sa', 'itsa4.sa', 'egie3.sa', 'enbr3.sa', 'alup11.sa']
data = yf.download(stocks, period='30d')

data = (data['Adj Close'] / data['Adj Close'].shift() * 100 - 100).fillna(0) #.dropna()

data = data.cumsum()

print(data.columns)

fig = px.line(data)
fig.show()

