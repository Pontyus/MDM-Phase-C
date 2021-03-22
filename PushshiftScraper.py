import pandas as pd
import numpy as np
import requests

subreddit = 'bitcoinmarkets'
limit = 10000
timeframe = 'all'  # hour, day, week, month, year, all
listing = 'new'  # controversial, best, hot, new, random, rising, top


def get_reddit(sub, order, lim, frame):
    try:
        base_url = f'https://www.reddit.com/r/{sub}/{order}.json?limit={lim}&t={frame}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
    except:
        print('Error')
    return request.json()


def get_post_titles(r):  # get a list of post titles
    postings = []
    for post in r['data']['children']:
        x = post['data']['title']
        postings.append(x)
    return postings


def get_results(r):  # get a df with title, url, score and number of comments
    dictionary = {}
    for post in r['data']['children']:
        dictionary[post['data']['title']] = {'url': post['data']['url'], 'score': post['data']['score'],
                                             'comments': post['data']['num_comments']}
    df = pd.DataFrame.from_dict(dictionary, orient='index')
    return df


result = get_reddit(subreddit, listing, limit, timeframe)
# posts = get_post_titles(result)
# print(posts)

df1 = get_results(result)
print(df1)
