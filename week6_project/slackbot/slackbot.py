import pyjokes
import requests
from sqlalchemy import create_engine
import logging
from sqlalchemy import text
import pandas as pd


webhook_url = "https://hooks.slack.com/services/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"

### Connect to Postgres ###
pg = create_engine('postgresql://postgres:postgres@postgres_container:5432/tweet_data')
logging.critical("Conect to Postgres ready.")

# The table is 'tweets' 

query="""SELECT * FROM tweets;"""
text_tweet=pd.DataFrame(pg.execute(query))

print('here is the text from postgres table=')
print(text_tweet)

print('one=',text_tweet.iloc[1,0])

### The tweet for slack
data = {'text': text_tweet.iloc[1,0]}
requests.post(url=webhook_url, json = data)









