import pandas as pd
from datetime import datetime

tweets1 = pd.read_csv('tweets1.csv')
tweets2 = pd.read_csv('tweets2.csv')
tweets = tweets1.append(tweets2)
tweets = tweets.sort_values(by=['Datetime'])

current_hour = '2020-07-31 00'
num_tweets = 0
num_tweet_likes = 0
num_tweet_retweets = 0
num_tweet_replies = 0
num_tweet_quotes = 0

hours = []
tweet_counts = []
like_averages = []
retweet_averages = []
reply_averages = []
quotes_averages = []

for row in tweets.itertuples():
    if current_hour in row.Datetime:
        num_tweets += 1
        num_tweet_likes += row.Likes
        num_tweet_retweets += row.Retweets
        num_tweet_replies += row.Replies
        num_tweet_quotes += row.Quotes
    else:
        hours.append(current_hour)
        current_hour = datetime.strptime(row.Datetime, '%Y-%m-%d %H:%M:%S+00:00').strftime('%Y-%m-%d %H')
        tweet_counts.append(num_tweets)
        like_averages.append(num_tweet_likes / num_tweets)
        retweet_averages.append(num_tweet_retweets / num_tweets)
        reply_averages.append(num_tweet_replies / num_tweets)
        quotes_averages.append(num_tweet_replies / num_tweets)

df = pd.DataFrame({'Date': hours, 'Number_of_Tweets': tweet_counts, 'Average_Number_of_Likes': like_averages,
                   'Average_Number_of_Retweets': retweet_averages, 'Average_Number_of_Replies': reply_averages,
                   'Average_Number_of_Quotes': quotes_averages})

df = df.sort_values(by=['Date'], ascending=False)

df.to_csv('tweets_processed.csv')
