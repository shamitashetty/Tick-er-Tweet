import json
import logging
import os
import pandas as pd

class ProcessData(object):

  def __init__(self, **kwargs):
    """
    Initialize ProcessData.
    :param kwargs:
    """
    self.ticker_list = kwargs["ticker_list"]
    self.logger = logging.getLogger(kwargs["logger_name"])

  def process_data_stock(self, excel_file_path):
    # Get stock data from excel sheet and rename columns
    # excel file path --> 'stockdata/stockdata.xlsx'
    df = pd.read_excel(excel_file_path)
    df = df.drop(df.index[1])
    len_symbols_list = len(self.ticker_list)
    for col in range(0, len(df.columns), len_symbols_list):
      stock_names = df.columns[col: col + len_symbols_list]
      stock_data_type = stock_names[0]
      for index, name in enumerate(stock_names):
        df = df.rename(columns={name: "{}_{}".format(self.ticker_list[index], stock_data_type)})
    # Set Index for dataframe
    df = df.drop(df.index[0])
    df.index = pd.to_datetime(df.index)
    df.index.names = ['Date']
    # Print and plot dataframe
    # print(df.head(5))
    # df.plot(title='stock data', kind='area')
    # plt.show()
    return df
  
  def get_filter_str(self, ticker):
    filter_strings_file_path = '{}/tweetdata/input/filter_strings.json'.format(os.getcwd())
    self.logger.info("Reading filter strings from {}".format(filter_strings_file_path))
    with open('{}'.format(filter_strings_file_path), 'r') as filter_strings_f:
      filter_strings = filter_strings_f.read()
      filter_dict = json.loads(filter_strings)
      try:
        filter_str = filter_dict[ticker]
      except KeyError:
        filter_str = ticker.lower()
        self.logger.warning('Filter string for {} stock not found in {}. Using ticker symbol ({}) as filter string.'.format(
          ticker, filter_strings_file_path, filter_str))
    return filter_str
          
  def filter_tweet(self, processed_df, ticker):
    stock_filter_str = self.get_filter_str(ticker)
    processed_df['tweetL'] = processed_df['text'].str.lower()
    self.logger.info("Filtering Tweets")
    filtered_df = processed_df[processed_df['tweetL'].str.contains('{}'.format(stock_filter_str))]
    return filtered_df  
  
  def process_data_tweet(self, csv_file_path):
    with open(csv_file_path) as csvfile:
      processed_df = pd.read_csv(csvfile, delimiter=',')
      # Convert created_at to datatime format and set it as index
      processed_df['created_at'] = pd.to_datetime(processed_df['created_at'])
      processed_df.set_index('created_at', inplace=True)
      processed_df.index.name = ['Date']
    return processed_df

