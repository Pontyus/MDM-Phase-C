import pandas as pd
from datetime import datetime

tweets = pd.read_csv('tweets_processed.csv')
prices = pd.read_csv('Bitstamp_LTCUSD_1h.csv')

for row in prices.itertuples():
    done = False
    for price in tweets.itertuples():
        date = str(price.Date)
        if date in row.date:
            done = True
    if not done:
        print(row.date)

for row in tweets.itertuples():
    done = False
    for price in prices.itertuples():
        date = datetime.strptime(price.date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H')
        if date in row.Date:
            done = True
    if not done:
        print(row.Date)
