#!/usr/bin/python
import requests
import re
import bs4
import pandas_datareader as web
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date, time
import getzacks
# -*- coding: utf-8 -*-

def read_sym(symbols):
  with open("symbols.txt", "r") as lines:
    for line in lines:
      mylist = []
      mylist = line.strip().split(';')
      if len(mylist) < 9:
        continue
      symbols[mylist[0]] = {}
      symbols[mylist[0]]['security'] = mylist[1]
      symbols[mylist[0]]['sector'] = mylist[2]
      symbols[mylist[0]]['industry'] = mylist[3]
      symbols[mylist[0]]['ranking'] = mylist[4]
      symbols[mylist[0]]['fwdPE'] = mylist[5]
      symbols[mylist[0]]['EPSGrowth'] = mylist[6]
      symbols[mylist[0]]['expEPSGrowth'] = mylist[7]
      symbols[mylist[0]]['dividendYield'] = mylist[8]
      symbols[mylist[0]]['beta'] = mylist[9]
      symbols[mylist[0]]['taxRate'] = mylist[10]

def main():
  symbols = {}
  read_sym(symbols)
  today = date.today()
  year = timedelta(days=365)
  yearago = today - year
  for sym, sym_dict in symbols.iteritems():
    try:
      dfquote = web.get_data_yahoo(symbols=sym, start=yearago, end=today)
    except Exception as e:
      print "Error: can't get quote for symbol : " + sym
      print "Error code: ", e.message
      continue
    try:
      security = sym_dict['security']
      sector  = sym_dict['sector']
      industry = sym_dict['industry']
      ranking = sym_dict['ranking']
      fwdPE = sym_dict['fwdPE']
      EPSGrowth= sym_dict['EPSGrowth']
      expEPSGrowth = sym_dict['expEPSGrowth']
      dividendYield  = sym_dict['dividendYield']
      beta  = sym_dict['beta']
      taxRate = sym_dict['taxRate']
    
      yearhigh = dfquote['High'].max()
      yearlow = dfquote['Low'].min()
      monthhigh = dfquote['High'][-21:-1].max()
      monthlow = dfquote['Low'][-21:-1].min()
      twoweekhigh = dfquote['High'][-10:-1].max()
      twoweeklow = dfquote['Low'][-10:-1].min()
      weekhigh =  dfquote['High'][-5:-1].max()
      weeklow =  dfquote['Low'][-5:01].min()
      pricelast = dfquote['Adj Close'][-1]
      priceday = dfquote['Adj Close'][-2]
      priceweek = dfquote['Adj Close'][-5]
      pricetwoweek = dfquote['Adj Close'][-10]
      pricemonth = dfquote['Adj Close'][-21]
      priceyear = dfquote['Adj Close'][0]
      daychange = (pricelast - priceday)/priceday
      weekchange = (pricelast - priceweek)/priceweek
      twoweekchange = (pricelast - pricetwoweek)/pricetwoweek
      monthchange = (pricelast - pricemonth)/pricemonth
      yearchange = (pricelast - priceyear)/priceyear

      dfquote['50 MA']=dfquote['Adj Close'].rolling(window=50,center=False).mean()
      MA50=dfquote['50 MA'][-1]
      dfquote['20 MA']=dfquote['Adj Close'].rolling(window=20,center=False).mean()
      MA20=dfquote['20 MA'][-1]
      dfquote['26 EMA']=dfquote['Adj Close'].ewm(ignore_na=False,span=26,min_periods=0,adjust=True).mean()
      dfquote['12 EMA']=dfquote['Adj Close'].ewm(ignore_na=False,span=12,min_periods=0,adjust=True).mean()
      dfquote['MACD'] = (dfquote['12 EMA'] - dfquote['26 EMA'])
      MACD=dfquote['MACD'][-1]
      MACD14 = dfquote['MACD'][-14]
    except Exception as e:
      print "Error: can't process pandas data for symbol : " + sym
      print "Error code: ", e.message
      continue
    if (MACD > 0):
      continue
    elif (MACD < -1):
      continue
    elif (MACD < MACD14):
      continue

    print "%s;%.2f;%.4f;%.4f;%.4f;%.4f;%.4f;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" %(sym,pricelast,daychange,weekchange,twoweekchange,monthchange,yearchange,security,sector,industry,ranking,fwdPE,EPSGrowth,expEPSGrowth,dividendYield,beta,taxRate)
  
if __name__== "__main__":
  main()

