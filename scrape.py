from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import json
import datetime
import os

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
    self.driver = webdriver.Firefox()  # options are Chrome() Firefox() Safari()
    # don't mess with this stuff
    self.twitter_ids_filename = '{}/tweetdata/all_ids.json'.format(os.getcwd())
    self.days = (self.end_date - self.start_date).days + 1
    self.id_selector ='.time a.tweet-timestamp'
    self.tweet_selector = 'li.js-stream-item'
    self.ids = []

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
    for day in range(self.days):
      d1 = self.format_day(self.increment_day(self.start_date, 0))
      d2 = self.format_day(self.increment_day(self.start_date, 1))
      url = self.form_url(d1, d2)
      print(url)
      print(d1)
      self.driver.get(url)
      sleep(self.delay)
      try:
        found_tweets = self.driver.find_elements_by_css_selector(self.tweet_selector)
        increment = 10
        while len(found_tweets) >= increment:
            print('scrolling down to load more tweets')
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(self.delay)
            found_tweets = self.driver.find_elements_by_css_selector(self.tweet_selector)
            increment += 10
        print('{} tweets found, {} total'.format(len(found_tweets), len(self.ids)))
        for tweet in found_tweets:
          try:
              id = tweet.find_element_by_css_selector(self.id_selector).get_attribute('href').split('/')[-1]
              self.ids.append(id)
          except StaleElementReferenceException as e:
              print('lost element reference', tweet)
      except NoSuchElementException:
          print('No tweets on this day')
      self.start_date = self.increment_day(self.start_date, 1)

  def write_twitter_data_to_file(self):
    """
    Write the data extracted from twitter to a file
    :return:
    """
    try:
      with open(self.twitter_ids_filename) as f:
        all_ids = self.ids + json.load(f)
        data_to_write = list(set(all_ids))
        print('tweets found on this scrape: ', len(self.ids))
        print('total tweet count: ', len(data_to_write))
    except FileNotFoundError:
      with open(self.twitter_ids_filename, 'w') as f:
        all_ids = self.ids
        data_to_write = list(set(all_ids))
        print('tweets found on this scrape: ', len(self.ids))
        print('total tweet count: ', len(data_to_write))

    with open(self.twitter_ids_filename, 'w') as outfile:
        json.dump(data_to_write, outfile)
    print('all done here')

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