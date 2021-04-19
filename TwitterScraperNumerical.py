import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwitter
from datetime import datetime

dates = []
current_day = '2021-01-31'
number_of_tweets = 0
tweet_number = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper('Doge since:2011-12-31 until:2020-04-01').get_items()):
    if str(current_day) in str(tweet.date):
        number_of_tweets += 1
    else:
        tweet_number.append(number_of_tweets)
        number_of_tweets = 1
        dates.append(str(current_day))
        current_day = datetime.strptime(str(tweet.date), '%Y-%m-%d %H:%M:%S+00:00').strftime('%Y-%m-%d')

# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame({'Dates': dates, 'Number_of_Tweets': tweet_number})

tweets_df2.to_csv('tweets_jan_2021.csv')
