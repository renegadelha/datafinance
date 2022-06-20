import pandas as pd
import numpy as np
import yfinance as yf
import math
from sklearn.linear_model import LinearRegression


def computAporte(tdiv, priorizarTopo, valorAporte, rebuild):
    if (not rebuild):
        tdiv = tdiv.set_index('stock')

    tdiv['notaMedia'] = 0
    tdiv['valorAporte'] = 0

    for i in tdiv.index:

        nota = 0
        if tdiv.loc[i, 'pontos'] == tdiv.describe()['pontos'][3]:
            nota = nota + 0
        if tdiv.loc[i, 'pontos'] <= tdiv.describe()['pontos'][4]:
            nota = nota + 3
        elif tdiv.loc[i, 'pontos'] <= tdiv.describe()['pontos'][5]:
            nota = nota + 2
        elif tdiv.loc[i, 'pontos'] <= tdiv.describe()['pontos'][6]:
            nota = nota + 1
        else:
            nota = nota + 0

        if tdiv.loc[i, 'margemGordon'] == tdiv.describe()['margemGordon'][7]:
            nota = nota + 0
        if tdiv.loc[i, 'margemGordon'] >= tdiv.describe()['margemGordon'][6]:
            nota = nota + 7
        elif tdiv.loc[i, 'margemGordon'] >= tdiv.describe()['margemGordon'][5]:
            nota = nota + 5
        elif tdiv.loc[i, 'margemGordon'] >= tdiv.describe()['margemGordon'][4]:
            nota = nota + 3
        else:
            nota = nota + 0

        #        if tdiv.loc[i, 'margemGraham'] == tdiv.describe()['margemGraham'][7]:
        #            nota = nota + 0
        #        if tdiv.loc[i, 'margemGraham'] >= tdiv.describe()['margemGraham'][6]:
        #            nota = nota + 1.5
        #        elif tdiv.loc[i, 'margemGraham'] >= tdiv.describe()['margemGraham'][5]:
        #            nota = nota + 1.5
        #        elif tdiv.loc[i, 'margemGraham'] >= tdiv.describe()['margemGraham'][4]:
        #            nota = nota + 1
        #        else:
        #            nota = nota + 1

        tdiv.loc[i, 'notaMedia'] = nota

    tdiv.drop(tdiv[tdiv['notaMedia'] < priorizarTopo].index, inplace=True)

    for i in tdiv.index:
        tdiv.loc[i, 'valorAporte'] = float(
            "{0:.2f}".format((tdiv.loc[i, 'notaMedia'] / tdiv['notaMedia'].sum()) * valorAporte))

    return tdiv


def dyanalise(name):
    empresa = name + '.SA'
    comp = yf.Ticker(empresa)
    hist2 = comp.history(start='2017-01-01', end='2021-12-30')
    if (len(hist2) == 0):
        return 0
    somaDiv = hist2['Dividends'].resample('Y').sum()
    meanPrice = hist2['Close'].resample('Y').mean()
    volatil = somaDiv.std() / somaDiv.mean()
    result = somaDiv / meanPrice * 100

    return [name, float("{0:.2f}".format(volatil)), float("{0:.2f}".format(somaDiv.median())),
            float("{0:.2f}".format(result.median())), float("{0:.2f}".format(result.mean()))]


def calcularCoefAngDiv(name):
    empresa = name + '.SA'
    comp = yf.Ticker(empresa)
    hist2 = comp.history(start='2016-01-01', end='2021-12-30')
    somaDiv = hist2['Dividends'].resample('Y').sum()
    pdanos = pd.DataFrame([*range(1, len(somaDiv) + 1)])
    linearReg = LinearRegression()
    linearReg.fit(pdanos, pd.DataFrame(somaDiv.values))

    return float("{0:.2f}".format(linearReg.coef_[0][0]))


def calcularDividendos(dados):
    dataf = []
    for empresa in dados['TICKER']:
        data = dyanalise(empresa)
        if (data != 0):
            data.append(calcularCoefAngDiv(empresa))
            dataf.append(data)

    df = pd.DataFrame(np.array(dataf), columns=['stock', 'volDIV', 'valueDiv', 'medianDIV', 'meanDIV', 'crescDiv'])
    df = df.astype(
        {"stock": str, "volDIV": float, "valueDiv": float, "medianDIV": float, "meanDIV": float, "crescDiv": float})

    df = df.sort_values(by=['medianDIV'], ascending=False)
    df = df.reset_index()
    df = df.drop(columns=['index'])
    return df


def getValue(ticket, dti, dtf, fun):
    if (dtf == 0):
        hist = yf.download(ticket, start=dti)
    else:
        hist = yf.download(ticket, start=dti, end=dtf)

    if (len(hist) == 0):
        return 0

    if (fun == 'min'):
        cotac = hist['Adj Close']
        cotac = pd.DataFrame(cotac)
        dataMenorCot = cotac[cotac['Adj Close'] == cotac['Adj Close'].min()].index[0].date().strftime("%Y-%m-%d")
        return [hist['Adj Close'].min(), dataMenorCot]
    elif (fun == 'max'):
        return hist['Adj Close'].max()
    elif (fun == 'last'):
        lastPrice = hist['Adj Close'][-1]
        if pd.isna(lastPrice):
            lastPrice = hist['Adj Close'][-2]
        return lastPrice


def evolut(name):
    name = name + '.SA'
    cotPre = getValue(name, '2020-01-01', '2020-05-01', 'max')
    if (cotPre == 0):
        hist11 = yf.download(name)
        if len(hist11) == 0:
            return 0
        else:
            return (hist11.iloc[-1]['Adj Close'] - hist11.iloc[0]['Adj Close']) / hist11.iloc[0]['Adj Close'] * 100

    saida = getValue(name, '2020-01-01', '2020-12-01', 'min')
    cotFun = saida[0]
    topoPos = getValue(name, saida[1], 0, 'max')
    atual = getValue(name, '2020-05-01', 0, 'last')

    recuperou = (atual / cotPre) * 100
    encoraj = 1 - (((topoPos - cotFun) - (topoPos - atual)) / (topoPos - cotFun))
    media = (recuperou + ((1 - encoraj) * 100)) / 2
    # print(f"{atual} - {cotPre} - {cotFun} - {topoPos} - {saida[1]} - {recuperou} - {encoraj} - {media}")

    return media


def calcularMagicFormulaRene(dados):
    empresas = dados.TICKER.values

    for nome in empresas:
        print(nome)
        dados.loc[(dados.TICKER == nome), 'media'] = float("{0:.2f}".format(evolut(nome)))

    dados4 = dados.replace(np.nan, 0)
    dados4.drop(dados4[dados4['media'] == 0].index, inplace=True)

    ranks = {}
    for name in dados4.TICKER:
        ranks[name] = 0

    dados4 = dados4.sort_values(by=['ROE'], ascending=False)
    i = 1
    for name in dados4.TICKER:
        i = i * 1.25
        ranks[name] = ranks[name] + int(i)

    #    dados4 = dados4.sort_values(by=['ROIC'], ascending=False)
    #    i = 0
    #    for name in dados4.TICKER:
    #        i = i + 1
    #        ranks[name] = ranks[name] + int(1 / (0.1 + math.exp(-j+5)))

    dados4 = dados4.sort_values(by=['EV/EBIT'])
    i = 1
    for name in dados4.TICKER:
        i = i * 1.25
        ranks[name] = ranks[name] + int(i)

    dados4 = dados4.sort_values(by=['media'])
    i = 1
    for name in dados4.TICKER:
        ranks[name] = ranks[name] + int(i)
        i = i * 1.2

    final = pd.DataFrame.from_dict({'stock': ranks.keys(), 'pontos': ranks.values()})
    final = final.sort_values(by=['pontos'])
    final = final.reset_index()
    final = final.drop(columns=['index'])

    return final


def modeloGordon(dados):
    gordon = []

    for name in dados.TICKER:

        empresa = name + '.SA'
        comp = yf.Ticker(empresa)
        hist2 = comp.history(start='2016-01-01', end='2021-12-30')
        hist = comp.history()

        if (len(hist2) != 0):
            somaDiv = hist2['Dividends'].resample('Y').sum()
            gordonPrice = somaDiv.median() / 0.06

            lastPrice = hist['Close'][-1]
            if pd.isna(lastPrice):
                lastPrice = hist['Close'][-2]

            difGordon = (gordonPrice - lastPrice) / lastPrice * 100

            gordon.append([name, float("{0:.2f}".format(difGordon))])

    dadoGordon = pd.DataFrame(gordon, columns=['stock', 'margemGordon'])
    return dadoGordon


def modeloGordonMyStocks(dados):
    gordon = []

    for name in dados.keys():

        empresa = name + '.SA'
        comp = yf.Ticker(empresa)
        hist2 = comp.history(period="1y")

        if (len(hist2) != 0):
            gordonPrice = dados.get(name) / 0.06
            lastPrice = hist2['Close'][-1]

            if pd.isna(lastPrice):
                lastPrice = hist2['Close'][-2]

            difGordon = (gordonPrice - lastPrice) / lastPrice * 100

            gordon.append([name, float("{0:.2f}".format(difGordon))])

    dadoGordon = pd.DataFrame(gordon, columns=['stock', 'margemGordon'])
    return dadoGordon


def modeloGraham(dados):
    tabela = []

    for i in range(0, len(dados)):
        empresa = dados.iloc[i]['TICKER'] + '.SA'
        comp = yf.Ticker(empresa)
        hist2 = comp.history(period="5d")

        if (len(hist2) != 0):
            lastPrice = hist2['Close'][-1]
            if pd.isna(lastPrice):
                lastPrice = hist2['Close'][-2]

            # print('{} - {}'.format(dados.iloc[i]['TICKER'], lastPrice))
            grahamPrice = math.sqrt(dados.iloc[i][' VPA'] * dados.iloc[i][' LPA'] * 22.5)
            difGraham = (grahamPrice - lastPrice) / lastPrice * 100
            tabela.append([dados.iloc[i]['TICKER'], float("{0:.2f}".format(difGraham))])

    dadoGraham = pd.DataFrame(tabela, columns=['stock', 'margemGraham'])
    return dadoGraham


def isOld(dados):
    acoesInclusas = []

    for ticket in dados['TICKER']:
        ret = yf.download(ticket + '.sa', start='2020-01-01', end='2020-01-30')
        if (len(ret) > 0):
            acoesInclusas.append(ticket)

    return dados[dados.TICKER.isin(acoesInclusas)]


def ticketsMaiorLiquidez(dados):
    tickets = dados['TICKER']

    ticketsNoNumber = set()
    for emp in tickets:
        ticketsNoNumber.add(emp[0:4])

    ticketsMaisLiquidos = []
    for j in ticketsNoNumber:
        ticketsMaisLiquidos.append(
            dados[dados['TICKER'].str.contains(j)].sort_values(by=[' LIQUIDEZ MEDIA DIARIA'], ascending=False)[
                'TICKER'].iloc[0])

    return ticketsMaisLiquidos


def teste():
    return 2

def lerCsv(path):
    dados = pd.read_csv(path, decimal=",", delimiter=";", thousands=".")
    dados = dados.fillna(0)

    return dados


def processarAnalise(dados, option):

    myStocks = True

    if option ==1:
        empresasdiv = {'VBBR3': 1.3, 'BBSE3': 1.7, 'PSSA3': 1.3}
    elif option == 2:
        empresasdiv = {'VBBR3': 1.3, 'BBSE3': 1.7, 'PSSA3': 1.3, 'BRSR6': 0.7,
                       'BBAS3': 2.2, 'ITSA4': 0.6}
    elif option == 3:
        empresasdiv = {'VBBR3': 1.3, 'BBSE3': 1.7, 'PSSA3': 1.3, 'BRSR6': 0.7,
                       'BBAS3': 2.2, 'ITSA4': 0.6, 'EGIE3': 2.5, 'ENBR3': 1.3, 'ALUP11': 1.5}
    else:
        empresasdiv = {'VBBR3': 1.3, 'BBSE3': 1.7, 'PSSA3': 1.3}

    dados3 = dados[dados.TICKER.isin(list(empresasdiv.keys()))]

    if not myStocks:
        filtrados = ticketsMaiorLiquidez(dados3)
        dados3 = dados3[dados.TICKER.isin(filtrados)]

    if not myStocks:
        dados3 = isOld(dados3)

    magdata = calcularMagicFormulaRene(dados3)

    divdata = calcularDividendos(dados3)

    # grahamdata = modeloGraham(dados3)

    if (myStocks):
        gordondata = modeloGordonMyStocks(empresasdiv)
    #    gordondata = modeloGordon(dados3)
    else:
        gordondata = modeloGordon(dados3)

    tmag = magdata
    tdiv = divdata
    tgordon = gordondata
    # tgraham = grahamdata

    tdiv = tdiv.merge(tmag, how='left', on='stock')
    tdiv = tdiv.merge(tgordon, how='left', on='stock')
    # tdiv = tdiv.merge(grahamdata, how='left', on='stock')

    if not myStocks:
        tdiv = tdiv.dropna()
        tdiv = tdiv[tdiv['medianDIV'] < 15]
        tdiv = tdiv[tdiv['volDIV'] < 1]


    return tdiv

def distribuirAporte(tdiv, valoraporte):

    tdiv = computAporte(tdiv, 0, valoraporte, False)
    tdiv.sort_values(by=['notaMedia', 'medianDIV'], ascending=False, inplace=True)

    return tdiv
