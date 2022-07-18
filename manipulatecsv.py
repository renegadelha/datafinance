import time

import pandas as pd
import yfinance as yf
import pathlib
import analisador


def isOld(dados):
    acoesInclusas = []

    for ticker in dados['TICKER']:
        if len(yf.Ticker(ticker + '.sa').history()) > 0:
            acoesInclusas.append(ticker)

    return dados[dados.TICKER.isin(acoesInclusas)]


def verifcsv():
    actual_dir = pathlib.Path().absolute()
    #dados = pd.read_csv(f'{actual_dir}/data/dados.csv')
    datacsv = analisador.lerCsv(f'{actual_dir}/data/dados.csv')
    tdiv = analisador.processarAnalise(datacsv, 3 )
    print(tdiv)


def criarcsv():
    actual_dir = pathlib.Path().absolute()

    path = f'{actual_dir}/data/statusinvest-busca-avancada.csv'
    dados = pd.read_csv(path, decimal=",", delimiter=";", thousands=".")
    dados = dados.fillna(0)
    dados.drop(dados[dados[' LIQUIDEZ MEDIA DIARIA'] < 500000].index, inplace=True)
    dados.drop(dados[dados['PRECO'] <= 0].index, inplace=True)
    dados = isOld(dados)

    dados.to_csv(f'{actual_dir}/data/dados.csv', index=False)
    print("terminei")


def gerarPickel():
    actual_dir = pathlib.Path().absolute()

    path = f'{actual_dir}/data/statusinvest-busca-avancada.csv'
    dados = pd.read_csv(path, decimal=",", delimiter=";", thousands=".")
    dados = dados.fillna(0)
    dados.drop(dados[dados[' LIQUIDEZ MEDIA DIARIA'] < 500000].index, inplace=True)
    dados.drop(dados[dados['PRECO'] <= 0].index, inplace=True)
    dados = isOld(dados)

    dados.to_pickle(f'{actual_dir}/data/dados.pkl')
    print("terminei pkl")

if __name__ == '__main__':
    init = time.time()
    actual_dir = pathlib.Path().absolute()
    path = f'{actual_dir}/data/dados.pkl'
    data = analisador.lerpickel(path)
    gastou = time.time() - init
    print(gastou)