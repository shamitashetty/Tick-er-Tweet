#Get tweet data from csv

from textblob import TextBlob
import re

tweetdata= pd.read_csv('realdonaldtrump.csv')

del tweetdata['in_reply_to_screen_name']
# print(tweetdata.head())
print(tweetdata.head())
print(tweetdata.columns)

# We extract the tweet with more FAVs and more RTs:

fav_max = np.max(tweetdata['favorite_count'])
rt_max  = np.max(tweetdata['retweet_count'])

fav = tweetdata[tweetdata.favorite_count == fav_max].index[0]
rt  = tweetdata[tweetdata.retweet_count == rt_max].index[0]

# Max FAVs:
print("The tweet with most likes is: \n{}".format(tweetdata['text'][fav]))
print("Number of likes: {}".format(fav_max))


# Max RTs:
print("The tweet with most retweets is: \n{}".format(tweetdata['text'][rt]))
print("Number of retweets: {}".format(rt_max))

# Convert created_at column to
tweetdata['created_at']= pd.to_datetime(tweetdata['created_at'])
# print(type(tweetdata['created_at']))
# print(tweetdata['created_at'].head())
tweetdata.set_index('created_at', inplace=True)
tweetdata.index.name= ['Date']

print(tweetdata.index)
print(tweetdata.head(2))

#Plot likes and retweets over time
tfav = pd.Series(data=tweetdata['favorite_count'].values, index=tweetdata.index)
tret = pd.Series(data=tweetdata['retweet_count'].values, index=tweetdata.index)

# Likes vs retweets visualization:
tfav.plot(figsize=(16,4), label="Likes", legend=True)
tret.plot(figsize=(16,4), label="Retweets", legend=True);
plt.show()

#Sentiment analysis of tweets
def clean_tweet(tweet):
  '''
  Utility function to clean the text in a tweet by removing
  links and special characters using regex.
  '''
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analyze_sentiment(tweet):
  '''
  Utility function to classify the polarity of a tweet
  using textblob.
  '''
  analysis = TextBlob(clean_tweet(tweet))
  if analysis.sentiment.polarity > 0:
    return 1
  elif analysis.sentiment.polarity == 0:
    return 0
  else:
    return -1

# Create a column with the result of the analysis:
tweetdata['SA'] = np.array([ analyze_sentiment(tweet) for tweet in tweetdata['text'] ])

# We display the updated dataframe with the new column:
print(tweetdata.head(5))

# Construct lists with classified tweets
pos_tweets = [ tweet for index, tweet in enumerate(tweetdata['text']) if tweetdata['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(tweetdata['text']) if tweetdata['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(tweetdata['text']) if tweetdata['SA'][index] < 0]

# Print percentages of each type
print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(tweetdata['text'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(tweetdata['text'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(tweetdata['text'])))
