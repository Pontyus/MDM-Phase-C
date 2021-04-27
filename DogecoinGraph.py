import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

dates = []
posts = []
highs = []
lows = []
averages = []
opens = []
closes = []
volumes = []
marketcaps = []
num_of_dates = []
done = False

reddit_data = pd.read_csv('Dogecoin_twitter2.csv')
price_data = pd.read_csv('Dogecoin_prices.csv')

for row in price_data.itertuples():
    dates.append(datetime.strptime(row.Date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
    highs.append(row.High)
    lows.append(row.Low)
    averages.append((row.High + row.Low) / 2)
    opens.append(row.Open)
    closes.append(row.Close)
    volumes.append(row.Volume)
    marketcaps.append(row.Marketcap)

for date in dates:
    done = False
    for row in reddit_data.itertuples():
        if row.Dates == date:
            posts.append(row.Number_of_Tweets)
            done = True
    if not done:
        posts.append(0)

for i in range(len(dates)):
    num_of_dates.append(i)

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Day')
ax1.set_ylabel('Number of posts', color=color)
ax1.plot(num_of_dates, posts, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Dogecoin price', color=color)  # we already handled the x-label with ax1
ax2.plot(num_of_dates, averages, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
