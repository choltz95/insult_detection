import pickle
import math
import numpy
from sklearn import ensemble, linear_model,svm

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import oauthHandler
import json
from time import sleep
from datetime import datetime
from dateutil.parser import parse
import re
import dataset

import classify

tweetDict = dict() 
parsedTweets = 0
bad_tweets = []
neutral_tweets = []
db = dataset.connect("sqlite:///tweets.db")

#Handeling tweets, updating dict, and writing a log
def parseTweet(tweet):
    global tweetDict
    global parsedTweets
    global bad_tweets
    global neutral_tweets

    bully = 0

    if tweet.quote != 0:
        return 1
    
    classification = classify.predict(tweet.text)
    if classification > 0.5:
        bad_tweets.append(tweet)
        bully = 1
        print tweet.text
    else:
        neutral_tweets.append(tweet)

    table = db["tweets"]
    table.insert(dict(
        username=tweet.username,
    #    user_location=loc,
    #    coordinates=coords,
        bully=bully,
        text=tweet.text,
        created=tweet.created
#        polarity=sent.polarity,
#        subjectivity=sent.subjectivity
    ))

#Look for all tags and update our tweetDict
#    for tag in tweet.hashtags:
#        t = g["text"]
#        if(tweetDict.has_key(t)):
#            tweetDict[t] += 1
#        else:
#            tweetDict[t] = 1
#    parsedTweets += 1
    #Every 10th tweet we will output the most popular tag and write the info to the log
   
    summary = "neutral: " + str(len(neutral_tweets)) + " bad: " + str(len(bad_tweets))
#        with open("log.txt","a") as f:
#            f.write(summary + "\n")
    print summary 			

#Tweet class with all the information we need for this program (Hashtags and the actual tweet text)
class Tweet:
    username = ''
    text = ''
    hashtags = []
    mentions = []
    reply = 0
    quote = 0
    created = ''

    def __init__(self, json):
        self.username = json['user']['screen_name']
        self.text = json["text"].replace("\"",'')
        self.hashtags = json["entities"]["hashtags"]
        self.mentions = json["entities"]["user_mentions"]
        self.reply = json['in_reply_to_user_id']
        
        if 'quoted_status_id' in json:
            self.quote = json['quoted_status_id']
        
        self.created = parse(json['created_at'])

#Basic listener which parses the json, creates a tweet, and sends it to parseTweet
class TweetListener(StreamListener):
    def on_data(self, data):
        jsonData = json.loads(data)
        tweet = Tweet(jsonData)
        parseTweet(tweet)
        return True

    def on_error(self, status):
        print status
        if status_code == 420:
        #returning False in on_data disconnects the stream
            return False

def run(t = ['donaldtrump']):
    parsedTweets = 0
    listener = TweetListener()
    auth = oauthHandler.getAuth()
    stream = Stream(auth, listener)	
    stream.filter(track=t)

if __name__ == '__main__':
    run()
