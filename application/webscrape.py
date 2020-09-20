import bs4 as bs
from bs4 import *
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web

def gettickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text[:-1]
        tickers.append(ticker)
    print((tickers))
#gettickers()
def getdata(reload_sp500=False):
    if reload_sp500:
        tickers = gettickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(2015,1,1)
    end = dt.datetime(2020,12,31)
    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))  
        else:
            print('Already have {}'.format(ticker))
#getdata()
def getTextfornews(l):
    link = requests.get(l)
    soup = bs.BeautifulSoup(link.text, 'lxml')

    get = soup.find('ul', class_ ="My(0) Ov(h) P(0) Wow(bw)")
    new = get.findAll('h3')
    string = ''
    for x in new:
        string+=x.getText()+"\n"+"\n"
    return string
    
if __name__ == "__main__":
    li = getTextfornews('https://finance.yahoo.com/')
    print(li)
    x = 'https://finance.yahoo.com/quote/{}?p={}'.format('TSLA','TSLA')
    print(x)