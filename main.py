#!/usr/bin/env python3

import datetime
import json
import logging
import os
from plots import Plots
import sys
from getstockdata import GetStockData
from gettweetdata import GetMetaData
from gettweetdata import ScrapeWeb
from processdata import ProcessData
from sentimentanalysis import SentimentAnalysis

log_file_name = "tickertweet_{}".format(datetime.datetime.now().strftime("%Y-%B-%d_%H-%M-%S"))
logging.basicConfig(filename='{}.log'.format(log_file_name), level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s')

if __name__ == "__main__":
  if len(sys.argv) < 5:
    print("Received Invalid command line parameters \n. Usage: python3 main.py <stock_data_filename> <stock_index_data_"
          "filename> <quandl_api_key> <tweet_data_csv_filename>")
    exit(0)
  # Set start and end date for stock and tweet retrieval
  logging.info("Started Tick-er-Tweet")
  start_date = datetime.date(2017, 1, 1)
  end_date = datetime.date.today()
  # Get ticker list from the input json file
  ticker_list_file_path = '{}/stockdata/input/tickerlist.json'.format(os.getcwd())
  logging.info("Reading ticker symbols list from {}.".format(ticker_list_file_path))
  with open('{}'.format(ticker_list_file_path), 'r') as ticker_list_f:
    ticker_list_str = ticker_list_f.read()
    ticker_list_json_str = json.loads(ticker_list_str)
  ticker_list = ticker_list_json_str["stock_ticker"]
  stock_index_list = ticker_list_json_str["stock_index_ticker"]
  logging.info("Extracting Stock Data")
  get_stock_data = GetStockData(stock_data_filename=sys.argv[1], index_data_filename=sys.argv[2], api_key=sys.argv[3],
                                start_date=start_date, end_date=end_date)
  get_stock_data.get_stock_data(ticker_list, stock_index_list)
  # Get tweet data
  tweet_user = sys.argv[4]
  logging.info("Extracting tweet data")
  if not os.path.exists('{}/tweetdata/output/{}.csv'.format(os.getcwd(), tweet_user)):
    scrape_web = ScrapeWeb(user="{}".format(tweet_user), start_date=start_date, end_date=end_date)
    scrape_web.get_tweets()
    # Get tweet data for the user "realdonaldtrump"
    meta_data = GetMetaData(user="{}".format(tweet_user))
    meta_data.get_metadata()
  logging.info("Processing the stock and tweet data")
  # Process retrieved data
  process_data = ProcessData(ticker_list=ticker_list)
  processed_df_stock = process_data.process_data_stock('{}/stockdata/output/{}'.format(os.getcwd(), sys.argv[1]))
  processed_df_tweet = process_data.process_data_tweet('{}/tweetdata/output/{}.csv'.format(os.getcwd(), sys.argv[4]))
  logging.info("Performing sentiment analysis")
  sa = SentimentAnalysis(csv_file='{}/tweetdata/output/{}.csv'.format(os.getcwd(), sys.argv[4]))
  sa.plot(['favorite_count', 'retweet_count'])
  logging.info("Plotting stock and tweet data")
  for ticker in ticker_list:
    filtered_df = process_data.filter_tweet(processed_df_tweet, ticker)
    # Plot processed data
    plot_data = Plots()
    # plot_data.candlestick_stock_plot(processed_df_stock, 'AMZN')
    plot_data.candlestick_stock_tweet_plot(processed_df_stock, filtered_df, ticker)
  logging.info("Tick-er-Tweet ran successfully!")
  print("Tick-er-Tweet ran successfully!")