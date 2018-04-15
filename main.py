#!/usr/bin/env python3

import datetime
import matplotlib
import matplotlib.pyplot as plt
import os
import pandas as pd
# For reading stock data from yahoo
import pandas_datareader as pdr
import quandl
import xlsxwriter
import pandas_datareader
import sys

class TweetAnalysis(object):

  def __init__(self, **kwargs):
    self.stock_data_sheetname = "stockdata"
    self.stock_data_filename = kwargs["stock_data_filename"]
    self.stock_data_path = "{}/stockdata/{}".format(os.getcwd(), self.stock_data_filename)
    self.quandl_api_key = kwargs["api_key"]
    quandl.ApiConfig.api_key = self.quandl_api_key

  def get_stock_data(self):
    # @todo implement this function
    """
    Extracts stock data from www.quandl.com and returns the data as an xlsxwriter workbook
    :return writer (xlsxwriter object):
    """
    # The tech stocks we'll use for this analysis
    ticker_list = ['AAPL', 'AMZN', 'FB', 'GOOG', 'MSFT']
    if os.path.exists(self.stock_data_path):
      pass
      # self.writer = xlsxwriter.Workbook(self.stock_data_path)
    else:
      self.writer = pd.ExcelWriter(self.stock_data_path, engine='xlsxwriter')
      # Set up End and Start times for data grab
      # We will look at stock prices over the past year, starting at January 1, 2016
      start = datetime.date(2017, 1, 1)
      end = datetime.date.today()
      try:
        # get the table for daily stock prices and,
        # filter the table for selected tickers, columns within a time range
        # set paginate to True because Quandl limits tables API to 10,000 rows per call
        stock_df = quandl.get_table('WIKI/PRICES', ticker=ticker_list,
                                    qopts={'columns': ['ticker', 'date', 'adj_open', 'adj_close']},
                                    date={'gte': start, 'lte': end},
                                    paginate=True)
        # create a new dataframe with 'date' column as index
        # stock_df_date_indexed = stock_df.set_index('date')
        # use pandas pivot function to sort adj_close by tickers
        stock_df_sortedby_tickers = stock_df.pivot(index='date', columns='ticker')
        stock_df_sortedby_tickers.to_excel(self.writer, sheet_name='{}'.format(self.stock_data_sheetname))
      except Exception as e:
        # Close the Pandas Excel writer and output the Excel file.
        self.writer.save()
        raise Exception("Exception while extracting stock data: {}".format(e))
      self.writer.save()

    data_frame = pd.read_excel(self.stock_data_path, sheet_name=self.stock_data_sheetname, skiprows=1)
    self.plot_data(data_frame)
    # Close the Pandas Excel writer and output the Excel file.
    # self.writer.save()

  def plot_data(self, data_frame):
    data_frame.drop(data_frame.index[0], inplace=True)
    start_adj_open_index = 1
    num_of_tickers = round((len(data_frame.columns) - 1) / 2)
    last_adj_open_index = start_adj_open_index + num_of_tickers
    first_adj_close_index = last_adj_open_index + 1
    data_frame.plot(x="ticker", y=list(data_frame.columns.values[start_adj_open_index:last_adj_open_index]), grid=True)
    plt.show()

  def get_tweet_data(self):
    pass

  def filter_tweets(self):
    pass

  def filter_stocks(self):
    pass

if __name__ == "__main__":
  tweet_analysis = TweetAnalysis(stock_data_filename=sys.argv[1], api_key=sys.argv[2])
  tweet_analysis.get_stock_data()
  # tweet_analysis.get_tweet_data()