import pandas.core.frame

import analisador
import pathlib

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

actual_dir = pathlib.Path().absolute()
path = f'{actual_dir}/data/dados.csv'
datacsv = analisador.lerCsv(path)

tdiv = gerarTdiv(3, datacsv)

#tableAll = viewTableAll(tdiv)
tableTop = viewTableTop(tdiv)


print(tableTop)