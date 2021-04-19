import requests
from datetime import datetime
import traceback
import time
import json
import sys
import pandas as pd
from datetime import datetime

subreddits = ['altcoins', 'cryptocurrency', 'cryptocurrencytrading', 'bitcoinmarkets', 'cryptomarkets',
              'crypto_currency_news', 'cryptotechnology', 'crypto']
url = "https://api.pushshift.io/reddit/{}/search?q=doge|dogecoin&limit=1000&sort=desc&{}&before="
# put crypto name/ticker in url

start_time = datetime.utcnow()  # start downloading from most recent post

posts = []
dates = []


def download(filename, object_type):
    count = 0
    for subreddit in subreddits:
        filter_string = f"subreddit={subreddit}"
        current_day = str(datetime.today().strftime('%Y-%m-%d'))
        number_of_posts = 0
        print(f"Saving {object_type}s to {filename}")

        previous_epoch = int(start_time.timestamp())
        while True:
            new_url = url.format(object_type, filter_string) + str(previous_epoch)
            json_text = requests.get(new_url, headers={'User-Agent': "Post Downloader"})
            time.sleep(1)
            # pushshift has a rate limit, if you send requests too fast it will start giving error messages
            try:
                json_data = json_text.json()
            except json.decoder.JSONDecodeError:
                time.sleep(1)
                continue

            if 'data' not in json_data:
                break
            objects = json_data['data']
            if len(objects) == 0:
                break

            for object in objects:
                previous_epoch = object['created_utc'] - 1  # go back 1 second from last entry and iterate
                count += 1
                if object_type == 'submission':
                    if object['is_self']:
                        if 'selftext' not in object:
                            continue
                        try:
                            if str(current_day) in str(
                                    datetime.fromtimestamp(object['created_utc']).strftime('%Y-%m-%d')):
                                number_of_posts += 1
                            else:
                                posts.append(number_of_posts)
                                number_of_posts = 1
                                dates.append(str(current_day))
                                current_day = str(datetime.fromtimestamp(object['created_utc']).strftime('%Y-%m-%d'))

                        except Exception as err:
                            print(f"Couldn't print post: {object['url']}")
                            print(traceback.format_exc())

            print("Saved {} {}s through {}".format(count, object_type,
                                                   datetime.fromtimestamp(previous_epoch).strftime(
                                                       "%d-%m-%Y, %H:%M:%S")))

        print(f"Saved {count} {object_type}s.")

    df = pd.DataFrame({'Dates': dates, 'Number_of_Posts': posts})
    aggregates = {'Number_of_Posts': 'sum'}
    df1 = df.groupby(df['Dates']).aggregate(aggregates)
    df2 = df1[(df1 != 0).all(1)]
    df2.to_csv(filename)


download("posts_.csv", "submission")
