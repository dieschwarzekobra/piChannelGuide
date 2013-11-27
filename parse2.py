from bs4 import BeautifulSoup

#Variables

##Basic text variables
html_doc = open("tvRage.html", "r")
text = html_doc.read()
firstShow = text.find('<SHOW>')
firstTime = text.find('<TIME>')
showText = text[firstShow:]

##Soup variables
soup = BeautifulSoup(text)
shows = soup.find_all('show')

##Arrays
updatedText = []
carrots = []
openingTags = []
closingTags = []
channel = []
channelList = []
channelNum = []
showListing = []
url = []
customList = []
time = []

def clearCache():
  file = open('tvRage2.html','w')
  file.write('')
  file.close()

def findCarrots():
  i = showText.find("^",0)
  while i>0:
    carrots.append(i)
    i = showText.find("^", i+1)

def findOpeningTag(tag):
  if tag == "<SHOW>":
    i = firstShow
    while i>0:
      openingTags.append(i + 6)
      i = showText.find(tag,i+1)
  elif tag == "<TIME>":
    i = firstTime
    while i>0:
      openingTags.append(i + 6)
      i = soup.find(tag,i+1)

def findClosingTag(tag):
  i = showText.find(tag,0)
  while i>0:
    closingTags.append(i+1)
    i = showText.find(tag,i+1)

def countShows():
  findOpeningTag("<TIME>")
  timeCount = soup.find_all("time")
  iOpeningTag = 0
  for i in range(len(openingTags)-1): #show in shows:
    s = shows[i]
    if (len(s) + openingTags[i]) < openingTags[i+1]:
      s['time'] = timeCount[i].contents
      print s

def extractChannel():
  iCarrot = 0
  iOpeningTag = 0
  for x in range(len(shows)-1):
    channelStart = openingTags[iOpeningTag]
    channelEnd = carrots[iCarrot]
    channel.append(showText[channelStart:channelEnd])
    iCarrot += 3
    iOpeningTag += 1

def extractShowTitle():
  iCarrot = 0
  for x in range(len(shows)-1):
    show_tag = soup.show
    showStart = carrots[iCarrot]+1
    showEnd = carrots[iCarrot+1]
    showListing.append(showText[showStart:showEnd])
    iCarrot += 3



def extractUrl():
  iCarrot = 2
  iClosingTag = 0
  for x in range(len(closingTags)-1):
    urlStart = carrots[iCarrot] + 1
    urlEnd = closingTags[iClosingTag] - 1
    url.append(showText[urlStart:urlEnd])
    iCarrot += 3
    iClosingTag += 1

def writeToCache(list):
  file = open('tvRage2.html', 'a')
  for item in list:
    file.write(item)
  file.close()
  file = open('tvRage2.html', 'r')
  cache = file.read()
  file.close()
  return cache

def putRowsBackTogether():
  rows = []
  for i in range(len(shows)-1):
    row = "<a href='" + url[i] + "'><SHOW channel='" + channel[i] + "'>" + showListing[i] + "</SHOW></a>"
    rows.append(row)
  newText = writeToCache(rows)
  return newText

def defineTimeAttributes():
  timeElement = soup.find_all("time")
  for showTime in timeElement:
    showTime['showTime'] = showTime.contents

def determineImportantChannels():
  usrInput = raw_input("Please list the channels you're interested in, following this format: ChannelNumber_ChannelName, with two spaces separating each channel. (i.e. 53_MTV  59_Animal Planet): ")
  usrList = usrInput.split("  ")
  return usrList

def parseChannelsAndChannelNumbers():
  global channelList, channelNum
  usrList = determineImportantChannels()
  for chann in usrList:
    splitList = chann.split("_")
    channelList.append(splitList[1])
    channelNum.append(splitList[0])

def compareChannels():
  for chann in channelList:
    if chann in channel:
      customList.append(chann)

def printShowings():
  row = BeautifulSoup(putRowsBackTogether())
  
  for chann in customList:
    rowsWithChannel = row.find_all("show", channel=chann)
    print rowsWithChannel



#Call functions / Run Program
clearCache()
findCarrots()
findOpeningTag("<SHOW>")
findClosingTag("</SHOW>")
extractChannel()
extractShowTitle()
extractUrl()
#putRowsBackTogether()
#determineImportantChannels()
parseChannelsAndChannelNumbers()

print "Channels that exist"
compareChannels()
printShowings()
defineTimeAttributes()
countShows()
