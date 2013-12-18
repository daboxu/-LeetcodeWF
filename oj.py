import urllib2, alfred, urllib
from bs4 import BeautifulSoup
#Target url we are searching on
url = "http://oj.leetcode.com/problems/"
#Fetch the webpage
usock = urllib2.urlopen(url)
data = usock.read()
usock.close()

#Get the table content we want
dom = BeautifulSoup(data)
tds = dom.find_all('td')

possbility = [] # Array for probability
count = 0 # Counter to control the information we are accessing
# count == 0 means we are accessing the title
# count == 2 means we are accessing the AC rate
urls = [] # Array for urls
title  = [] # Array for titles

#In the for loop, get every question out from
#the webpage
for td in tds:
    if '\n' not in  td.contents:
        if count==0:
            # Get the title
            for t in td.children:
                title.append(str(unicode(t.contents[0])))
            # Get the url
            urls.append("http://oj.leetcode.com"+ str(unicode(td.a['href'])))
            count += 1
        elif count == 2:
            # Get the AC rate
            possbility.append(str(unicode(td.contents[0])))
            count = 0
        else:
            # Skip the Date column
            count += 1
# Get the keyword which user input
theQuery = u'{query}'
theQuery = urllib.quote_plus(theQuery)
i = 0
indexes = []
result = []
# In the for loop, search the keyword in all titles,
# record the index of the title.
for t in title:
    if theQuery in t.lower():
        indexes.append(i)
    i += 1
# Create list items with the information we get
for ix in indexes:
    item = alfred.Item({'uid':1, 'arg':urls[ix]}, title[ix], possbility[ix], ('icon', {'type':'png'}))
    result.append(item)
# Write the result into xml format and return it.
xml = alfred.xml(result)
alfred.write(xml)