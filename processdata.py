import pandas as pd
import itertools

class ProcessData(object):

  def __init__(self, **kwargs):
    """
    Initialize ProcessData.
    :param kwargs:
    """
    self.ticker_list = kwargs["ticker_list"]


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

  def process_data_tweet(self, csv_file_path):
    with open(csv_file_path) as csvfile:
      read_csv = pd.read_csv(csvfile, delimiter=',')
      read_csv['tweetL'] = read_csv['text'].str.lower()
      tweetdata_df = read_csv[read_csv['tweetL'].str.contains('amazon|amzn|@amazon|#amazon')]
      # Convert created_at to datatime format and set it as index
      tweetdata_df['created_at'] = pd.to_datetime(tweetdata_df['created_at'])
      tweetdata_df.set_index('created_at', inplace=True)
      tweetdata_df.index.name = ['Date']
    return tweetdata_df

