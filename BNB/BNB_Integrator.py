import pandas as pd
from datetime import datetime

tweets1 = pd.read_csv('tweets_1.csv')
tweets2 = pd.read_csv('tweets_2.csv')
tweets = tweets1.append(tweets2)
tweets = tweets.sort_values(by=['Datetime'])
reddit = pd.read_csv('reddit_posts.csv')
reddit = reddit.sort_values(by=['Time_Created'])

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
        if num_tweets == 0:
            like_averages.append(0)
            retweet_averages.append(0)
            reply_averages.append(0)
            quotes_averages.append(0)
        else:
            like_averages.append(num_tweet_likes / num_tweets)
            retweet_averages.append(num_tweet_retweets / num_tweets)
            reply_averages.append(num_tweet_replies / num_tweets)
            quotes_averages.append(num_tweet_replies / num_tweets)
        num_tweets = 1
        num_tweet_likes = row.Likes
        num_tweet_retweets = row.Retweets
        num_tweet_replies = row.Replies
        num_tweet_quotes = row.Quotes

num_posts = 0
post_counts = []

current_hour = '31-07-2020 00'
previous_hour = ''

for i in range(len(tweet_counts) + 1):
    for row in reddit.itertuples():
        if current_hour in row.Time_Created:
            num_posts += 1
    post_counts.append(num_posts)
    h = int(datetime.strptime(current_hour, '%d-%m-%Y %H').strftime('%H')) + 1
    d = int(datetime.strptime(current_hour, '%d-%m-%Y %H').strftime('%d'))
    m = int(datetime.strptime(current_hour, '%d-%m-%Y %H').strftime('%m'))
    y = int(datetime.strptime(current_hour, '%d-%m-%Y %H').strftime('%Y'))
    if h == 24:
        d = d + 1
        h = 0
    if m in (1, 3, 5, 7, 8, 10, 12) and d == 32:
        m = m + 1
        d = 1
    if y % 4 == 0:
        if m == 2 and d == 30:
            m = m + 1
            d = 1
    else:
        if m == 2 and d == 29:
            m = m + 1
            d = 1
    if m in (4, 6, 9, 11) and d == 31:
        m = m + 1
        d = 1
    if m == 13:
        y = y + 1
        m = 1
        d = 1
        h = 1
    if m < 10:
        m = '0' + str(m)
    previous_hour = current_hour
    current_hour = str(d) + '-' + str(m) + '-' + str(y) + ' ' + str(h)
    num_posts = 0

hours.append(current_hour)
tweet_counts.append(num_tweets)
like_averages.append(num_tweet_likes / num_tweets)
retweet_averages.append(num_tweet_retweets / num_tweets)
reply_averages.append(num_tweet_replies / num_tweets)
quotes_averages.append(num_tweet_replies / num_tweets)

df = pd.DataFrame({'Date': hours, 'Number_of_Tweets': tweet_counts, 'Average_Number_of_Likes': like_averages,
                   'Average_Number_of_Retweets': retweet_averages, 'Average_Number_of_Replies': reply_averages,
                   'Average_Number_of_Quotes': quotes_averages, 'Number_of_Reddit_posts': post_counts})

df = df.sort_values(by=['Date'], ascending=False)

df.to_csv('tweets_processed.csv')
