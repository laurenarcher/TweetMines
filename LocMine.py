from twitter import *
import csv
import codecs
import re

import pymongo

#MongoDB implementation based on instruction from here:
#https://skyl.org/log/post/skyl/2011/12/use-python-to-store-data-from-twitters-streaming-api-in-mongodb/

connection = pymongo.Connection("localhost", 27017)
db = connection.tweetmine

#This is an example of a geo-bounding box for the Toronto area.
#I used this: http://paulisageek.com/hacku/examples/geoBoundingBoxTabs.html

place = "-79.59,43.57,-79.10,43.87"

#Twitter now requires user authentication for nearly everything.
#Get more info here: https://dev.twitter.com/docs/streaming-apis

consumer_key = "XXxxXxXxxxxXXXxxXXXX"
consumer_secret = "XXXxXxxxXXxXXXXxXxXXx"
access_key = "XXXxxXXXxxXXxXxxXxxXXxXXXxxXxXXxxxxxXX"
access_secret = "XXXXxxxXXXxXXXXXXXxXXxxXXXxxxXXxx"

# Creates Twitter API object

auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
stream = TwitterStream(auth = auth, secure = True)

# Creates .csv file.
#I like to make a .csv copy for visualization & exploratory analysis.

loc_output_file = open(('locdata.csv'), 'a')
date = ["Date"]
user = ["User"]
text = ["Text"]
location = ["Location"]
lat = ["Latitude"]
lon = ["Longitude"]
new_line = date + user + text + location + lat + lon
csv.writer(loc_output_file).writerow(new_line)
loc_output_file.close()

#Now the meat.
            
locstream = stream.statuses.filter(locations = place)
for tweet in locstream:
        if tweet.get('text'):
                #This sends all tweet data to mongodb.
                db.loctweets.save(tweet)
                #This sends some tweet data to a .csv
                with open('locdata.csv', 'a') as loc_output_file:
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
                        csv.writer(loc_output_file).writerow(new_line)
                        print new_line
