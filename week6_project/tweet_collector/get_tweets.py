import tweepy


API_KEY = "nrOOA8H0iBtdpTUAaleBKtiOW"
API_SECRET = "Eubpi3jHAy37fYqQ78jAxVIhqp6ZvQ3MJyC3lQdrEDbXbGBp6D"


########### MONGODB #############
import pymongo

client = pymongo.MongoClient(host="mongodb", port=27017)
db = client.twitter
collection=db.tweets
#################################

def get_auth_handler():
    """
    Function for handling Twitter Authentication. See course material for 
    instructions on getting your own API Twitter credentials.
    """
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    return auth


def get_full_text(status):
    """Returns the full text of a (re)tweet"""
    try:
        return status.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        return status.full_text


if __name__ == '__main__':
    auth = get_auth_handler()
    api = tweepy.API(auth)

    cursor = tweepy.Cursor(
        api.user_timeline,
        id='elonmusk',
        tweet_mode='extended'
    )

    for status in cursor.items(10):  # 10 tweets
        tweet = {
            'text': get_full_text(status),
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count
        }
        collection.insert_one(tweet)
        #print(tweet)
    for doc in collection.find():
        print('final_print=',doc)



