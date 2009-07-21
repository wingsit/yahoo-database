from ystockquote import get_historical_prices_list as getprice
from ystockquote import get_all

from elixir import *
from datetime import date

metadata.bind = "sqlite:///stock.db"
metadata.bind.echo = False

# class Ticker(Entity):
#     ticker = Field(String(7))
#     tsdata = OneToMany('TimeSeriesData')
#     staticdata = OneToMany('StaticData')
    
#     def __repr__(self):
#         return "%s %s %s "% (self.ticker, self.tsdata, self.staticdata)

# class TimeSeriesData(Entity):
#     ticker = ManyToOne('Ticker', primary_key = True)
#     date = Field(Date, primary_key = True)
#     open = Field(Float)
#     high = Field(Float)
#     low = Field(Float)
#     close = Field(Float)
#     adjclose = Field(Float)
#     volume = Field(Integer)
    
#     def __repr__(self):
#         return "%s %s %.2f %.2f %.2f %0.2f %0.2f %.2d\n" % (self.ticker, self.date, self.open, self.high, self.low, self.close, self.adjclose, self.volume)

class StaticData(Entity):
    ticker = ManyToOne('Ticker', primary_key = True)
    price = Field(Float)
    change = Field(Float)
    volume = Field(Integer)
    avg_daily_volume = Field(Integer)
    stock_exchange = Field(String(15))
    market_cap = Field(String(10))
    book_value = Field(Float)
    ebitda = Field(String(10))
    dividend_per_share = Field(Float)
    dividend_yield = Field(Float)
    earnings_per_share = Field(Float)
    week_high_52 = Field(Float) 
    week_low_52 = Field(Float)
    day_moving_avg_50 = Field(Float)
    day_moving_avg_200 = Field(Float)
    price_earnings_ratio = Field(Float)
    price_earnings_growth_ratio = Field(Float)
    price_sales_ratio = Field(Float)
    price_book_ratio = Field(Float) 
    short_ratio = Field(Float) 

    def __repr__(self):
        string = ""
        for i in sorted(self.__dict__.keys()):
            string += "%s: %s\n"%(i,self.__dict__[i])
        return string

def time_series_fetcher(obj,ticker, begin, end = date.today()):
    for i in getprice(ticker, begin, end):
        obj.tsdata.append(TimeSeriesData( date = i[0], open = i[1], high = i[2], low = i[3], close = i [4], adjclose = i[5], volume = i[6]))

def static_fetcher(obj, ticker):
    sdata = get_all(ticker)
    obj.staticdata.append(StaticData(
        price = sdata['price'],
        change = sdata['change'],
        volume = sdata['volume'],
        avg_daily_volume = sdata['avg_daily_volume'],
        stock_exchange = sdata['stock_exchange'],
        market_cap = sdata['market_cap'],
        book_value = sdata['book_value'],
        ebitda = sdata['ebitda'],
        dividend_per_share = sdata['dividend_per_share'],
        dividend_yield = sdata['dividend_yield'],
        earnings_per_share = sdata['earnings_per_share'],
        week_high_52 = sdata['52_week_high'],
        week_low_52 = sdata['52_week_low'],
        day_moving_avg_50 = sdata['50_day_moving_avg'],
        day_moving_avg_200 = sdata['200_day_moving_avg'],
        price_earnings_ratio = sdata['price_earnings_ratio'],
        price_earnings_growth_ratio = sdata['price_earnings_growth_ratio'],
        price_sales_ratio = sdata['price_sales_ratio'],
        price_book_ratio = sdata['price_book_ratio'],
        short_ratio = sdata['short_ratio']))

if __name__ == "__main__":
    setup_all()
    create_all()
    tickers = ["yhoo", "GS", "c"]
    begin = date(2005,1,1)
    for ticker in tickers:
        yhoo = Ticker(ticker= ticker)
        time_series_fetcher(yhoo, ticker,begin)
        static_fetcher(yhoo,ticker)
        session.commit()
        print Ticker.query.first().ticker
    
