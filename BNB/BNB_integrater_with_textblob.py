import pandas as pd
from datetime import datetime
from textblob import TextBlob

tweets1 = pd.read_csv('tweets1.csv')
tweets2 = pd.read_csv('tweets2.csv')
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
total_polarity = 0

hours = []
tweet_counts = []
like_averages = []
retweet_averages = []
reply_averages = []
quotes_averages = []
polarity = []

for row in tweets.itertuples():
    if current_hour in row.Datetime:
        num_tweets += 1
        num_tweet_likes += row.Likes
        num_tweet_retweets += row.Retweets
        num_tweet_replies += row.Replies
        num_tweet_quotes += row.Quotes
        blob = TextBlob(row.Text)
        total_polarity += blob.sentiment.polarity
    else:
        hours.append(current_hour)
        current_hour = datetime.strptime(row.Datetime, '%Y-%m-%d %H:%M:%S+00:00').strftime('%Y-%m-%d %H')
        tweet_counts.append(num_tweets)
        like_averages.append(num_tweet_likes / num_tweets)
        retweet_averages.append(num_tweet_retweets / num_tweets)
        reply_averages.append(num_tweet_replies / num_tweets)
        quotes_averages.append(num_tweet_replies / num_tweets)
        polarity.append(total_polarity / num_tweets)
        num_tweets = 1
        num_tweet_likes = row.Likes
        num_tweet_retweets = row.Retweets
        num_tweet_replies = row.Replies
        num_tweet_quotes = row.Quotes
        blob = TextBlob(row.Text)
        total_polarity = blob.sentiment.polarity

last_hour = current_hour

num_posts = 0
post_counts = []
reddit_polarity = 0
reddit_polarities = []
reddit_hours = []

current_hour = '31-07-2020 00'

for i in range(len(tweet_counts) + 1):
    for row in reddit.itertuples():
        if current_hour in row.Time_Created:
            num_posts += 1
            blob = TextBlob(str(row.Content))
            reddit_polarity += blob.sentiment.polarity
    post_counts.append(num_posts)
    if num_posts > 0:
        reddit_polarities.append(reddit_polarity / num_posts)
    else:
        reddit_polarities.append(0)
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
        h = 0
    if m < 10:
        m = '0' + str(m)
    reddit_hours.append(current_hour)
    current_hour = str(d) + '-' + str(m) + '-' + str(y) + ' ' + str(h)
    num_posts = 0
    reddit_polarity = 0

hours.append(last_hour)
tweet_counts.append(num_tweets)
like_averages.append(num_tweet_likes / num_tweets)
retweet_averages.append(num_tweet_retweets / num_tweets)
reply_averages.append(num_tweet_replies / num_tweets)
quotes_averages.append(num_tweet_replies / num_tweets)
polarity.append(total_polarity / num_tweets)

df = pd.DataFrame({'Date': hours, 'Reddit_Date': reddit_hours, 'Number_of_Tweets': tweet_counts, 'Average_Number_of_Likes': like_averages,
                   'Average_Number_of_Retweets': retweet_averages, 'Average_Number_of_Replies': reply_averages,
                   'Average_Number_of_Quotes': quotes_averages, 'Number_of_Reddit_posts': post_counts,
                   'Average_Twitter_Sentiment': polarity, 'Average_Reddit_Sentiment': reddit_polarities})

df = df.sort_values(by=['Date'], ascending=False)

df.to_csv('tweets_reddit_processed_sentiment.csv')
