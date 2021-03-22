import requests
from datetime import datetime
import traceback
import time
import json
import sys
import pandas as pd

username = ""  # put the username you want to download in the quotes
subreddit = "bitcoinmarkets"  # put the subreddit you want to download in the quotes
# leave either one blank to download an entire user's or subreddit's history
# or fill in both to download a specific users history from a specific subreddit

filter_string = None
if username == "" and subreddit == "":
    print("Fill in either username or subreddit")
    sys.exit(0)
elif username == "" and subreddit != "":
    filter_string = f"subreddit={subreddit}"
elif username != "" and subreddit == "":
    filter_string = f"author={username}"
else:
    filter_string = f"author={username}&subreddit={subreddit}"

url = "https://api.pushshift.io/reddit/{}/search?limit=1000&sort=desc&{}&before="

start_time = datetime.utcnow()  # start downloading from most recent post

posts = []


def download(filename, object_type):
    print(f"Saving {object_type}s to {filename}")

    count = 0
    previous_epoch = int(start_time.timestamp())
    while True:
        new_url = url.format(object_type, filter_string) + str(previous_epoch)
        json_text = requests.get(new_url, headers={'User-Agent': "Post Downloader"})
        time.sleep(1)  # pushshift has a rate limit, if you send requests too fast it will start giving error messages
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
                        object_text_lines = object['selftext'].splitlines()
                        object_text_lines_no_comma = [line.replace(',', '') for line in object_text_lines]
                        object_text_rejoined = ' '.join(object_text_lines_no_comma)
                        posts.append([datetime.fromtimestamp(object['created_utc']).strftime("%d-%m-%Y, %H:%M:%S"),
                                      object['title'], object['score'], object['author'], object['num_comments'],
                                      object_text_rejoined])
                    except Exception as err:
                        print(f"Couldn't print post: {object['url']}")
                        print(traceback.format_exc())

        print("Saved {} {}s through {}".format(count, object_type,
                                               datetime.fromtimestamp(previous_epoch).strftime("%d-%m-%Y, %H:%M:%S")))

    print(f"Saved {count} {object_type}s.")

    df = pd.DataFrame(posts, columns=['Time_Created', 'Title', 'Score', 'Author', 'Num_Comments', 'Content'])
    df.to_csv(filename)


download("posts_.csv", "submission")
