# from elixir import *
# from connection import *
# from singledata import StaticData
# import itertools
# import sets
# from tickers_data import * 
# from timeSeriesData_tbl import TimeSeriesData

# class Ticker(Entity):
#     ticker = Field(String(7))
#     tsdata = OneToMany('TimeSeriesData')
#     staticdata = OneToMany('StaticData')
    
#     def __repr__(self):
#         return "%s %s %s "% (self.ticker, self.tsdata, self.staticdata)

# def windows(iterable, length=2, overlap = 0):
#     it = iter(iterable)
#     results = list(itertools.islice(it,length))
#     while len(results) == length:
#         yield results
#         results = results[length - overlap:]
#         results.extend(itertools.islice(it, length-overlap))
#     if results:
#         yield results

# def ticker_add(tickers):
#     for ticker in tickers: Ticker(ticker = ticker)
#     session.commit()

# def ticker_update(tickers):
#     """In:
#     List of tickers
#     will check if the list of tickers is already in the database, if not, it will be inserted.
#     """
#     origtickers = sets.Set(i.ticker for i in session.query(Ticker).all())
#     print "Number of tickers currently in database: ", len(origtickers)
#     tickers = [i for i in tickers if i not in origtickers]
#     print "Number of tickers will be added: ", len(tickers)
#     ticker_add(tickers)

# def main():
#     metadata.bind = "sqlite:///stock.db"
#     metadata.bind.echo = False
#     setup_all()
#     create_all()
#     for twindow in windows(s_n_p, 100, 0):
#         ticker_add(twindow)
#     ticker_update(full_stock_tickers)

# if __name__ == "__main__":
#     main() 
