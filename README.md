#TweetMines
==========

Twitter data mining using MongoDB and Python Twitter Tools. 

This miner uses the Twitter Streaming API, which is explained in more detail here:

https://dev.twitter.com/docs/streaming-apis/streams/public

#Requires 

Python Twitter Tools:

https://github.com/sixohsix/twitter

Pymongo:

https://pypi.python.org/pypi/pymongo/

And MongoDB:

http://www.mongodb.org/

MongoDB implementation is based on this post here:

https://skyl.org/log/post/skyl/2011/12/use-python-to-store-data-from-twitters-streaming-api-in-mongodb/

#LocMine: 

Gathers geocoded tweets within a geo-bounding box area (I use the Toronto area here)

I used this to define my bounding box:

http://paulisageek.com/hacku/examples/geoBoundingBoxTabs.html

#QMine: 

Gathers tweets based on a list of queries. Keywords I am interesting in tracking.
