import pandas as pd
import numpy as np
from datetime import datetime
from textblob import TextBlob
import time

tweets1 = pd.read_csv('tweets_1.csv')
tweets2 = pd.read_csv('tweets_2.csv')
tweets3 = pd.read_csv('tweets_3.csv')
tweets = tweets1.append(tweets2)
tweets = tweets.append(tweets3)
tweets = tweets.sort_values(by=['Datetime'])
tweets = tweets.drop_duplicates()
reddit = pd.read_csv('reddit_posts.csv')
reddit = reddit.sort_values(by=['Time_Created'])

num_tweets = 0
num_tweet_likes = 0
num_tweet_retweets = 0
num_tweet_replies = 0
num_tweet_quotes = 0
total_polarity = 0

hours = []
tweet_counts = []
like_averages = []
retweet_averages = []
reply_averages = []
quotes_averages = []
polarity = []

total_time = 26155

num_posts = 0
post_counts = []
reddit_polarity = 0

current_hour = '13-05-2018 23'
current_hour = int(datetime.strptime(current_hour, '%d-%m-%Y %H').timestamp())
previous_hour = ''
reddit_polarities = []

for i in range(total_time):
    current_hour = datetime.utcfromtimestamp(current_hour).strftime('%Y-%m-%d %H')
    for row in reddit.itertuples():
        if current_hour in row.Time_Created:
            num_posts += 1
            blob = TextBlob(str(row.Content))
            reddit_polarity += blob.sentiment.polarity
    post_counts.append(num_posts)
    reddit_polarities.append(reddit_polarity)
    current_hour = int(datetime.strptime(current_hour, '%Y-%m-%d %H').timestamp())
    current_hour = current_hour + 3600
    num_posts = 0
    reddit_polarity = 0
    print(i)

current_hour = '2018-05-13 23'
current_hour = int(datetime.strptime(current_hour, '%Y-%m-%d %H').timestamp())

dates = tweets['Datetime']
likes = tweets['Likes']
retweets = tweets['Retweets']
replies = tweets['Replies']
quotes = tweets['Quotes']
text = tweets['Text']

for i in range(total_time):
    hours.append(current_hour)
    current_hour = datetime.utcfromtimestamp(current_hour).strftime('%Y-%m-%d %H')
    for n, date in enumerate(dates):
        if current_hour in date:
            num_tweets += 1
            num_tweet_likes += likes[n]
            num_tweet_retweets += retweets[n]
            num_tweet_replies += replies[n]
            num_tweet_quotes += quotes[n]
            blob = TextBlob(text[n])
            total_polarity += blob.sentiment.polarity
    tweet_counts.append(num_tweets)
    if num_tweets == 0:
        like_averages.append(0)
        retweet_averages.append(0)
        reply_averages.append(0)
        quotes_averages.append(0)
        polarity.append(0)
    else:
        like_averages.append(num_tweet_likes / num_tweets)
        retweet_averages.append(num_tweet_retweets / num_tweets)
        reply_averages.append(num_tweet_replies / num_tweets)
        quotes_averages.append(num_tweet_quotes / num_tweets)
        polarity.append(total_polarity / num_tweets)
    current_hour = int(datetime.strptime(current_hour, '%Y-%m-%d %H').timestamp())
    current_hour = current_hour + 3600
    num_tweets = 0
    num_tweet_likes = 0
    num_tweet_retweets = 0
    num_tweet_replies = 0
    num_tweet_quotes = 0
    total_polarity = 0
    print(i)

df = pd.DataFrame({'Date': hours, 'Number_of_Tweets': tweet_counts, 'Average_Number_of_Likes': like_averages,
                   'Average_Number_of_Retweets': retweet_averages, 'Average_Number_of_Replies': reply_averages,
                   'Average_Number_of_Quotes': quotes_averages, 'Number_of_Reddit_posts': post_counts})

df = df.sort_values(by=['Date'], ascending=False)

df.to_csv('tweets_reddit_processed_sentiment.csv')
