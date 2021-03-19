import pandas as pd
import numpy as np
import praw

reddit = praw.Reddit(client_id='8M8-mBFoIzQqbQ', client_secret='Qcqac72dM6trs_Nq3Yr6XecCKC-JJg', user_agent='Scraper')

posts = []

bitcoin_markets = reddit.subreddit('BitcoinMarkets')
for post in bitcoin_markets.new(limit=10000):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url,
                  post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts, columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
print(posts)
