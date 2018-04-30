# TrumpTweetTicker
*Sentiment analysis of tweets, analyzing stock trends and impact of tweets on the stock market*

<!-- TOC -->

- [Contents](#Contents)
- [Objective](#Objective)
- [Introduction](#Introduction)
- [Description](#Description)
    - [Twitter Scraping](#Twitter_Scraping)
    - [Getting stock data](#Get_stock_data)
    - [Preprocessing of tweet and stock data](#Data_preprocessing)
    - [Sentiment analysis of tweets](#Sentiment_Analysis)
    - [Candlestick plot of stock and filtered tweet data](#Plotting_data)
    - [Main() function](#Main())
- [Inference and Path forward](#Inference)
- [References](#References)
- [Acknowledgment](#Acknowledgment)    

<!-- /TOC -->

## Contents
This document describes my final project for BIOF309 Introduction to Python. The code and all supporting files are in my [TweetAnalysis GitHub repo](https://github.com/shamitashetty/TweetAnalysis)

## Objective
The idea for this project was conceived when I noticed that if Trump mentioned a company within his tweets, their shares would either go up in price if the tweet was positive or drop if the tweet was negative. I decided to make a python script to follow Trump and monitor the companies that he mentioned since the day he was inducted as the POTUS, to see how the tweet affected the price of the company's shares or the general stock market indices. 
The goal of this repository is to provide adequate links for scholars who want to research in this domain; and at the same time, be sufficiently accessible for developers who want to integrate sentiment analysis into their applications.The code is flexible enough to be amended for retrieving tweets from other user(s) and data for other stocks. 

## Introduction

The code is divided into six separate classes for easy understanding, editing and calling in the main() function:

<table border="0">
<tr><th>Name</th><th>Relevant files</th></tr>Contains</th></tr>
<tr><td>Twitter Scraping</td><td> atimahs16@gmail.com</td></tr>
<tr><td>Getting stock data </td><td>anupmath@gmail.com</td></tr>
<tr><td>Preprocessing of tweet and stock data  </td><td>anupmath@gmail.com</td></tr>
<tr><td>Sentiment analysis of tweets </td><td>anupmath@gmail.com</td></tr>
<tr><td>Candlestick plot of stock and filtered tweet data</td><td>anupmath@gmail.com</td></tr>
<tr><td>Main() function</td><td>anupmath@gmail.com</td></tr>
</table>

|Name    | Relevant files | Contains|
|:------------:|:---:|:---------:|
| Twitter Scraping  | Main source   | Everything     |
| Getting stock data     | Python script | Text & Code    |
| Preprocessing of tweet and stock data   | Report        | Text & Figures |
| Sentiment analysis of tweets     | Report        | Text & Figures |
| Candlestick plot of stock and filtered tweet data   | Report        | Text & Figures |
| Main() function calls the above classes and gives the results  | Report        | Text & Figures |


## Description 
   ## Twitter_Scraping
   Twitter makes it hard to get all of a user's tweets (assuming they have more than 3200). This is a way to get around that using Python, Selenium, and Tweepy. 
    Essentially, we will use Selenium to open up a browser and automatically visit Twitter's search page, searching for a single user's tweets on a single day. If we want all tweets from 2015, we will check all 365 days / pages. This would be a nightmare to do manually, so the scrape.py script does it all for you - all you have to do is input a date range and a twitter user handle, and wait for it to finish.
    The scrape.py script collects tweet ids. If you know a tweet's id number, you can get all the information available about that tweet using Tweepy - text, timestamp, number of retweets / replies / favorites, geolocation, etc. Tweepy uses Twitter's API, so you will need to get API keys. Once you have them, you can run the get_metadata.py script.
    Requirements: 
    1. Tweepy- `pip3 install tweepy`
    2. Selenium- `pip3 install selenium`
    3. [Twitter Apps Account] (https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/)
    
   ##Get_stock_data
    Yahoo! finance has decommissioned their historical data API and as a result the most popular Python packages for retrieving data have stopped functioning properly. This script uses the Quandl API for retrieving stock data and retruns a .csv file based on the list of Stock ticker names provided to the query.
    Requirements: 
    [Quandl API] (https://blog.quandl.com/getting-started-with-the-quandl-api) - `pip3 install quandl`
    
   ##Data_preprocessing
    Performs the basic 'cleaning' of the .csv and .xlsx files for tweet data and stock data respectively. This script also filters the tweet data to get a dataframe object of tweets mentioning the stocks/ keywords of interest.
    
   ##Sentiment_Analysis
    This script takes the preprocessed csv tweet file returns the results of sentiment analysis of all tweets as positive(+1), negative (-1) or neutral(0). It also gives some general information about the trends from the tweet file such as max likes and max retweets.
    Requirements:
    [Textblob] (https://textblob.readthedocs.io/en/dev/) - `pip3 install textblob`
    
   ##Plotting_data
    The stock data is plotted using the [Plotly] package in Python3. [plotly.py](https://plot.ly/d3-js-for-python-and-pandas-charts/) is an interactive, browser-based graphing library for Python :sparkles:. You need to create a free account for accessing the online plots but you can also plot data offline using the offline feature in the package.
    Requirements: 
    Plotly- `pip3 install plotly`
    
   ##Main()
   Main() function calls the above classes in the specified order and returns the results.
    

## References 

Liu, Bing. "Sentiment analysis and opinion mining." Synthesis lectures on human language technologies 5.1 (2012): 1-167. [[pdf]](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.244.9480&rep=rep1&type=pdf)

Vinodhini, G., and R. M. Chandrasekaran. "Sentiment analysis and opinion mining: a survey." International Journal 2.6 (2012): 282-292. [[pdf]](http://www.dmi.unict.it/~faro/tesi/sentiment_analysis/SA2.pdf)

Medhat, Walaa, Ahmed Hassan, and Hoda Korashy. "Sentiment analysis algorithms and applications: A survey." Ain Shams Engineering Journal 5.4 (2014): 1093-1113. [[pdf]](http://www.sciencedirect.com/science/article/pii/S2090447914000550)

<strong>Output</strong>
```python
Emoticons: {'positive': 0.33, 'negative': 0.66}
DictionaryTest: {'positive': 0.46153846153846156, 'negative': 0.5384615384615384}
Hashtags:  {'positive': 0.38, 'negative': 0.62}
```
Progress
--------
* <span style="color:green;">Emoticons: This class uses emoticons detection to classify the passed string as positive or negative</span>
* <span style="color:green;">DictionaryTest: This class uses a set of English words and their subjectivity to give a score to a string</span>
* <span style="color:green;">hashtags: This class extracts hashtags from the string sent and calculates the sentiment based on a trained dataset</span>
* AllCaps
* ElongatedWords
* Negation
* Punctuation

Social Network APIs
---------------
* Twitter Search API
* Yahoo Fnance API
* Google Finance API

Team Members
------------
<table border="0">
<tr><th>Name</th><th>Email</th></tr>
<tr><td>Shamitha Shetty</td><td> atimahs16@gmail.com</td></tr>
<tr><td>Anup Mathur</td><td>anupmath@gmail.com</td></tr>
</table>


