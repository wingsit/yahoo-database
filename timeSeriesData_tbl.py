from datetime import date, timedelta
from ystockquote import get_historical_prices_list as getprice, get_all
#from ticker_tbl import Ticker
from elixir import *
from singledata import StaticData
from tickers_data import *
import sets
 
class Ticker(Entity):
    ticker = Field(String(7))
    tsdata = OneToMany('TimeSeriesData')
    staticdata = OneToMany('StaticData')
    
    def __repr__(self):
        return "%s"% (self.ticker)

def windows(iterable, length=2, overlap = 0):
    it = iter(iterable)
    results = list(itertools.islice(it,length))
    while len(results) == length:
        yield results
        results = results[length - overlap:]
        results.extend(itertools.islice(it, length-overlap))
    if results:
        yield results

def ticker_add(tickers):
    for ticker in tickers: Ticker(ticker = ticker)
    session.commit()

def ticker_update(tickers):
    """In:
    List of tickers
    will check if the list of tickers is already in the database, if not, it will be inserted.
    """
    origtickers = sets.Set(i.ticker for i in session.query(Ticker).all())
    print "Number of tickers currently in database: ", len(origtickers)
    tickers = [i for i in tickers if i not in origtickers]
    print "Number of tickers will be added: ", len(tickers)
    ticker_add(tickers)



class TimeSeriesData(Entity):
    ticker = ManyToOne('Ticker', primary_key = True)
    date = Field(Date, primary_key = True)
    open = Field(Float)
    high = Field(Float)
    low = Field(Float)
    close = Field(Float)
    adjclose = Field(Float)
    volume = Field(Integer)
    
    def __repr__(self):
        return "%s" % self.ticker
#        return "%s %s %.2f %.2f %.2f %0.2f %0.2f %.2d\n" % (self.ticker, self.date, self.open, self.high, self.low, self.close, self.adjclose, self.volume)

def timeSeriesData_add(tickerObj, begin = date.today() - timedelta(days = 182), end = date.today()):
    """This will update all tickers in the database"""
    ticker = tickerObj.ticker
    data = getprice(ticker, begin, end)
    for i in data:
        tickerObj.tsdata.append(TimeSeriesData( date = i[0], open = i[1], high = i[2], low = i[3], close = i [4], adjclose = i[5], volume = i[6]))
    session.commit()

def timeSeriesData_update(tickerObj, begin = date.today() - timedelta(days = 182), end = date.today):
    print sets.Set((i.ticker, i.date) for i in session.query(TimeSeriesData).all())
    pass


def main():
    pass

if __name__ == "__main__":
    metadata.bind = "sqlite:///stock.db"
    metadata.bind.echo = False
    setup_all()
    create_all()
    ticker_update(s_n_p)
    query = session.query(Ticker)
    for i in query.all()[:20]:
        timeSeriesData_add(i)
        #    timeSeriesData_update(query.all()[:3])
    main()
