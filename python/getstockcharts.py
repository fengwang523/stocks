#!/usr/bin/python
from __future__ import division
import requests
import re
import bs4
import urllib
# -*- coding: utf-8 -*-

def get_portfolios(listfile,portfolios):
  with open(listfile) as f:
    for line in f.readlines():
      searched = re.search(r"^\s*\[\s*(\S.+?)\s*\]\s*$", line,re.M|re.I)
      if searched:
        portfolio = searched.group(1)
        portfolios[portfolio] = []
      searched  = re.search(r"^ +(\S+)\s*$", line)
      if searched:
        sym=searched.group(1)
        portfolios[portfolio].append(sym)

def get_chart(sym):
  user_agent = {'User-agent': 'Mozilla/5.0'}
  sym = sym.replace("/", "%2F")
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
  listfile = '/var/www/stocks/monitor.list';
  get_portfolios(listfile, portfolios)
  for portfolio, sym_list in portfolios.iteritems():
    print portfolio, sym_list
    for sym in sym_list:
      symbols[sym] = {}
  for sym in symbols:
    get_chart(sym)


if __name__== "__main__":
  main()

