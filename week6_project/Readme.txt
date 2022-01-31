

In this project a data pippeline that collect tweets and stores them in a database is build. Next, the tweets is analyzed and stored in a second database. Finally, a choos one is published on Slack.


Install Docker

Build a data pipeline with docker-compose
-compose.yml

Collect Tweets and store Tweets in Mongo DB
-tweet_collector

Create an ETL job transporting data from MongoDB to PostgreSQL
-etl_job

Build a Slack bot that publishes selected tweets
-slackbot
