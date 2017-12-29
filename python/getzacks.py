#!/usr/bin/python
from __future__ import division
import codecs
import sys
import requests
import re
import bs4
# -*- coding: utf-8 -*-

def get_zacks(sym):
  url="https://www.zacks.com/stock/quote/" + sym
  search = "(1-Strong Buy|2-Buy|3-Hold|4-Sell|5-Strong Sell)"
  try:
    response = requests.get (url)
  except Exception as e:
    print url, "requests error!"
    print e.message
    return ['error']
  if (response.status_code==200):
    pass
  else:
    print "symbol:", sym, url, "response.status_code=", response.status_code
    return ['error']
  result = re.search (search, response.content)
  if result:
    Ranking=result.group(0)
  else:
    Ranking="null"
  soup = bs4.BeautifulSoup(response.content, 'html.parser')
  #find "Key Earnings Data" table
  earningstable=soup.find('section', id="stock_key_earnings").select('table')[0]
  ExpEPSGrowth =earningstable.select('tr')[6].select('td')[0].text
  searchObj = re.search(r'\)\s*(\S+?%)', ExpEPSGrowth)
  if searchObj:
    ExpEPSGrowth = searchObj.group(1)
  else:
    ExpEPSGrowth = 'null'
  ForwardPE =earningstable.select('tr')[7].select('td')[1].text
  activitytable=soup.find('section', id="stock_activity").select('table')[0]
  DividendYield=activitytable.select('tr')[7].select('td')[1].text
  searchObj = re.search(r'\(\s*(\S+)\s*\)', DividendYield)
  if searchObj:
    DividendYield = searchObj.group(1)
  else:
    DividendYield = 'null'
  Beta=activitytable.select('tr')[8].select('td')[1].text

  sectortd=soup.find('table', class_="abut_top").select('tr')[0].select('td')[0]
  sector='null'
  industry='null'
  sector=sectortd.select('a')[0].text
  industry=sectortd.select('a')[1].text

  url="https://www.zacks.com/stock/quote/" + sym + "/income-statement"
  try:
    response = requests.get (url)
  except Exception as e:
    print url, "requests error!"
    print e.message
    return ['error']
  soup = bs4.BeautifulSoup(response.content, 'html.parser')
  incometable=soup.find('section', id="income_statements_tabs").select('table')[0]
  pretaxIncome=incometable.select('tr')[8]
  pretaxIncomeLast1=pretaxIncome.select('td')[1].text
  pretaxIncomeLast2=pretaxIncome.select('td')[2].text
  pretaxIncomeLast3=pretaxIncome.select('td')[3].text
  incomeTax=incometable.select('tr')[9]
  incomeTaxLast1=incomeTax.select('td')[1].text
  incomeTaxLast2=incomeTax.select('td')[2].text
  incomeTaxLast3=incomeTax.select('td')[3].text

  EPStable=soup.find('section', id="income_statements_tabs").select('table')[2]
  dilutedEPS=EPStable.select('tr')[-1]
  dilutedEPSLast1=dilutedEPS.select('td')[1].text
  dilutedEPSLast2=dilutedEPS.select('td')[2].text
  dilutedEPSLast3=dilutedEPS.select('td')[3].text
  try:
    tax1=int(incomeTaxLast1.replace(',','')) 
    tax2=int(incomeTaxLast2.replace(',',''))
    tax3=int(incomeTaxLast3.replace(',',''))
    income1=int(pretaxIncomeLast1.replace(',',''))
    income2=int(pretaxIncomeLast2.replace(',',''))
    income3=int(pretaxIncomeLast3.replace(',',''))
    incometax=(tax1+tax2+tax3)/(income1+income2+income3)
    incometax='{:.2%}'.format(incometax)
  except Exception as e:
    incometax='null'
    print sym, "get incometax error:", e.message
  try:
    dilutedEPSLast1=float(dilutedEPSLast1)
    dilutedEPSLast2=float(dilutedEPSLast2)
    dilutedEPSLast3=float(dilutedEPSLast3)
    EPSGrowth12=(dilutedEPSLast1-dilutedEPSLast2)/dilutedEPSLast2
    EPSGrowth23=(dilutedEPSLast2-dilutedEPSLast3)/dilutedEPSLast3
    EPSGrowth=(EPSGrowth12+EPSGrowth23)/2
    EPSGrowth='{:.2%}'.format(EPSGrowth)
  except Exception as e:
    EPSGrowth='null'
    print sym, "get EPS  error:", e.message


  return [sector, industry, Ranking, ForwardPE, EPSGrowth, ExpEPSGrowth, DividendYield, Beta, incometax]
         

def get_sp500_sym(symbols):
  url="http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
  try:
    response = requests.get(url)
  except Exception as e:
    print url, "requests error!"
    print e.message
    return ['error']
  if (response.status_code==200):
    pass
  else:
    print url, "response.status_code=", response.status_code
    return ['error']

  soup = bs4.BeautifulSoup(response.content, 'html.parser')
  symbolslist = soup.select('table')[0].select('tr')[1:]
  for i, symbol in enumerate(symbolslist, 1):
    tds = symbol.select('td')
    symbols[tds[0].select('a')[0].text] = {}
    symbols[tds[0].select('a')[0].text]['security'] = tds[1].select('a')[0].text

def get_qqq_sym(symbols):
  url="https://en.wikipedia.org/wiki/NASDAQ-100"
  try:
    response = requests.get(url)
  except Exception as e:
    print url, "requests error!"
    print e.message
    return ['error']
  if (response.status_code==200):
    pass
  else:
    print url, "response.status_code=", response.status_code
    return ['error']

  soup = bs4.BeautifulSoup(response.content, 'html.parser')
  symbolslist = soup.find('div', class_="div-col columns column-count column-count-2").select('ol')[0].select('li')[0:]
  for i, symbol in enumerate(symbolslist, 1):
    string = symbol.text
    search = re.search("(\s*\S.+?)\s*\((.+?)\)",string)
    if search:
      symbols[search.group(2)] = {}
      symbols[search.group(2)]['security'] = search.group(1)

def main():
  symbols = {}
  get_sp500_sym(symbols)
  get_qqq_sym(symbols)
  fh=open('symbols.txt', 'w')
  for sym, sym_dict in symbols.iteritems():
    data=[]
    data = get_zacks(sym)
    datastr = ";".join(data)
    try:
      print sym + ";" + sym_dict['security'].encode('utf-8') + ";" + datastr
      fh.write(sym + ";" + sym_dict['security'].encode('utf-8') + ";" + datastr + "\n")
    except Exception as e:
      print "Error for symbal:", sym
      print e.message
      continue
  fh.close()
  
if __name__== "__main__":
  main()

