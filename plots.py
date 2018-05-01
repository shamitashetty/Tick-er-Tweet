import plotly.offline as py_offline
import plotly.graph_objs as go


class Plots(object):

  def __init__(self, **kwargs):
    """
    Initialize Plots.
    :param kwargs:
    """
    pass

  def candlestick_stock_plot(self, dataframe, stock_ticker):
    import pdb;pdb.set_trace()
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
    tweet_date_list = list(tweet_df.index.date)
    trace_tweet_y = stock_df.loc[stock_df.index.isin(tweet_date_list)]

    trace_stock = go.Candlestick(x=stock_df.index,
                                 open=stock_df.AMZN_open,
                                 high=stock_df.AMZN_high,
                                 low=stock_df.AMZN_low,
                                 close=stock_df.AMZN_close)
    trace_stock_tweet = go.Candlestick(x=tweet_df.index,
                                       open=stock_df.AMZN_open,
                                       high=stock_df.AMZN_high,
                                       low=stock_df.AMZN_low,
                                       close=stock_df.AMZN_close)
    trace_tweet = go.Scatter(
      x=trace_tweet_y.index,
      y=trace_tweet_y["{}_close".format(stock_ticker)],
      mode='markers',
      name='markers',
      text=tweet_df.text,
      textposition='bottom',
      textfont=dict(
        family='sans serif',
        size=8,
        color='#ff7f0e'
      )
    )
    data = [trace_stock, trace_stock_tweet, trace_tweet]
    layout = go.Layout(
      showlegend=False, title='{} stock trend ft. Trump Tweets'.format(stock_ticker),
      yaxis={'title': '{} Stock'.format(stock_ticker)})
    fig = go.Figure(data=data, layout=layout)
    plot_url = py_offline.plot(fig, filename='{}_tweet.html'.format(stock_ticker))

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










