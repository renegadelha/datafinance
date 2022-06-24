import pandas as pd
import yfinance as yf
import numpy as np


def generateGraphMonth():

    stocks = ['brsr6.sa', 'bbas3.sa', 'VBBR3.sa', 'bbse3.sa', 'pssa3.sa', 'itsa4.sa', 'egie3.sa', 'enbr3.sa', 'alup11.sa' ]
    data = yf.download(stocks, start='2022-01-01')

    data = (data['Adj Close']/data['Adj Close'].shift() * 100 - 100).dropna()

    data = data.cumsum()

    line0 = pd.DataFrame(np.zeros((1, len(stocks))), columns=data.columns)

    data2 = pd.concat([line0, data], ignore_index=True, axis=0).dropna()

    return data2

