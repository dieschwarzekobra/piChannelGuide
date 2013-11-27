from bs4 import BeautifulSoup

#Variables

##Basic text variables
html_doc = open("tvRage.html", "r")
text = html_doc.read()
firstShow = text.find('<SHOW>')
showText = text[firstShow:]

##Soup variables
soup = BeautifulSoup(text)
shows = soup.find_all('show')

##Arrays
updatedText = []
carrots = []
closingBrackets = []
openingBrackets = []
channel = []
channelList = []
channelNum = []
showListing = []
url = []
customList = []

def clearCache():
  file = open('tvRage2.html','w')
  file.write('')
  file.close()

def findCarrots():
  i = showText.find("^",0)
  while i>0:
    carrots.append(i)
    i = showText.find("^", i+1)

def findClosingBracket():
  i = firstShow
  while i>0:
    closingBrackets.append(i + 6)
    i = showText.find("<SHOW>",i+1)

def findOpeningBracket():
  i = showText.find("</SHOW>",0)
  while i>0:
    openingBrackets.append(i+1)
    i = showText.find("</SHOW>",i+1)

def extractChannel():
  iCarrot = 0
  iClosingBracket = 0
  for x in range(len(shows)-1):
    channelStart = closingBrackets[iClosingBracket]
    channelEnd = carrots[iCarrot]
    channel.append(showText[channelStart:channelEnd])
    iCarrot += 3
    iClosingBracket += 1

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
  iOpeningBracket = 0
  for x in range(len(openingBrackets)-1):
    urlStart = carrots[iCarrot] + 1
    urlEnd = openingBrackets[iOpeningBracket] - 1
    url.append(showText[urlStart:urlEnd])
    iCarrot += 3
    iOpeningBracket += 1

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
findClosingBracket()
findOpeningBracket()
extractChannel()
extractShowTitle()
extractUrl()
#putRowsBackTogether()
#determineImportantChannels()
parseChannelsAndChannelNumbers()

print "Channels that exist"
compareChannels()
printShowings()
