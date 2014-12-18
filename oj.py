import urllib2, alfred, urllib, itertools
from bs4 import BeautifulSoup
from bs4 import element as BSElem
#Target url we are searching on
url = "http://oj.leetcode.com/problems/"
#Fetch the webpage
usock = urllib2.urlopen(url)
data = usock.read()
usock.close()

def isTag(x):
    return isinstance(x, BSElem.Tag)

#Get the table content we want
dom = BeautifulSoup(data)
table = dom.find('table', id="problemList")

questions = []

for row in itertools.ifilter(isTag, table.tbody.contents):
        cell = list(itertools.ifilter(isTag, row.contents))
        questions.append((str(unicode(cell[1].a.string)), #name
            float(str(unicode(cell[3].string)).strip('%')), #AC Rate
            unicode("http://oj.leetcode.com"+str(unicode(cell[1].a['href']))) #url
        ))

theQuery = u'{query}'
theQuery = theQuery.replace('+', ' ')

matched = filter(lambda t: theQuery in t[0].lower(), questions)
matched = sorted(matched, key = lambda item: item[1], reverse=True)
result = []
id = 1
# # # Create list items with the information we get
for item in matched:
    result.append(
        alfred.Item({'uid':id, 'arg': item[2]}, item[0], 'AC Rate: ' + str(item[1]), ('icon.png', {'type':'png'}))
    )
    id += 1

# # Write the result into xml format and return it.
xml = alfred.xml(result)
alfred.write(xml)
