import pandas as pd
import numpy as np
from datetime import datetime
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

tweets_df = pd.read_csv('tweets_processed2.csv')
prices_df = pd.read_csv('Binance_BNBUSDT_1h.csv')
tweets_df = tweets_df.sort_values(by=['Date'], ascending=True)
tweets_df2 = pd.DataFrame({'Date': tweets_df['Date']})
tweets_df2['Number_of_Tweets'] = tweets_df['Number_of_Tweets'].rolling(3).mean()  # rolling average on 3 data points
tweets_df2['Average_Number_of_Likes'] = tweets_df['Average_Number_of_Likes'].rolling(3).mean()
tweets_df2['Average_Number_of_Retweets'] = tweets_df['Average_Number_of_Retweets'].rolling(3).mean()
tweets_df2['Average_Number_of_Replies'] = tweets_df['Average_Number_of_Replies'].rolling(3).mean()
tweets_df2['Average_Number_of_Quotes'] = tweets_df['Average_Number_of_Quotes'].rolling(3).mean()
tweets_df2['Number_of_Reddit_posts'] = tweets_df['Number_of_Reddit_posts'].rolling(3).mean()
tweets_df2 = tweets_df2.dropna()
tweets_df = tweets_df2.sort_values(by=['Date'], ascending=False)
new_tweets = tweets_df.head(700)
new_prices = prices_df.head(700)

tweets_df = tweets_df[~tweets_df.isin(new_tweets)].dropna()
prices_df = prices_df[~prices_df.isin(new_prices)].dropna()

prices_df = prices_df.drop(prices_df.tail(len(prices_df) - len(tweets_df)).index)

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
    volumes.append(row.Volume_USDT)

df = pd.DataFrame({'Price': prices, 'Volume': volumes, 'Number_of_Tweets': tweet_number,
                   'Average_Number_of_Likes': like_number, 'Average_Number_of_Retweets': retweet_number,
                   'Average_Number_of_Replies': reply_number, 'Average_Number_of_Quotes': quote_number,
                   'Number_of_Reddit_posts': post_number})

train_dataset = df.sample(frac=0.8, random_state=0)
test_dataset = df.drop(train_dataset.index)

train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop('Price')
test_labels = test_features.pop('Price')

normaliser = keras.layers.experimental.preprocessing.Normalization()

normaliser.adapt(np.array(train_features))

model = keras.Sequential([normaliser, keras.layers.Dense(units=1)])

model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.1), loss='mean_absolute_error')

history = model.fit(train_features, train_labels, epochs=100, validation_split=0.2)


#plt.plot(history.history['loss'], label='loss')
#plt.plot(history.history['val_loss'], label='val_loss')
#plt.xlabel('Epoch')
#plt.ylabel('Error (USD)')
#plt.legend()
#plt.show()

test_results['linear_model'] = model.evaluate(test_features, test_labels)

print(model.get_weights())

dnn_model = keras.Sequential([normaliser, keras.layers.Dense(416, activation='relu'),
                              keras.layers.Dense(416, activation='relu'), keras.layers.Dense(1)])

dnn_model.compile(optimizer=tf.optimizers.Adam(0.001), loss='mean_absolute_error')

history2 = dnn_model.fit(train_features, train_labels, validation_split=0.2, epochs=100)

test_results['dnn_model'] = dnn_model.evaluate(test_features, test_labels)


test_predictions_dnn = dnn_model.predict(test_features).flatten()
test_predictions_linear = model.predict(test_features).flatten()

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('True Value [USD]')
ax1.set_ylabel('Predicted Value (DNN) [USD]', color=color)
ax1.scatter(test_labels, test_predictions_dnn, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Predicted Value (Linear) [USD]', color=color)
ax2.scatter(test_labels, test_predictions_linear, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.show()

error = test_predictions_linear - test_labels
plt.hist(error, bins=25)
plt.xlabel('Prediction Error [USD]')
plt.ylabel('Count')
plt.show()

# Test on April to visually see how good model is

tweet_number = []
like_number = []
retweet_number = []
reply_number = []
quote_number = []
post_number = []
prices = []
volumes = []

for row in new_tweets.itertuples():
    tweet_number.append(row.Number_of_Tweets)
    like_number.append(row.Average_Number_of_Likes)
    retweet_number.append(row.Average_Number_of_Retweets)
    reply_number.append(row.Average_Number_of_Replies)
    quote_number.append(row.Average_Number_of_Quotes)
    post_number.append(row.Number_of_Reddit_posts)

for row in new_prices.itertuples():
    prices.append((row.high + row.low) / 2)
    volumes.append(row.Volume_USDT)

df = pd.DataFrame({'Volume': volumes, 'Number_of_Tweets': tweet_number,
                   'Average_Number_of_Likes': like_number, 'Average_Number_of_Retweets': retweet_number,
                   'Average_Number_of_Replies': reply_number, 'Average_Number_of_Quotes': quote_number,
                   'Number_of_Reddit_posts': post_number})

april_predictions_dnn = dnn_model.predict(df).flatten()
april_predictions_linear = model.predict(df).flatten()

num_of_dates = []

for i in range(len(prices)):
    num_of_dates.append(i)

plt.plot(num_of_dates, prices, color='black', label='Actual Price')
plt.plot(num_of_dates, april_predictions_linear, color='red', label='Predicted Price (Linear Model)')
plt.plot(num_of_dates, april_predictions_dnn, color='blue', label='Predicted Price(DNN Model)')
plt.legend(title='Price Predictions of BNB in April 2021')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
