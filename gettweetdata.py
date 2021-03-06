import csv
import datetime
import json
import logging
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import tweepy
import zipfile


class ScrapeWeb(object):

  def __init__(self, **kwargs):
    """
    Initialize the class ScrapeWeb
    :param kwargs: [user (String), start_date (datetime), end_date(datetime)]
    """
    self.keys = None
    self.api = None
    self.user = kwargs["user"].lower()
    self.all_data = []
    self.output_file = None
    self.output_file_short = None
    self.start_date = kwargs["start_date"]
    self.end_date = kwargs["end_date"]
    # only edit these if you're having problems
    self.delay = 1
    self.driver = webdriver.Safari()  # options are Chrome() Firefox() Safari()
    # don't mess with this stuff
    self.twitter_ids_filename = '{}/tweetdata/output/all_ids.json'.format(os.getcwd())
    self.days = (self.end_date - self.start_date).days + 1
    self.id_selector ='.time a.tweet-timestamp'
    self.tweet_selector = 'li.js-stream-item'
    self.ids = []
    self.logger = logging.getLogger(kwargs["logger_name"])

  def format_day(self, date):
      day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
      month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
      year = str(date.year)
      return '-'.join([year, month, day])

  def form_url(self, since, until):
      p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
      p2 = "{}%20since%3A{}%20until%3A{}include%3Aretweets&src=typd".format(self.user, since, until)
      return p1 + p2

  def increment_day(self, date, i):
      return date + datetime.timedelta(days=i)

  def scrape_data_from_twitter(self):
    """
    Scrape data from twitter for a given user fromo start_date till end_date
    :return:
    """
    self.logger.info("Scraping data from Twitter.")
    for day in range(self.days):
      d1 = self.format_day(self.increment_day(self.start_date, 0))
      d2 = self.format_day(self.increment_day(self.start_date, 1))
      url = self.form_url(d1, d2)
      self.logger.info("Url = {}".format(url))
      self.driver.get(url)
      sleep(self.delay)
      try:
        found_tweets = self.driver.find_elements_by_css_selector(self.tweet_selector)
        increment = 10
        while len(found_tweets) >= increment:
          self.logger.info('Scrolling down to load more tweets')
          self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
          sleep(self.delay)
          found_tweets = self.driver.find_elements_by_css_selector(self.tweet_selector)
          increment += 10
        self.logger.info('{} tweets found, {} total'.format(len(found_tweets), len(self.ids)))
        for tweet in found_tweets:
          try:
            id = tweet.find_element_by_css_selector(self.id_selector).get_attribute('href').split('/')[-1]
            self.ids.append(id)
          except StaleElementReferenceException as e:
            self.logger.error('Lost element reference', tweet)
      except NoSuchElementException:
        self.logger.info('No tweets on this day')
      self.start_date = self.increment_day(self.start_date, 1)

  def write_twitter_data_to_file(self):
    """
    Write the data extracted from twitter to a file
    :return:
    """
    self.logger.info("Writing the extracted twitter data to a file")
    try:
      with open(self.twitter_ids_filename) as f:
        all_ids = self.ids + json.load(f)
        data_to_write = list(set(all_ids))
        self.logger.debug('tweets found on this scrape: ', len(self.ids))
        self.logger.debug('total tweet count: ', len(data_to_write))
    except FileNotFoundError:
      with open(self.twitter_ids_filename, 'w') as f:
        all_ids = self.ids
        data_to_write = list(set(all_ids))
        self.logger.debug('tweets found on this scrape: ', len(self.ids))
        self.logger.debug('total tweet count: ', len(data_to_write))

    with open(self.twitter_ids_filename, 'w') as outfile:
        json.dump(data_to_write, outfile)
    self.logger.info('All done here')

  def get_tweets(self):
    """
    Get tweets for a given user from start_date till the end_date
    :return:
    """
    try:
      self.scrape_data_from_twitter()
      self.write_twitter_data_to_file()
    finally:
      self.driver.close()


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
    self.tweetdata_input_path = '{}/tweetdata/input'.format(os.getcwd())
    self.tweetdata_output_path = '{}/tweetdata/output'.format(os.getcwd())
    self.logger = logging.getLogger(kwargs["logger_name"])

  def collect_all_metadata(self):
    """
    Collect all metadata from twitter for a given user
    :return:
    """
    self.user = self.user.lower()
    with open('{}/all_ids.json'.format(self.tweetdata_output_path)) as f:
      ids = json.load(f)
    self.logger.info('Total ids: {}'.format(len(ids)))
    limit = len(ids)
    for id in range(0, limit, 100):
      self.logger.info('Currently getting {} - {}'.format(id, id + 100))
      sleep(6)  # needed to prevent hitting API rate limit
      id_batch = ids[id:id + 100]
      tweets = self.api.statuses_lookup(id_batch)
      for tw in tweets:
        self.all_data.append(dict(tw._json))
    self.logger.info('Metadata collection complete')

  def connect_to_twitter_API(self):
    """
    Connect to Twitter API
    :return:
    """
    self.logger.info("Connecting to twitter API")
    auth = tweepy.OAuthHandler(self.keys['consumer_key'], self.keys['consumer_secret'])
    auth.set_access_token(self.keys['access_token'], self.keys['access_token_secret'])
    self.api = tweepy.API(auth)

  def create_csv_of_json_master_file(self):
    """
    Create a csv of json master file
    :return:
    """
    self.logger.info("Creating csv of master json file")
    with open(self.output_file_short) as master_file:
      data = json.load(master_file)
      fields = ["favorite_count", "source", "text", "in_reply_to_screen_name", "is_retweet", "created_at",
                "retweet_count", "id_str"]
      f = csv.writer(open('{}/{}.csv'.format(self.tweetdata_output_path, self.user), 'w'))
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
    self.output_file = '{}/all_ids.json'.format(self.tweetdata_output_path)
    self.output_file_short = '{}/{}_short.json'.format(self.tweetdata_output_path, self.user)
    compression = zipfile.ZIP_DEFLATED
    self.logger.info('Creating master json file')
    with open(self.output_file, 'w') as outfile:
      json.dump(self.all_data, outfile)
    self.logger.info('Creating ziped master json file')
    zf = zipfile.ZipFile('{}/{}.zip'.format(self.tweetdata_output_path, self.user), mode='w')
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
    self.logger.info('Creating minimized json master file')
    with open(self.output_file_short, 'w') as outfile:
      json.dump(results, outfile)

  def get_api_keys(self):
    """
    Get API keys from api_keys.json file
    :return:
    """
    with open('{}/api_keys.json'.format(self.tweetdata_input_path)) as f:
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
