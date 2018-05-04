#!/usr/bin/env python3

import datetime
import os
from plots import Plots
import sys
from getstockdata import GetStockData
from gettweetdata import GetMetaData
from gettweetdata import ScrapeWeb
from processdata import ProcessData
from sentimentanalysis import SentimentAnalysis


if __name__ == "__main__":
  # Set start and end date for stock and tweet retrieval
  start_date = datetime.date(2017, 1, 1)
  end_date = datetime.date.today()
  # Get stock data
  ticker_list = ['AAPL', 'AMZN', 'FB', 'GOOG', 'JWN', 'MSFT', 'PEP', 'X', 'GM', 'F', 'BA']
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
  sa = SentimentAnalysis(csv_file='{}/tweetdata/{}.csv'.format(os.getcwd(), sys.argv[4]))
  sa.plot(['favorite_count', 'retweet_count'])
  for ticker in ticker_list:
    filtered_df = process_data.filter_tweet(processed_df_tweet, ticker)
    # Plot processed data
    plot_data = Plots()
    # plot_data.candlestick_stock_plot(processed_df_stock, 'AMZN')
    plot_data.candlestick_stock_tweet_plot(processed_df_stock, filtered_df, ticker)
  print("Tick-er-Tweet ran successfully!")