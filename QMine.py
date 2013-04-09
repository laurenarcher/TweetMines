from twitter import *
import csv
import codecs
import re

import pymongo

#MongoDB implementation based on instruction from here:
#https://skyl.org/log/post/skyl/2011/12/use-python-to-store-data-from-twitters-streaming-api-in-mongodb/

connection = pymongo.Connection("localhost", 27017)
db = connection.tweetmine

#Search terms I am interested in.

search_term = "casinNO, ontag, onpoli, TOpoli, Toronto, builtheritage"

#Twitter now requires user authentication for nearly everything.
#Get more info here: https://dev.twitter.com/docs/streaming-apis

consumer_key = "XXxxXxXxxxxXXXxxXXXX"
consumer_secret = "XXXxXxxxXXxXXXXxXxXXx"
access_key = "XXXxxXXXxxXXxXxxXxxXXxXXXxxXxXXxxxxxXX"
access_secret = "XXXXxxxXXXxXXXXXXXxXXxxXXXxxxXXxx"

#Creates Twitter API object

auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
stream = TwitterStream(auth = auth, secure = True)

#Creates .csv file.
#I like to make a .csv copy for visualization & exploratory analysis.

q_output_file = open(('qdata.csv'), 'a')
date = ["Date"]
user = ["User"]
text = ["Text"]
location = ["Location"]
lat = ["Latitude"]
lon = ["Longitude"]
new_line = date + user + text + location + lat + lon
csv.writer(q_output_file).writerow(new_line)
q_output_file.close()

#Now the meat.

qstream = stream.statuses.filter(track = search_term)
for tweet in qstream:
        if tweet.get('text'):
                #This sends all tweet data to mongodb.
                db.qtweets.save(tweet)
                #This sends some tweet data to a .csv
                with open('qdata.csv', 'a') as q_output_file:
                        date = [tweet["created_at"].encode('utf-8')]
                        user = [tweet["user"]["screen_name"].encode('utf-8')]
                        text = [tweet["text"].encode('utf-8')]
                        location = [tweet["user"]["location"].encode('utf-8')]
                        coordinates = str(tweet["coordinates"])
                        coordinates = "".join(i for i in coordinates if i in ".-0123456789,")
                        coordinates = coordinates[1:-1]
                        lat = [coordinates[(coordinates.find(",")+1):-1]]
                        lon = [coordinates[0:(coordinates.find(","))]]
                        new_line = date + user + text + location + lat + lon
                        csv.writer(q_output_file).writerow(new_line)
                        print new_line

