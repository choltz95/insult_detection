# module oath
import tweepy

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="tZVCAJuCMkmdIPShR27lj1Bmc"
consumer_secret="QcwO5snWlEOb7yV8I72zUSriAiPrP4Mo8e2zFozRXlvtyjvb2i"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="3937769356-lUgSfOmCDV6xAg8hj0uLuXKeSO0Gov1pAj9B3vA"
access_token_secret="WfRRt8J8OrKlWD6QaibCjCcq1IVqYjKAt2RfzLeH0tUSl"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def getAPI():
	api = tweepy.API(auth)
	print "DEBUG: " + api.me().name + " is no logged in!"
	return api

def getAuth():
	return auth
