#!/usr/bin/env python3

import datetime
# import matplotlib.pyplot as plt
import os
import pandas as pd
# For reading stock data from yahoo
import pandas_datareader as pdr
import xlsxwriter


class TweetAnalysis:

  def __init__(self):
    self.stock_data_filename = "stockdata.xlsx"
    self.stock_data_path = "{}/stockdata/{}".format(os.getcwd(), self.stock_data_filename)

  def get_stock_data(self):
    # @todo implement this function
    """
    Extracts stock data from www.quandl.com and returns the data as an xlsxwriter workbook
    :return writer (xlsxwriter object):
    """
    # The tech stocks we'll use for this analysis
    # tech_list = ['GOOG', 'AAPL', 'MSFT', 'AMZN']
    tech_list = ['GOOG']
    if os.path.exists(self.stock_data_path):
      self.writer = xlsxwriter.Workbook(self.stock_data_path)
    else:
      self.writer = pd.ExcelWriter(self.stock_data_path, engine='xlsxwriter')
      # Set up End and Start times for data grab
      # We will look at stock prices over the past year, starting at January 1, 2016
      start = datetime.date(2016, 1, 1)
      end = datetime.date.today()
      stock_df_list = []
      try:
        for stock in tech_list:
          # Set DataFrame as the Stock Ticker
          stock_df = pdr.get_data_quandl(stock, start, end, retry_count=3, pause=2)
          stock_df.to_excel(self.writer, sheet_name='{}'.format(stock))
          stock_df_list.append(stock_df)
      except Exception as e:
        # Close the Pandas Excel writer and output the Excel file.
        self.writer.save()
        raise Exception("Exception while extracting stock data: {}".format(e))
    for stock in tech_list:
      data_frame = pd.read_excel(self.stock_data_path, sheet_name=stock)
      self.plot_data(data_frame)
    return self.writer

  def __exit__(self, exc_type, exc_val, exc_tb):
    # Close the Pandas Excel writer and output the Excel file.
    self.writer.save()

  def plot_data(self, data_frame):
    # pylab.rcParams['figure.figsize'] = (15, 9)  # Change the size of plots
    # apple["Adj Close"].plot(grid=True)
    data_frame["AdjClose"].plot(grid=True)

  def get_tweet_data(self):
    pass

  def filter_tweets(self):
    pass

  def filter_stocks(self):
    pass

if __name__ == "__main__":
  tweet_analysis = TweetAnalysis()
  stock_data = tweet_analysis.get_stock_data()
  # tweet_analysis.get_tweet_data()