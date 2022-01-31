import pymongo
import time
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging



# Establish a connection to the MongoDB server

client = pymongo.MongoClient(host="mongodb", port=27017)

# Select the database you want to use withing the MongoDB server
db = client.twitter


# time
time.sleep(10)  # seconds


### Connect to Postgres ###
pg = create_engine('postgresql://postgres:postgres@postgres_container:5432/tweet_data', echo=True)

pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
);
''')
logging.critical("Mongo and Postgres connections ready.")
s=SentimentIntensityAnalyzer()
## Print entries and Insert data ##
docs = db.tweets.find()
for doc in docs:
    print(doc['text'])
    score=s.polarity_scores(doc['text'])
    score=score['compound']
    query = "INSERT INTO tweets VALUES (%s, %s);"
    pg.execute(query, (doc['text'], score))







