from ystockquote import get_historical_prices_list as getprice
from ystockquote import get_all

from elixir import *
from datetime import date

metadata.bind = "sqlite:///"
metadata.bind.echo = True

class tsdata(Entity):
    ticker = Field(String(7))
    date = Field(Date)
    open = Field(Float)
    high = Field(Float)
    low = Field(Float)
    close = Field(Float)
    adjclose = Field(Float)
    volume = Field(Integer)
    
    def __repr__(self):
        return "%s %s %.2f %.2f %.2f %0.2f %0.2f %.2d\n" % (self.ticker, self.date, self.open, self.high, self.low, self.close, self.adjclose, self.volume)

class staticdata(Entity):
    ticker = OnetoOne("tsdata")
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
    52_week_high = Field(Float) 
    52_week_low = Field(Float)
    50day_moving_avg = Field(Float)
    200day_moving_avg = Field(Float)
    price_earnings_ratio = Field(Float)
    price_earnings_growth_ratio = Field(Float)
    price_sales_ratio = Field(Float)
    price_book_ratio = Field(Float) 
    short_ratio = Field(Float) 
    pass

def fetcher(ticker, begin, end = date.today()):
    for i in  getprice("YHOO", begin, end):
        tsdata(ticker = ticker, date = i[0], open = i[1], high = i[2], low = i[3], close = i [4], adjclose = i[5], volume = i[6])


    
if __name__ == "__main__":
    setup_all()
    create_all()
    ticker = "YHOO"
    begin = date(2009,5,1)
    fetcher(ticker, begin)
    session.commit()
    print tsdata.query.all()
    print get_all(ticker)
