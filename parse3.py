from bs4 import BeautifulSoup
import time

##############################VARIABLES########################################

##Basic text variables
html_doc = open("tvRage.html", "r")
text = html_doc.read()
content = ''

##Soup variables
soup = BeautifulSoup(text)
shows = soup.find_all('show')
times = soup.find_all('time')
allTags = soup.find_all()

#############################FUNCTIONS#########################################

def clearCache():
  file = open('tvRage2.html','w')
  file.write('')
  file.close()

#######################################################################

def defineChannelAttribute(show):
  global content
  content = str(show.contents)
  startingPoint = content.find("'") + 1
  stoppingPoint = content.find("^")

  #Set attribute
  show['channel'] = content[startingPoint:stoppingPoint]

  #Reset the content variable to erase channel from the content
  content = content[stoppingPoint+1:]

#######################################################################

def defineUrlAttribute(show):
  global content
  urlStartingPoint = content.find("^")
  url = content[urlStartingPoint+1:]

  #Refine starting point
  urlStartingPoint = url.find("^") + 1
  urlStoppingPoint = url.find("'")

  url = url[urlStartingPoint:urlStoppingPoint]

  #Set attribute
  show['url'] = url

#######################################################################

def defineShowTagContent(show):
  global content
  contentEndingPoint = content.find("^")
  content = content[:contentEndingPoint]

  #Clear the contents of the tag
  show.clear()

  #Insert title into the tag
  show.insert(0, content)

########################################################################

def assignShowtimes():
  for tag in allTags:
    if tag.name == "time":
      showTime = tag.contents
    elif tag.name == "show":
      tag['time'] = showTime

########################################################################

def sortShows():
  #Find given time
  givenTime = getTime()

  #Set boundaries for span of time to print entries for
  upperBoundary = int(givenTime) + 100
  midBoundary = int(givenTime) + 30
  lowerBoundary = int(givenTime)

  #Initialize lists for each boundary
  upperBoundaryList = []
  midBoundaryList = []
  lowerBoundaryList = []

  #If show is at a given time, print the show
  for show in shows:
    if int(show['time'][0]) == lowerBoundary:
      lowerBoundaryList.append(show)
    elif int(show['time'][0]) == midBoundary:
      midBoundaryList.append(show)
    elif int(show['time'][0]) == upperBoundary:
      upperBoundaryList.append(show)

#  printShows(lowerBoundary, lowerBoundaryList)
#  printShows(midBoundary, midBoundaryList)
#  printShows(upperBoundary, upperBoundaryList)

########################################################################

def printShows(Boundary, List):

  print Boundary
  for item in List:
    print item

########################################################################

def getTime():
  #Get local time
  givenTime = time.strftime("%H%M", time.localtime())
  minutes = roundToNearestHalfHour(givenTime[:2])
  givenTime = str(givenTime[:2]) + str(minutes)

  return givenTime

########################################################################

def convertTimeToUniversal():
  for show in shows:
    hour = calculateHours(show['time'][0])
    minutes = roundToNearestHalfHour(show['time'][0][-5:-2])

    #Replace time with UTC time
    show['time'] = []
    show['time'].append(str(hour) + str(minutes))
    print show

########################################################################

def calculateHours(hour):
  if ("pm" in hour) and ("12" not in hour):
    hour = int(hour[:2]) + 12
  elif ("am" in hour) and ("120" in hour):
    hour = int(hour[:2]) + 12
  elif ("am" in hour) and ("1230" in hour):
    hour = "00"
  else:
    hour = hour[:2]
  return hour


########################################################################

def roundToNearestHalfHour(minutes):
  if int(minutes) > 30:
    minutes = "30"
  else:
    minutes = "00"
  return minutes


########################################################################

def runProgram():
  clearCache()
  for show in shows:
    defineChannelAttribute(show)
    defineUrlAttribute(show)
    defineShowTagContent(show)
  assignShowtimes()
  convertTimeToUniversal()
  sortShows()

########################################################################


runProgram()
getTime()
