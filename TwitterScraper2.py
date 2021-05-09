import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwitter

# Creating list to append tweet data to
tweets_list2 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper('LTC since:2018-05-14 until:2020-05-05').get_items()):
    if i > 2000000:
        break
    else:
        tweet_text_lines = tweet.content.splitlines()
        tweet_text_lines_no_comma = [line.replace(',', '') for line in tweet_text_lines]
        tweet_text_rejoined = ' '.join(tweet_text_lines_no_comma)
        tweets_list2.append([tweet.date, tweet.id, tweet.user.username, tweet.likeCount, tweet.retweetCount,
                             tweet.replyCount, tweet.quoteCount, tweet_text_rejoined])

# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet_ID', 'Username', 'Likes', 'Retweets', 'Replies',
                                                 'Quotes', 'Text'])

tweets_df2.to_csv('tweets_.csv')
