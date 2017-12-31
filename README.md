# Objective

  learning python, javascript, ajax via this stocks monitoring mini project

# directories and scripts

  python/			#dir for python back scripts

  python/getzacks.py		#get sp500 and qqq100 symblo lists

				#then get zacks.com stock data

				#output data to file symbols.txt in html www directory

  python/getstockquotes.py	#get stock history quotes from yahoo

				#filter out stocks with MACD stragegy

				#update Movers symbols to monitor.json in html www directory

  python/getstockcharts.py	#read monitor.json, and get charts from stockcharts.com

  www/				#dir for html files

  www/index.html		#main html file to display stock portfolios

  www/ajaxstock.php		#index.html has ajaxcall to ajaxstock.php

				#ajaxstock.php returns stock data from symbols.txt

  www/monitor.json		#stock portfolios to monitor

				#"Movers" portfolio is udpated by python/getstockcharts.py script

# initial setup

  1. copy files www/* to /var/www/stocks/

    #if you www director is not /var/www/stocks/, then all python scripts need to modify souce code to reference the correct director

  2. create /var/www/stocks/img dir

  3. put files pythoan/* to another directory 

  4. install required python modules: bs4, pandas, numpy

  5. modify /var/www/stocks/monitor.json for stock portfolios to monitor

  6. run python/getzacks.py to popolate /var/www/stocks/symbols.txt file

  7. run python/getstockquotes.py to populate /var/www/stocks/monitor.json file for "Movers" portfolio

    #this step is optional, if you don't want to use the MACD filter strategy

  8. run python/getstockcharts.py to pull charts from stockcharts.com
 
  9. open 127.0.0.1/stocks/ to monitor stock charts

# day to day usage

  1. modify /var/www/stocks/monitor.json to add/delete stocks from portfolios

  2. run python/getstockquotes.py to modify /var/www/stocks/monitor.json file for "Movers" portfolio

    #this is optional

  3. run python/getstockcharts.py to pull charts from stockcharts.com

  4. open 127.0.0.1/stocks/ to monitor stock charts
