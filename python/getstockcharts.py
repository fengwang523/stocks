#!/usr/bin/python
from __future__ import division
import requests
import re
import bs4
import urllib
import json
# -*- coding: utf-8 -*-

def get_portfolios(jsonfile):
  with open(jsonfile) as f:
    portfolios = json.load(f)
  return portfolios

def get_chart(sym):
  user_agent = {'User-agent': 'Mozilla/5.0'}
  if sym.count('.') >= 2:
    sym = sym.replace(".", "%2F", 1)
  url = "http://stockcharts.com/h-sc/ui?s=" + sym
  response  = requests.get(url, headers = user_agent)
  if response.status_code != 200:
    print "Error: sym", sym, "can not get chart!"
    return
  soup = bs4.BeautifulSoup(response.content, 'html.parser')
  imgurl = soup.find('img', class_="chartimg")["src"]
  if not imgurl:
    print "Error: sym", sym, "can not parse out img src!"
    return
  imgurl = 'http://stockcharts.com' + imgurl
  sym = sym.replace("$", "_")
  sym = sym.replace("%2F", ".")
  with open('/var/www/stocks/img/'+sym+'.png', "wb") as f:
    f.write(requests.get(imgurl,headers = user_agent).content)


def main():
  portfolios = {}
  symbols = {}
  jsonfile = '/var/www/stocks/monitor.json'
  portfolios = get_portfolios(jsonfile)
  print json.dumps(portfolios)
  for portfolio, sym_list in portfolios.iteritems():
    print portfolio, sym_list
    for sym in sym_list:
      symbols[sym] = {}
  for sym in symbols:
    get_chart(sym)


if __name__== "__main__":
  main()

