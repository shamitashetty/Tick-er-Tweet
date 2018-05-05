import logging
import plotly.offline as py_offline
import plotly.graph_objs as go
import pandas as pd


class Plots(object):

  def __init__(self, **kwargs):
    """
    Initialize Plots.
    :param kwargs:
    """
    self.logger = logging.getLogger(kwargs["logger_name"])

  def candlestick_stock_plot(self, dataframe, stock_ticker):

    self.logger.info("Plotting stock data for {}".format(stock_ticker))
    mcd_candle = go.Candlestick(x=dataframe.index,
                                open=dataframe["{}_open".format(stock_ticker)],
                                high=dataframe["{}_high".format(stock_ticker)],
                                low=dataframe["{}_low".format(stock_ticker)],
                                close=dataframe["{}_close".format(stock_ticker)])
    data = [mcd_candle]
    py_offline.plot(data, filename='Candle Stick.html')

  def candlestick_stock_tweet_plot(self, stock_df, tweet_df, stock_ticker):
    """
    Accepts data frames where indices are set to date and plots a candle stick graph.
    :param stock_df:
    :param tweet_df:
    :param stock_ticker:
    :return:
    """
    self.logger.info("Plotting stock and tweet data for {}".format(stock_ticker))
    tweet_date_list = list(tweet_df.index.date)
    trace_tweet_y = stock_df.loc[stock_df.index.isin(tweet_date_list)]
    # trace_stockchange= ((stock_df['AMZN_close']/stock_df['AMZN_close'].shift(1)) - 1)
    trace_stockpct= pd.DataFrame([])
    trace_stockpct['{}_pctchange'.format(stock_ticker)]= (stock_df['{}_close'.format(stock_ticker)].pct_change() * 100)
    trace_stockpct= trace_stockpct.loc[trace_stockpct.index.isin(trace_tweet_y.index)]
    trace_tweet_y= pd.merge(trace_tweet_y, trace_stockpct, left_index=True, right_index=True)
    pct_change_list = trace_tweet_y["{}_pctchange".format(stock_ticker)].tolist()
    tweet_text_list = tweet_df.text.tolist()
    tweet_pct_change_list = []
    for pair in zip(pct_change_list, tweet_text_list):
      res_str = "% change: {}. Tweet: {}".format(round(pair[0], 4), pair[1])
      tweet_pct_change_list.append(res_str)
    trace_stock = go.Candlestick(x=stock_df.index,
                                 open=stock_df["{}_open".format(stock_ticker)],
                                 high=stock_df["{}_high".format(stock_ticker)],
                                 low=stock_df["{}_low".format(stock_ticker)],
                                 close=stock_df["{}_close".format(stock_ticker)])
    trace_stock_tweet = go.Candlestick(x=trace_tweet_y.index,
                                       open=trace_tweet_y["{}_open".format(stock_ticker)],
                                       high=trace_tweet_y["{}_high".format(stock_ticker)],
                                       low=trace_tweet_y["{}_low".format(stock_ticker)],
                                       close=trace_tweet_y["{}_close".format(stock_ticker)])
    trace_tweet = go.Scatter(
      x=trace_tweet_y.index,
      y=trace_tweet_y["{}_close".format(stock_ticker)],
      mode='markers',
      name='markers',
      marker={'color': 'blue', 'symbol': 104, 'size': "6"},
      text=tweet_pct_change_list,
      textposition='bottom',
      textfont=dict(
        family='sans serif',
        size=8,
        color='#ff7f0e'
      )
    )
    data = [trace_stock, trace_tweet]
    layout = go.Layout(
      showlegend=False, title='{} stock trend ft. Trump Tweets'.format(stock_ticker),
      yaxis={'title': '{} Stock'.format(stock_ticker)})
    fig = go.Figure(data=data, layout=layout)
    plot_url = py_offline.plot(fig, filename='sampleoutput/{}_tweet.html'.format(stock_ticker), auto_open=False)

# trace = go.Candlestick(x=df.index,
#                        open=df.AMZN_open,
#                        high=df.AMZN_high,
#                        low=df.AMZN_low,
#                        close=df.AMZN_close)
# data = [trace]
# py.plot(data, filename='AMAZON')

# d=3
# df["Marker"] = np.where(df["AMZN_open"]<df["AMZN_close"], df["AMZN_high"]+d, df["AMZN_low"]-d)
# df["Symbol"] = np.where(df["AMZN_open"]<df["AMZN_close"], "triangle-up", "triangle-down")
# df["Color"] = np.where(df["AMZN_open"]<df["AMZN_close"], "green", "red")
#
# Candle = go.Candlestick(x=df.index, open=df.AMZN_open,high=df.AMZN_high,low=df.AMZN_low, close=df.AMZN_close)
#
# Trace = go.Scatter(x=df.index,
#                    y=df.Marker,
#                    mode='markers',
#                    name ='markers',
#                    marker=go.Marker(size=5,
#                                     symbol=df["Symbol"],
#                                     color=df["Color"])
#                    )
# py_offline.plot([Candle, Trace], filename='CandleStick.html')










