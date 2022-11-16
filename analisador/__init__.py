import pandas as pd
import numpy as np
import yfinance as yf
import math
from sklearn.linear_model import LinearRegression
import tweepy as tw



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


def calcularMagicFormulaRene(dados):
    dados4 = dados.replace(np.nan, 0)

    ranks = dict(zip(list(dados4.TICKER), [0] * len(dados4)))
#    for name in dados4.TICKER:
#        ranks[name] = 0

    dados4 = dados4.sort_values(by=['ROE'], ascending=False)
    i = 1
    for name in dados4.TICKER:
        i = i + 1
        ranks[name] = ranks[name] + i

    dados4 = dados4.sort_values(by=['MARGEM EBIT'], ascending=False)
    i = 0
    for name in dados4.TICKER:
        i = i + 1
        ranks[name] = ranks[name] + i

    dados4 = dados4.sort_values(by=['EV/EBIT'])
    i = 1
    for name in dados4.TICKER:
        i = i + 1
        ranks[name] = ranks[name] + i

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

            difGordon = (gordonPrice - lastPrice) / gordonPrice * 100

            gordon.append([name, float("{0:.2f}".format(difGordon))])

    dadoGordon = pd.DataFrame(gordon, columns=['stock', 'margemGordon'])
    return dadoGordon


def modeloGordonMyStocks(dados):
    gordon = []

    for name in dados.keys():

        empresa = name + '.SA'
        comp = yf.Ticker(empresa)
        hist2 = comp.history()

        gordonPrice = dados.get(name) / 0.06
        lastPrice = hist2['Close'][-1]

        if pd.isna(lastPrice):
            lastPrice = hist2['Close'][-2]

        difGordon = (gordonPrice - lastPrice) / gordonPrice * 100

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

    for ticker in dados['TICKER']:
        if len(yf.Ticker(ticker + '.sa').history()) > 0:
            acoesInclusas.append(ticker)

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


def lerCsv(path):
    dados = pd.read_csv(path, decimal=",", delimiter=";", thousands=".")
    #
    return dados

def lerpickel(path):
    return pd.read_pickle(path)


def processarAnalise(dados, option):

    myStocks = True

    if option == 1:
        empresasdiv = {'VBBR3': 1.2, 'BBSE3': 1.7}
    elif option == 2:
        empresasdiv = {'VBBR3': 1.2, 'BBSE3': 1.7, 'BRSR6': 0.7,
                       'BBAS3': 2.2, 'ITSA4': 0.5}
    elif option == 3:
        empresasdiv = {'VBBR3': 1.2, 'BBSE3': 1.7, 'PSSA3': 1.1, 'BRSR6': 0.7,
                       'BBAS3': 2.2, 'ITSA4': 0.5, 'EGIE3': 2.3, 'ENBR3': 1.3, 'ALUP11': 1.6, 'TAEE11': 2.1}
    elif option == 4:
        empresasdiv = {'VBBR3': 1.2, 'BBSE3': 1.7, 'PSSA3': 1.1, 'BRSR6': 0.7,
                       'BBAS3': 2.2, 'ITSA4': 0.5, 'EGIE3': 2.3, 'ENBR3': 1.3, 'ALUP11': 1.6, 'TAEE11': 2.1,
                       'VIVT3': 2.7, 'VALE3': 3.8, 'SIMH3': 0.5}
    else:
        empresasdiv = {'VBBR3': 1.3, 'BBSE3': 1.7, 'PSSA3': 1.3}

    dados3 = dados[dados.TICKER.isin(list(empresasdiv.keys()))].copy()
    dados3.loc[dados3['MARGEM EBIT'] == 0, 'MARGEM EBIT'] = dados3['MARGEM EBIT'].median()

    magdata = calcularMagicFormulaRene(dados3)

#    divdata = calcularDividendos(dados3)

    # grahamdata = modeloGraham(dados3)

    if (myStocks):
        gordondata = modeloGordonMyStocks(empresasdiv)
    #    gordondata = modeloGordon(dados3)
    else:
        gordondata = modeloGordon(dados3)

    tmag = magdata
    #tdiv = divdata
    tgordon = gordondata
    # tgraham = grahamdata

    #tdiv = tdiv.merge(tmag, how='left', on='stock')
    #tdiv = tdiv.merge(grahamdata, how='left', on='stock')

    tmag = tmag.merge(tgordon, how='left', on='stock')

    return tmag


def distribuirAporte(tdiv, valoraporte):

    tdiv = computAporte(tdiv, 0, valoraporte, False)
    tdiv.sort_values(by=['notaMedia'], ascending=False, inplace=True)

    return tdiv

def capturarTweets(stocks):
    auth = tw.OAuthHandler('jXPLVPJ66fGJizGijEfnEg', 'gynr3QHMVoQLuvc5zX2nZzmIPRg97qJkSUlYhmxQOE')
    auth.set_access_token('206698741-uA2PhwtLD1RT3aa9iXjZlxxjKMmg3HbgFYAQleTl',
                          'PCkJYQmL2YlN8CK449zIevBb56Oiu17TAhycqXaLwhtw8')

    api = tw.API(auth, wait_on_rate_limit=True)

    busca = str(stocks[0])
    for n in range(1, len(stocks)):
        busca = busca + ' OR ' + str(stocks[n])

    tweets = tw.Cursor(api.search_tweets, q=busca, lang="pt").items(50)

    return tweets