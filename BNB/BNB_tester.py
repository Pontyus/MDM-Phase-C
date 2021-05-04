import pandas as pd
from datetime import datetime

tweets = pd.read_csv('tweets_processed2.csv')
prices = pd.read_csv('Binance_BNBUSDT_1h.csv')

for row in tweets.itertuples():
    done = False
    for price in prices.itertuples():
        date = datetime.strptime(price.date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H')
        if date in row.Date:
            done = True
    if not done:
        print(row.Date)
