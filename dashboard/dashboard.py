from flask import Flask, render_template, request
import sqlite3
import ast
import dataset
import topicmodel
from collections import defaultdict
import json

import streaming

db =app = Flask(__name__)
d = 'sqlite:///tweets.db'
def get_top_tweets():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * from twit_data  ORDER BY datetime DESC LIMIT 30")
    result = c.fetchall()
    tweets = []

    datetime_toptweets = result[0]['datetime']

    for tweet in result:
        tweets.append(tweet['top_tweet'])
    
    conn.close()

    return tweets, datetime_toptweets

def get_trends():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    trend = []
    trend_tweet = []

    c.execute("SELECT * from trend_data ORDER BY datetime DESC LIMIT 10") 
    result = c.fetchall()

    datetime_trends = result[0]['datetime']

    for r in result:
        trend.append(r['trend'])
        trend_tweet.append(r['trend_id1'])
        trend_tweet.append(r['trend_id2'])
        trend_tweet.append(r['trend_id3'])

    conn.close()

    return trend, trend_tweet, datetime_trends

def get_lang(): 
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * from lang_data ORDER BY datetime DESC LIMIT 1")

    result = c.fetchone()
    lang = ast.literal_eval(result['language'])
    top_lang = ast.literal_eval(result['top_language'])
  
    conn.close()
    return lang, top_lang

def get_tweet_data():
    db = dataset.connect(d)
    table = db['tweets']

    nosocialmediamessages = len(db['tweets'])
    nobullytraces = table.count(bully=1)
    return nosocialmediamessages, nobullytraces

def get_time_series_data():
    db = dataset.connect(d)
    table = db['tweets']
    MonthL = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    DayL = ['Mon','Tues','Wed','Thurs','Fri','Sat','Sun']

    rp = []
    for t in table.find(bully=1):
        rp.append({'y': DayL[t['created'].weekday()], 'a': 1})

    c = defaultdict(int)
    for e in rp:
        c[e['y']] += e['a']


#    weekts_dict="["

#    for t in table.find(bully=1):
#        dayobj_dict="{'y': '" + DayL[t['created'].weekday()] + "', 'a': '" + str(1) + "'},"
#        weekts_dict = weekts_dict + dayobj_dict

#    weekts_dict= weekts_dict + "]"

    weekts_dict = str([{'y': day, 'a': a} for day, a in c.items()])

    return weekts_dict, weekts_dict

def get_bully_data():
    db = dataset.connect(d)
    table = db['tweets']
    recentincidents = table.find(bully=1, order_by='created')
    recent_posts = []
    for t in recentincidents:
        recent_posts.append(t)
    return recent_posts

#@app.route("/",methods = ['POST'])
#def searchParams():
#    if request.method == 'POST':
#        result = request.form
#        query = result.split()
#        streaming.run(query)

@app.route("/")
@app.route("/",methods=['POST'])
def main():
    if request.method == 'POST':
        result = request.form
        query = result['search'].split()
        streaming.run(query)

    nosocialmediausers = 39
    nosocialmediamessages,nobullytraces = get_tweet_data()
   
    months_dict,weekts_dict = get_time_series_data()    
    recentincidents = get_bully_data()

    topics = topicmodel.topic_model()
   
    affective_dict = json.loads(topics['affective_counts_json'])

    affective_count_list = [] #must be in order
    affective_count_list.append(affective_dict['sadness'])
    affective_count_list.append(affective_dict['anticipation'])
    affective_count_list.append(affective_dict['disgust'])
    affective_count_list.append(affective_dict['positive'])
    affective_count_list.append(affective_dict['anger'])
    affective_count_list.append(affective_dict['joy'])
    affective_count_list.append(affective_dict['fear'])
    affective_count_list.append(affective_dict['trust'])
    affective_count_list.append(affective_dict['negative'])
    affective_count_list.append(affective_dict['surprise']) 

    affective_count_list_str = ','.join(map(str, affective_count_list))


    affective_cyber_dict = json.loads(topics['affective_counts_cyberbullying_json'])

    affective_count_list = [] #must be in order
    affective_count_list.append(affective_cyber_dict['sadness'])
    affective_count_list.append(affective_cyber_dict['anticipation'])
    affective_count_list.append(affective_cyber_dict['disgust'])
    affective_count_list.append(affective_cyber_dict['positive'])
    affective_count_list.append(affective_cyber_dict['anger'])
    affective_count_list.append(affective_cyber_dict['joy'])
    affective_count_list.append(affective_cyber_dict['fear'])
    affective_count_list.append(affective_cyber_dict['trust'])
    affective_count_list.append(affective_cyber_dict['negative'])
    affective_count_list.append(affective_cyber_dict['surprise'])

    affective_cyber_count_list_str = ','.join(map(str, affective_count_list))

    # Load and print up to 10 Topics
    tm_dict = json.loads(topics['topic_model_json'])
    count = 1
    tm_str = "<ul>"
    for tp in tm_dict:
        tm_str = tm_str + "<li><strong>Topic %d</strong></br>" % (count)
        words_in_topic = []
        for t in tp[1]:
            words_in_topic.append(t[0])
        wrds = ','.join(map(str, words_in_topic))
        tm_str = tm_str + wrds + "</li>"
        count = count + 1
        if count==11: break
    tm_str = tm_str + "</ul>"

    # Load and print up to 10 Topics
    tm_dict = json.loads(topics['topic_model_cyberbullying_json'])
    count = 1
    tm_cyber_str = "<ul>"
    for tp in tm_dict:
        tm_cyber_str = tm_cyber_str + "<li><strong>Topic %d</strong></br>" % (count)
        words_in_topic = []
        for t in tp[1]:
            words_in_topic.append(t[0])
        wrds = ','.join(map(str, words_in_topic))
        tm_cyber_str = tm_cyber_str + wrds + "</li>"
        count = count + 1
        if count==11: break
    tm_cyber_str = tm_cyber_str + "</ul>" 

    return render_template("dashboard.html", nobullytraces=nobullytraces,nosocialmediausers=nosocialmediausers,nosocialmediamessages=nosocialmediamessages, weekts_dict=weekts_dict,months_dict=months_dict,recentincidents=recentincidents, tm_str=tm_str, tm_cyber_str=tm_cyber_str, affective_count_list_str=affective_count_list_str, affective_cyber_count_list_str=affective_cyber_count_list_str)
#    language_data = []
#    top_language_data = []

#    lang, top_lang = get_lang()
#    for l in lang:
#        language_data.append([l[0], l[1], l[1]])

#    for t in top_lang:
#        top_language_data.append([t[0], t[1], t[1]])
#    return render_template("lang1.html", language_data = language_data, top_language_data = top_language_data)

#@app.route("/top_tweets")
#def top_tweets():
#    tweets, datetime_toptweets = get_top_tweets()
#    return render_template('top_tweets.html', tweets = tweets, datetime_toptweets = datetime_toptweets)

#@app.route("/trends")
#def trends():
#    trend, trend_tweet, datetime_trends = get_trends()
#    return render_template('trends.html', trend = trend, trend_tweet = trend_tweet, datetime_trends = datetime_trends)

if __name__ == "__main__":
    app.run(debug = True)    
