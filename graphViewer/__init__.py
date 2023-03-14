import pandas as pd
import yfinance as yf
import numpy as np


def generateGraphMonth(tempo):

    stocks = ['brsr6.sa', 'bbas3.sa', 'VBBR3.sa', 'bbse3.sa', 'pssa3.sa', 'itsa4.sa','taee11.sa', 'egie3.sa', 'klbn11.sa', 'alup11.sa', 'vivt3.sa', 'simh3.sa' ]
    if tempo == 'diário':
        #data = yf.download(stocks, period='2d')
        data = yf.download(stocks, period="1d", interval="5m")
    elif tempo == '30 dias':
        data = yf.download(stocks, period='30d')
    elif tempo == '180 dias':
        data = yf.download(stocks, period='180d')
    else:
        data = yf.download(stocks, start='2023-01-01')

    data = (data['Adj Close']/data['Adj Close'].shift() * 100 - 100).fillna(0)

    data = data.cumsum()

    return data



