#!/usr/bin/env python
#
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.


import urllib
from datetime import datetime, date

"""
This is the "ystockquote" module.

This module provides a Python API for retrieving stock data from Yahoo Finance.

sample usage:
>>> import ystockquote
>>> print ystockquote.get_price('GOOG')
529.46

[Date, open, high, low, close, volume, adjclose]
"""
    
class DataError(Exception):
    """dataerror class for volatility exception"""
    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__

class NetworkError(Exception):
    """dataerror class for volatility exception"""
    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__

def request1(ticker):
    url = 'http://finance.yahoo.com/d/cp?s=^%s' % (ticker)
    return urllib.urlopen(url).read().strip().strip('"')


def __request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.urlopen(url).read().strip().strip('"')


def get_all(symbol):
    """
    Get all available quote data for the given ticker symbol.
    
    Returns a dictionary.
    """
    values = __request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
    data = {}
    data['ticker'] = symbol
    try: data['price'] = float(values[0])
    except:data['price'] = None
    try: data['change'] = float(values[1])
    except: data['change'] = None
    try: data['volume'] = int(values[2])
    except: data['volume'] = None
    try: data['avg_daily_volume'] = float(values[3])
    except: data['avg_daily_volume'] = None
    data['stock_exchange'] = values[4]
    data['market_cap'] = values[5]
    try: data['book_value'] = float(values[6])
    except: data['book_value'] = None
    try: data['ebitda'] = float(values[7])
    except:data['ebitda'] = None
    try: data['dividend_per_share'] = float(values[8])
    except: data['dividend_per_share'] = None
    try: data['dividend_yield'] = float(values[9])
    except : data['dividend_yield'] = None
    try: data['earnings_per_share'] = float(values[10])
    except: data['earnings_per_share'] = None
    try: data['52_week_high'] = float(values[11])
    except: data['52_week_high'] = None
    try: data['52_week_low'] = float(values[12])
    except: data['52_week_low'] = None
    try: data['50_day_moving_avg'] = float(values[13])
    except: data['50_day_moving_avg'] = None
    try: data['200_day_moving_avg'] = float(values[14])
    except : data['200_day_moving_avg'] = None
    try: data['price_earnings_ratio'] = float(values[15])
    except: data['price_earnings_ratio'] = None
    try: data['price_earnings_growth_ratio'] = float(values[16])
    except: data['price_earnings_growth_ratio'] = None
    try: data['price_sales_ratio'] = float(values[17])
    except: data['price_sales_ratio'] = None
    try: data['price_book_ratio'] = float(values[18])
    except: data['price_book_ratio'] = None
    try: data['short_ratio'] = float(values[19])
    except: data['short_ratio'] = None
    return data

def get_price(symbol): 
    return __request(symbol, 'l1')


def get_change(symbol):
    return __request(symbol, 'c1')
    
    
def get_volume(symbol): 
    return __request(symbol, 'v')


def get_avg_daily_volume(symbol): 
    return __request(symbol, 'a2')
    
    
def get_stock_exchange(symbol): 
    return __request(symbol, 'x')
    
    
def get_market_cap(symbol):
    return __request(symbol, 'j1')
   
   
def get_book_value(symbol):
    return __request(symbol, 'b4')

def get_ebitda(symbol): 
    return __request(symbol, 'j4')
    
def get_dividend_per_share(symbol):
    return __request(symbol, 'd')


def get_dividend_yield(symbol): 
    return __request(symbol, 'y')
def get_earnings_per_share(symbol): 
    return __request(symbol, 'e')


def get_52_week_high(symbol): 
    return __request(symbol, 'k')
    
    
def get_52_week_low(symbol): 
    return __request(symbol, 'j')


def get_50day_moving_avg(symbol): 
    return __request(symbol, 'm3')
    
    
def get_200day_moving_avg(symbol): 
    return __request(symbol, 'm4')
    
    
def get_price_earnings_ratio(symbol): 
    return __request(symbol, 'r')


def get_price_earnings_growth_ratio(symbol): 
    return __request(symbol, 'r5')


def get_price_sales_ratio(symbol): 
    return __request(symbol, 'p5')

def get_price_book_ratio(symbol): 
    return __request(symbol, 'p6')

def get_short_ratio(symbol): 
    return __request(symbol, 's7')

def get_historical_prices(symbol, start_date, end_date=date.today(), freq ='d'):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    Returns a nested a dictionary.
    """
    start_date = str(start_date)[0:11]
    end_date = str(end_date)[0:11]
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(end_date[5:7]) - 1) + \
          'e=%s&' % str(int(end_date[8:10])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=%s&' % freq+ \
          'a=%s&' % str(int(start_date[5:7]) - 1) + \
          'b=%s&' % str(int(start_date[8:10])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'ignore=.csv'
    try:
        days = urllib.urlopen(url).readlines()
    except IOError:
        raise NetworkError('No data is delivered from Yahoo via internet')
    data = {}
    try:
        for day in days[1:]:
            day =  day[:-2].split(',')
            data[date(int(day[0][0:4]),int(day[0][5:7]),int(day[0][8:10]))] =(float(day[1]), float(day[2]), float(day[3]), float(day[4]),  float(day[6]),long(day[5]))
        return data
    except IndexError:
        raise DataError('No data from Yahoo with ticker: %s'%symbol)

def get_historical_prices_list(symbol, start_date, end_date = date.today(), freq = 'd', assending = False):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    Returns a nested list.
    """
    try:
        def mapper(quote):
            quote = quote[:-2].split(',')
            quote[0] = date(int(quote[0][0:4]),int(quote[0][5:7]),int(quote[0][8:10]))
            quote[1] = float(quote[1])
            quote[2] = float(quote[2])
            quote[3] = float(quote[3])
            quote[4] = float(quote[4])
            quote[6], quote[5] = long(quote[5]),float(quote[6])
            return quote
        start_date = str(start_date)[0:11]
        end_date = str(end_date)[0:11]
        url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
              'd=%s&' % str(int(end_date[5:7]) - 1) + \
              'e=%s&' % str(int(end_date[8:10])) + \
              'f=%s&' % str(int(end_date[0:4])) + \
              'g=%s&' % freq+ \
              'a=%s&' % str(int(start_date[5:7]) - 1) + \
              'b=%s&' % str(int(start_date[8:10])) + \
              'c=%s&' % str(int(start_date[0:4])) + \
              'ignore=.csv'
        days = urllib.urlopen(url).readlines()
        data = [mapper(day) for day in days[1:]]
    except IOError:
        raise NetworkError('No data is delivered from Yahoo via internet')
    except ValueError:
        raise DataError('No data from Yahoo with ticker: %s'%symbol)
    if assending:
        return reversed(data)
    else:
        return data


if __name__ =="__main__":
    #data = get_historical_prices("YHOO", date(2001,1,1), date(2001,5,1), freq = 'd')
#    data = get_historical_prices_list("YHOO", datetime(2001,1,1), datetime(2001,5,1), freq = 'd')
    #    for i in data: print i
    data2 = get_historical_prices_list("YHOO", datetime(2001,1,1), datetime(2001,5,1), freq = 'm')
    for day in data2:
        print day
#    print get_all("yhoo")

