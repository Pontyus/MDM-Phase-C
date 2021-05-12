import pandas as pd
import matplotlib.pyplot as plt

tweets_df = pd.read_csv('tweets_processed.csv')
prices_df = pd.read_csv('Bitstamp_LTCUSD_1h.csv')

tweet_number = []
like_number = []
retweet_number = []
reply_number = []
quote_number = []
post_number = []
prices = []
volumes = []
test_results = {}

for row in tweets_df.itertuples():
    tweet_number.append(row.Number_of_Tweets)
    like_number.append(row.Average_Number_of_Likes)
    retweet_number.append(row.Average_Number_of_Retweets)
    reply_number.append(row.Average_Number_of_Replies)
    quote_number.append(row.Average_Number_of_Quotes)
    post_number.append(row.Number_of_Reddit_posts)

for row in prices_df.itertuples():
    prices.append((row.high + row.low) / 2)
    volumes.append(row.Volume_USD)

n = 0
number_of_hours = []

for i in range(len(prices)):
    n = n + 1
    number_of_hours.append(n)

plt.plot(number_of_hours, prices, color='black', label='LTC Price')
plt.xlabel('Hour')
plt.ylabel('Price')
plt.show()

number_of_hours2 = []
n = 0
for i in range(200):
    n = n + 1
    number_of_hours2.append(n)
number_of_hours3 = []
n = 0
for i in range(100):
    n = n + 1
    number_of_hours3.append(n)
number_of_hours4 = []
n = 0
for i in range(1000):
    n = n + 1
    number_of_hours4.append(n)
number_of_hours5 = []
n = 0
for i in range(500):
    n = n + 1
    number_of_hours5.append(n)

plt.plot(number_of_hours2, prices[12600:12800], color='black', label='LTC Price')
plt.xlabel('Hour')
plt.ylabel('Price')
plt.show()

plt.plot(number_of_hours3, prices[10000:10100], color='black', label='LTC Price')
plt.xlabel('Hour')
plt.ylabel('Price')
plt.show()

plt.plot(number_of_hours4, prices[8500:9500], color='black', label='LTC Price')
plt.xlabel('Hour')
plt.ylabel('Price')
plt.show()

plt.plot(number_of_hours5, prices[18000:18500], color='black', label='LTC Price')
plt.xlabel('Hour')
plt.ylabel('Price')
plt.show()
