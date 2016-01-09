# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 07:00:44 2016

@author: subhajit
"""

import os
from twitter import *
from PIL import Image

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np

os.chdir('Path/to/this/folder')

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
exec(compile(open('config.py', "rb").read(), 'config.py', 'exec'), config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		        auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))


#-----------------------------------------------------------------------
# perform a basic search 
# Twitter API docs:
# https://dev.twitter.com/docs/api/1/get/search
#-----------------------------------------------------------------------
query = twitter.search.tweets(q = "modi", count=5000) #, until='2016-01-07')

#-----------------------------------------------------------------------
# How long did this query take?
#-----------------------------------------------------------------------
print ("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]))

#-----------------------------------------------------------------------
# Loop through each of the results, and print its content.
#-----------------------------------------------------------------------
#for result in query["statuses"]:
#	print ("(%s) @%s %s" % (result["created_at"], result["user"]["screen_name"], result["text"]))

# make a corpus from the list of tweets
status_list = [ result['text'] for result in query['statuses']]
corpus = ' '.join(status_list)

# read in the image and colors and plot the word cloud
img = Image.open("modi.jpg")
#img = img.resize((980,1080), Image.ANTIALIAS)
modi_coloring = np.array(img)
image_colors = ImageColorGenerator(modi_coloring)
#hcmask = scipy.ndimage.zoom(hcmask, 2, order=3)
STOPWORDS = STOPWORDS.union({"http","https","t","co","rt","since","towards","now","ok","okay","tag", "amp"})
#wc = WordCloud(background_color="white", max_words=2000, mask=hcmask, stopwords=STOPWORDS)
wc = WordCloud(font_path='cabin-sketch.bold.ttf', background_color="white", max_words=2000, mask=modi_coloring, color_func=image_colors, stopwords=STOPWORDS)
wc.generate(corpus)
wc.to_file("wc_color.png")