#!/usr/bin/env python3

import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd
import quandl
import sys
from get_metadata import GetMetaData
from scrape import ScrapeWeb
from processdata import ProcessData
from plots import Plots

class GetStockData(object):

  def __init__(self, **kwargs):
    """
    Initialize TweetAnalysis class using command line parameters.
    :param kwargs:
    """
    self.stock_data_sheetname = "stockdata"
    self.index_data_sheetname = "indexdata"
    self.stock_data_filename = kwargs["stock_data_filename"]
    self.index_data_filename = kwargs["index_data_filename"]
    self.stock_data_path = "{}/stockdata/{}".format(os.getcwd(), self.stock_data_filename)
    self.index_data_path = "{}/stockdata/{}".format(os.getcwd(), self.index_data_filename)
    self.quandl_api_key = kwargs["api_key"]
    quandl.ApiConfig.api_key = self.quandl_api_key
    #Start and end dates for stock data extraction
    self.start_date = kwargs["start_date"]
    self.end_date = kwargs["end_date"]
    self.writer_stock = None
    self.writer_index = None


  def get_stock_data_from_quandl(self, ticker_list):
    """
    Get stock data from quandl and save it in an excel sheet.
    :return stock_df_sortedby_tickers (DataFrame:
    """
    try:
      # get the table for daily stock prices and,
      # filter the table for selected tickers, columns within a time range
      # set paginate to True because Quandl limits tables API to 10,000 rows per call
      stock_df = quandl.get_table('WIKI/PRICES', ticker=ticker_list,
                                  qopts={'columns': ['ticker', 'date', 'open', 'close', 'low', 'high', 'adj_open',
                                                     'adj_close', 'volume', 'adj_volume']},
                                  date={'gte': self.start_date, 'lte': self.end_date},
                                  paginate=True)
      # create a new dataframe with 'date' column as index
      # use pandas pivot function to sort adj_close by tickers
      stock_df_sortedby_tickers = stock_df.pivot(index='date', columns='ticker')
      stock_df_sortedby_tickers.to_excel(self.writer_stock, sheet_name='{}'.format(self.stock_data_sheetname))
    except Exception as e:
      # Close the Pandas Excel writer and output the Excel file.
      self.writer_stock.save()
      raise Exception("Exception while extracting stock data: {}".format(e))
    self.writer_stock.save()
    return stock_df_sortedby_tickers

  def get_stock_index_data_from_quandl(self, stock_index_list):
    """
    Get stock index data from quandl and save it in an excel sheet.
    :return index_df_sortedby_tickers (DataFrame):
    """
    try:
      # get the table for daily stock prices and,
      # filter the table for selected tickers, columns within a time range
      # set paginate to True because Quandl limits tables API to 10,000 rows per call
      index_df = quandl.get(stock_index_list, start_date=self.start_date, end_date=self.end_date)
      # create a new dataframe with 'date' column as index
      # use pandas pivot function to sort adj_close by tickers
      # index_df_sortedby_tickers = index_df.pivot(index='date', columns='ticker')
      index_df.to_excel(self.writer_index, sheet_name='{}'.format(self.index_data_sheetname))
    except Exception as e:
      # Close the Pandas Excel writer and output the Excel file.
      self.writer_index.save()
      raise Exception("Exception while extracting stock data: {}".format(e))
    self.writer_index .save()
    return index_df

  def get_stock_data(self, ticker_list, stock_index_list):
    """
    Extracts stock data from www.quandl.com and stores it in an excel file
    :return None:
    """
    stock_data_file_exists = os.path.exists(self.stock_data_path)
    index_data_exists = os.path.exists(self.index_data_path)
    if not stock_data_file_exists:
      self.writer_stock = pd.ExcelWriter(self.stock_data_path, engine='xlsxwriter')
      # get stock data from quandl and write it to an excel file
      self.get_stock_data_from_quandl(ticker_list)
    if not index_data_exists:
      # get index data from quandl and write it to an excel file
      self.writer_index = pd.ExcelWriter(self.index_data_path, engine='xlsxwriter')
      self.get_stock_index_data_from_quandl(stock_index_list)
    # stock_data_frame = pd.read_excel(self.stock_data_path, sheet_name=self.stock_data_sheetname, skiprows=1)
    # index_data_frame = pd.read_excel(self.index_data_path, sheet_name=self.index_data_sheetname, skiprows=1)
    # self.plot_data(stock_data_frame)
    # self.plot_data(index_data_frame)

  def plot_data(self, data_frame):
    """
    Plot data in a dataframe.
    :param data_frame:
    :return:
    """
    data_frame.drop(data_frame.index[0], inplace=True)
    start_adj_open_index = 1
    num_of_tickers = round((len(data_frame.columns) - 1) / 2)
    last_adj_open_index = start_adj_open_index + num_of_tickers
    data_frame.plot(x="ticker", y=list(data_frame.columns.values[start_adj_open_index:last_adj_open_index]), grid=True)
    plt.show()


if __name__ == "__main__":
  # Set start and end date for stock and tweet retrieval
  start_date = datetime.date(2017, 1, 1)
  end_date = datetime.date.today()
  # Get stock data
  ticker_list = ['AAPL', 'AMZN', 'FB', 'GOOG', 'JWN', 'MSFT']
  # S&P500: 'BCIW/_INX'
  stock_index_list = ['BCB/7809', 'NASDAQOMX/COMP']
  get_stock_data = GetStockData(stock_data_filename=sys.argv[1], index_data_filename=sys.argv[2], api_key=sys.argv[3],
                                start_date=start_date, end_date=end_date)
  get_stock_data.get_stock_data(ticker_list, stock_index_list)
  # Get tweet data
  tweet_user = sys.argv[4]
  if not os.path.exists('{}/tweetdata/{}.csv'.format(os.getcwd(), tweet_user)):
    scrape_web = ScrapeWeb(user="{}".format(tweet_user), start_date=start_date, end_date=end_date)
    scrape_web.get_tweets()
    # Get tweet data for the user "realdonaldtrump"
    meta_data = GetMetaData(user="{}".format(tweet_user))
    meta_data.get_metadata()
  # Process retrieved data
  process_data = ProcessData(ticker_list=ticker_list)
  processed_df_stock = process_data.process_data_stock('{}/stockdata/{}'.format(os.getcwd(), sys.argv[1]))
  processed_df_tweet = process_data.process_data_tweet('{}/tweetdata/{}.csv'.format(os.getcwd(), sys.argv[4]))
  # Plot processed data
  plot_data = Plots()
  # plot_data.candlestick_stock_plot(processed_df_stock, 'AMZN')
  plot_data.candlestick_stock_tweet_plot(processed_df_stock, processed_df_tweet, 'AMZN')