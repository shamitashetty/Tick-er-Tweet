#Get tweet data from csv

import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from textblob import TextBlob
import re

class SentimentAnalysis(object):

  def __init__(self, **kwargs):
    """
    Initialize ProcessData.
    :param kwargs:
    """
    self.tweet_data = pd.read_csv('{}'.format(kwargs["csv_file"]))
    del self.tweet_data['in_reply_to_screen_name']
    self.logger = logging.getLogger(kwargs["logger_name"])


  def get_favourite_tweet(self):
    """
    Get the tweet with most likes
    :return fav_tweet (String):
    :return fav_max_count (Integer):
    """
    fav_max_count = np.max(self.tweet_data['favorite_count'])
    fav_tweet = self.tweet_data[self.tweet_data.favorite_count == fav_max_count].index[0]
    return fav_tweet, fav_max_count

  def get_most_retweeted_tweet(self):
    """
    Get the tweet with most retweets
    :return most_retweeted_tweet (String):
    :return rt_max_count (Integer):
    """
    rt_max_count = np.max(self.tweet_data['retweet_count'])
    most_retweeted_tweet = self.tweet_data[self.tweet_data.retweet_count == rt_max_count].index[0]
    return most_retweeted_tweet, rt_max_count

  def plot(self, data_types):
    """
    Plot likes or retweets over time
    :param data_type (String): Allowed valued: "favorite_count"/"retweet_count"
    :return None:
    """
    logging.info("Plotting most liked and most retweeted tweet")
    if not data_types:
      self.logger.warning("data_types list is empty. Valid data_types are favorite_count and retweet_count. "
                      "Plotting both favorite and retweet count")
      data_types = ["favorite_count", "retweet_count"]
    else:
      for data_type in data_types:
        if data_type not in ["favorite_count", "retweet_count"]:
          self.logger.warning("{} is not a valid data_type. Valid data_types are favorite_count and retweet_count. "
                          "Plotting both favorite and retweet count".format(data_type))
          data_types = ["favorite_count", "retweet_count"]
          break
    tweet_data = self.tweet_data
    tweet_data['created_at'] = pd.to_datetime(tweet_data['created_at'])
    tweet_data.set_index('created_at', inplace=True)
    tweet_data.index.name = ['Date']
    for data_type in data_types:
      # Plot likes and retweets over time
      plot_data = pd.Series(data=tweet_data['{}'.format(data_type)].values, index=tweet_data.index)
      plot_data.plot(figsize=(16, 4), label='{}'.format(data_type), legend=True)
      plt.savefig('sampleoutput/sentiment_analysis'.format())
      # plt.show()

  #Sentiment analysis of tweets
  def clean_tweet(self, tweet):
    """
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    :return:
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

  def analyze_sentiment(self, tweet):
    """
    Utility function to classify the polarity of a tweet
    using textblob.
    :param tweet:
    :return:
    """
    self.logger.info("Analysing sentiment")
    analysis = TextBlob(self.clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
      return 1
    elif analysis.sentiment.polarity == 0:
      return 0
    else:
      return -1

  def get_SA_results(self):
    """
    Return percentage of positive, negative and neutral tweets
    :return pct_pos_tweets (Float):
    :return pct_neu_tweets (Float):
    :return pct_neg_tweets (Float):
    """
    self.logger.info("Getting sentiment analysis results")
    # Create a column with the result of the analysis:
    self.tweet_data['SA'] = np.array([self.analyze_sentiment(tweet) for tweet in self.tweet_data['text']])
    # Construct lists with classified tweets
    pos_tweets = [tweet for index, tweet in enumerate(self.tweet_data['text']) if self.tweet_data['SA'][index] > 0]
    neu_tweets = [tweet for index, tweet in enumerate(self.tweet_data['text']) if self.tweet_data['SA'][index] == 0]
    neg_tweets = [tweet for index, tweet in enumerate(self.tweet_data['text']) if self.tweet_data['SA'][index] < 0]
    get_pct_tweets = lambda no_of_tweets, total_no_of_tweets: no_of_tweets * 100 / total_no_of_tweets
    pct_pos_tweets = get_pct_tweets(len(pos_tweets), len(self.tweet_data['text']))
    pct_neu_tweets = get_pct_tweets(len(neu_tweets), len(self.tweet_data['text']))
    pct_neg_tweets = get_pct_tweets(len(neg_tweets), len(self.tweet_data['text']))
    return pct_pos_tweets, pct_neu_tweets, pct_neg_tweets
