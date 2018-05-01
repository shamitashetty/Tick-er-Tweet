# Tick-er-Tweet
*Sentiment analysis of tweets, analyzing stock trends and impact of tweets on the stock market*

<!-- TOC -->

- [Contents](#contents)
- [Objective](#objective)
- [Introduction](#introduction)
- [Description](#description)

    - [Twitter Scraping](#twitter_scraping)
    - [Getting stock data](#get_stock_data)
    - [Preprocessing of tweet and stock data](#data_preprocessing)
    - [Sentiment analysis of tweets](#sentiment_analysis)
    - [Candlestick plot of stock and filtered tweet data](#plotting_data)
    - [Main() function](#main)
    
- [Inference and Path forward](#inference)
- [References](#references)
- [Further reading](#further_reading)
- [Acknowledgment](#acknowledgment)    

<!-- /TOC -->

## Contents
This document describes my final project for BIOF309 Introduction to Python. The code and all supporting files are in my [Tick-er-Tweet GitHub repo](https://github.com/shamitashetty/Tick-er-Tweet)

## Objective
The idea for this project was conceived when I noticed that if Trump mentioned a company within his tweets, their shares would either go up in price if the tweet was positive or drop if the tweet was negative. I decided to make a python script to follow Trump and monitor the companies that he mentioned since the day he was inducted as the POTUS, to see how the tweet affected the price of the company's shares or the general stock market indices. 
The goal of this project is to provide adequate links for scholars who want to research in this domain; and at the same time, be sufficiently accessible for developers who want to integrate sentiment analysis into their applications.The code is flexible enough to be amended for retrieving tweets from other user(s) and data for other stocks. 

## Introduction

The code is divided into five separate classes for easy understanding, editing and calling in the main() function:

![Flowchart](https://github.com/shamitashetty/Tick-er-Tweet/blob/master/img/Flowchart-tick-er-tweet-analysis.svg "Flowchart")

<table border="0">
<tr><th>Name</th><th>Relevant files</th><th>Output</th></tr>
<tr><td>Getting stock data </td><td>main.py</td><td> <a href="https://github.com/shamitashetty/Tick-er-Tweet/tree/master/stockdata"> stockdata</a></td></tr>
<tr><td>Twitter Scraping</td><td> scrape.py get_metadata.py</td><td> <a href="https://github.com/shamitashetty/Tick-er-Tweet/tree/master/tweetdata">tweetdata</a></td></tr>
<tr><td>Preprocessing of tweet and stock data  </td><td>processdata.py</td><td> Text file </td></tr>
<tr><td>Sentiment analysis of tweets </td><td>sentimentanalysis.py</td><td>  Report </td></tr>
<tr><td>Candlestick plot of stock and filtered tweet data</td><td>plots.py</td><td> Text & Figures <a href="https://github.com/shamitashetty/Tick-er-Tweet/tree/master/sampleoutputs">sample outputs</a></td></tr>
</table>


## Description 

   **List of Python3 packages required across all scripts**
   
    pip3 install numpy
    pip3 install pandas
    pip3 install matplotlib
    pip3 install seaborn
    pip3 install tweepy
    pip3 install selenium
    pip3 install quandl
    pip3 install json
    pip3 install plotly
    pip3 install textblob
    
    

   ## Twitter_Scraping
   Twitter makes it hard to get all of a user's tweets (assuming they have more than 3200). This is a way to get around that using Python, Selenium, and Tweepy. 
    Essentially, we will use Selenium to open up a browser and automatically visit Twitter's search page, searching for a single user's tweets on a single day. If we want all tweets from 2015, we will check all 365 days / pages. This would be a nightmare to do manually, so the scrape.py script does it all for you - all you have to do is input a date range and a twitter user handle, and wait for it to finish.
    The scrape.py script collects tweet ids. If you know a tweet's id number, you can get all the information available about that tweet using Tweepy - text, timestamp, number of retweets / replies / favorites, geolocation, etc. Tweepy uses Twitter's API, so you will need to get API keys. Once you have them, you can run the get_metadata.py script.
   
   Requirements: 
   1. Tweepy- `pip3 install tweepy`
   2. Selenium- `pip3 install selenium`
   3. [Twitter Apps Account](https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/)
    
   ## Get_stock_data   
   Yahoo! finance has decommissioned their historical data API and as a result the most popular Python packages for retrieving data have stopped functioning properly. This script uses the Quandl API for retrieving stock data and returns a .xlsx file based on the list of Stock ticker names provided to the query. 📈
   
   Requirements: 
   [Quandl API](https://blog.quandl.com/getting-started-with-the-quandl-api) - `pip3 install quandl`
    
   ## Data_preprocessing
   Performs the basic 'cleaning' and filtering of the .csv and .xlsx files for tweet data and stock data respectively. This script also filters the tweet data to get a dataframe object of tweets mentioning the stocks/ keywords of interest.
    
   ## Sentiment_Analysis
   This script takes the .csv tweet file returns the results of sentiment analysis of all tweets as positive(+1), negative (-1) or neutral(0). It also gives some general information about the trends from the tweet file such as max likes and max retweets.
   
   Requirements:
   [Textblob](https://textblob.readthedocs.io/en/dev/) - `pip3 install textblob`
    
   ## Plotting_data
   The stock data is plotted using the Plotly package in Python3. [plotly.py](https://plot.ly/d3-js-for-python-and-pandas-charts/) is an interactive, browser-based graphing library for Python :sparkles:. You need to create a free account for accessing the online plots but you can also plot data offline using the offline feature in the package.
   
   Requirements: 
    Plotly- `pip3 install plotly`
    
   ## Main()
   Main() function calls the above classes in the specified order and returns the results.
   Running main: 
   
   `python3 main.py "stockdata.xlsx" "indexdata.xlsx" "<quandl-api-key>" "<twitter-user-handle>"`
    
## Inference
   Weak to no correlation between Trump’s tweet sentiment score and the stock index, as multiple factors can affect the stock market including:  
   
   - New policies not mentioned in tweets
   - News about a company’s earnings, acquisitions etc.
   - A switch in investor sentiment in general
   
   Only a short term effect was observed on the stock market values of most companies and they seemed to recover from this slump in the long run.
   
   
 ### **Challenges and Path forward**
  
The sentiment analysis tool has limitations in accurately gauging the sentiment of sarcasm or tweets that don't fall in the category of positive/ negative/ neutral keywords.
   
New features can be added to the script for giving information about the nature of tweets and stock data. Additional data can be gathered from other sources to make the analysis more reliable.

## References 

* #### https://github.com/bpb27/twitter_scraping.git
* #### https://github.com/RodolfoFerro/pandas_twitter
* #### https://plot.ly/python/candlestick-charts/

## Further_Reading
#### [Donald Trump's Tweets Toy With Stocks]( http://fortune.com/2018/04/07/donald-trump-tweets-stock-market/)
#### [Here’s What Happened After Trump Targeted These 9 Companies on Twitter]( https://studentloanhero.com/featured/donald-trump-tweets-targeted-companies/)
#### [The Bankrate Trump Index: How the president’s words affect stocks]( https://www.bankrate.com/investing/the-bankrate-trump-index-how-the-presidents-words-affect-stocks/)
#### [Amazon stock extends fall after Trump tweets ‘concerns’ about U.S. Postal Service, taxes]( https://www.marketwatch.com/story/amazon-shares-keep-falling-after-trump-tweets-concerns-about-us-postal-service-taxes-2018-03-29)
#### [Never Tweet, Mr. President]( https://fivethirtyeight.com/features/never-tweet-mr-president/)
#### [The 425 People, Places and Things Donald Trump Has Insulted on Twitter: A Complete List]( https://www.nytimes.com/interactive/2016/01/28/upshot/donald-trump-twitter-insults.html?mcubz=3&amp;_r=0)


## Acknowledgment
------------
* #### Martin Skarzynski, Michael & Ben
* #### Anup Mathur

Please send any questions/comments to atimahs16 at gmail dot com.  📢

