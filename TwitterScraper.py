import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwitter

# Creating list to append tweet data to
tweets_list2 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper('Bitcoin since:2020-06-01 until:2020-07-31').get_items()):
    if i > 10000:
        break
    tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.username])

# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

print(tweets_df2)
