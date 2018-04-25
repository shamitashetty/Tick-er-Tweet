import tweepy
import json
import csv
import zipfile
from time import sleep


class GetMetaData(object):

  def __init__(self, **kwargs):
    """
    Initialize the class GetMetaData
    :param kwargs: [user (String)]
    """
    self.keys = None
    self.api = None
    self.user = kwargs["user"]
    self.all_data = []
    self.output_file = None
    self.output_file_short = None

  def collect_all_metadata(self):
    """
    Collect all metadata from twitter for a given user
    :return:
    """
    self.user = self.user.lower()
    with open('all_ids.json') as f:
      ids = json.load(f)
    print('total ids: {}'.format(len(ids)))
    limit = len(ids)
    for id in range(0, limit, 100):
      print('currently getting {} - {}'.format(id, id + 100))
      sleep(6)  # needed to prevent hitting API rate limit
      id_batch = ids[id:id + 100]
      tweets = self.api.statuses_lookup(id_batch)
      for tw in tweets:
        self.all_data.append(dict(tw._json))
    print('metadata collection complete')

  def connect_to_twitter_API(self):
    """
    Connect to Twitter API
    :return:
    """
    auth = tweepy.OAuthHandler(self.keys['consumer_key'], self.keys['consumer_secret'])
    auth.set_access_token(self.keys['access_token'], self.keys['access_token_secret'])
    self.api = tweepy.API(auth)

  def create_csv_of_json_master_file(self):
    """
    Create a csv of json master file
    :return:
    """
    with open(self.output_file_short) as master_file:
      data = json.load(master_file)
      fields = ["favorite_count", "source", "text", "in_reply_to_screen_name", "is_retweet", "created_at",
                "retweet_count", "id_str"]
      print('creating CSV version of minimized json master file')
      f = csv.writer(open('{}.csv'.format(self.user), 'w'))
      f.writerow(fields)
      for x in data:
        f.writerow(
          [x["favorite_count"], x["source"], x["text"], x["in_reply_to_screen_name"], x["is_retweet"], x["created_at"],
           x["retweet_count"], x["id_str"]])

  def create_master_json_file(self):
    """
    Create master json file
    :return:
    """
    self.output_file = '{}.json'.format(self.user)
    self.output_file_short = '{}_short.json'.format(self.user)
    compression = zipfile.ZIP_DEFLATED
    print('creating master json file')
    with open(self.output_file, 'w') as outfile:
      json.dump(self.all_data, outfile)
    print('creating ziped master json file')
    zf = zipfile.ZipFile('{}.zip'.format(self.user), mode='w')
    zf.write(self.output_file, compress_type=compression)
    zf.close()

  def create_minimized_json_master_file(self):
    """
    Create minimised json master file
    :return:
    """
    results = []
    with open(self.output_file) as json_data:
      data = json.load(json_data)
      for entry in data:
        t = {
          "created_at": entry["created_at"],
          "text": entry["text"],
          "in_reply_to_screen_name": entry["in_reply_to_screen_name"],
          "retweet_count": entry["retweet_count"],
          "favorite_count": entry["favorite_count"],
          "source": self.get_source(entry),
          "id_str": entry["id_str"],
          "is_retweet": self.is_retweet(entry)
        }
        results.append(t)
    print('creating minimized json master file')
    with open(self.output_file_short, 'w') as outfile:
      json.dump(results, outfile)

  def get_api_keys(self):
    """
    Get API keys from api_keys.json file
    :return:
    """
    with open('api_keys.json') as f:
      self.keys = json.load(f)

  def get_metadata(self):
    """
    Get metadata from Twitter and write it to a json file and csv file
    :return:
    """
    self.get_api_keys()
    self.connect_to_twitter_API()
    self.collect_all_metadata()
    self.create_master_json_file()
    self.create_minimized_json_master_file()
    self.create_csv_of_json_master_file()

  def get_source(self, entry):
    if '<' in entry["source"]:
      return entry["source"].split('>')[1].split('<')[0]
    else:
      return entry["source"]

  def is_retweet(self, entry):
    return 'retweeted_status' in entry.keys()
