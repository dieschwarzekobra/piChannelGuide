from bs4 import BeautifulSoup
import re, string, sys, time, urllib 

##Declare global variables
showListingTime = 0
programRunning = True
channelList = []
channelNum = []
customList = []
channel = []

def connectToTvRage():
  page = urllib.urlopen("http://services.tvrage.com/feeds/fullschedule.php?country=US")
  page = page.read()
  page = string.replace(page, "[", "<")
  page = string.replace(page, "]", ">")
  xmlHeader = "<?xml version='1.0'?>\n\n"
  page = xmlHeader + page

  file = open("tvRage.html", "w")
  file.write(page)
  file.close()
  print "Connection complete."

#############################################################

def getImportantChannels():
#  usrInput = raw_input("What channels are important to you?[i.e.: 59_Animal Planet  83_Logo]: ")
  file = open("usrInput.txt", "r")
  input = file.read()
  file.close()
  usrList = input.split("  ")
  return usrList
  
#############################################################

def parseChannelsAndNumbers():
  usrList = getImportantChannels()
  for chann in usrList:
    splitList = chann.split("_")
    channelList.append(splitList[1])
    channelNum.append(splitList[0])

#############################################################

def compareChannels():
  for chann in channelList:
    if chann in channel:
      customList.append(chann)

#############################################################

def runProgram():

  #############FUNCTIONS#####################

  def clearCache():
    file = open('tvRage2.html','w')
    file.write('')
    file.close()

  ############################################

  def defineChannelAttribute(show):
    global content
    content = str(show.contents)
    startingPoint = content.find("'") + 1
    stoppingPoint = content.find("^")

    #Set attribute
    show['channel'] = content[startingPoint:stoppingPoint].lower()
    channel.append(content[startingPoint:stoppingPoint].lower())

    #Reset the content variable to erase channel from the content
    content = content[stoppingPoint+1:]

  ##############################################

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

  ###############################################

  def defineShowTagContent(show):
    global content
    contentEndingPoint = content.find("^")
    content = content[:contentEndingPoint]

    #Clear the contents of the tag
    show.clear()

    #Insert title into the tag
    show.insert(0, content)

  ################################################

  def assignShowtimes():
    for tag in allTags:
      if tag.name == "time":
        showTime = tag.contents
      elif tag.name == "show":
        tag['time'] = showTime

  #################################################

  def sortShows(interval):

    global showListingTime
    showListingTime = int(showListingTime) + (interval)

    #Set boundaries for span of time to print entries for
    upperBoundary = int(showListingTime) + 100
    midBoundary = int(showListingTime) + 30
    lowerBoundary = int(showListingTime)

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

    printShows(lowerBoundary, lowerBoundaryList)
    printShows(midBoundary, midBoundaryList)
    printShows(upperBoundary, upperBoundaryList)

  ###################################################

  def printShows(Boundary, List):

    print Boundary
    if len(customList) <= 0:
      print "Sorry, there are no shows for this time period :("
    elif len(customList) >= 1:
      for item in List:
        print item
        if item['channel'] in customList:
          print item

  ###################################################

  def getTime():

    #Get local time
    givenTime = time.strftime("%H%M", time.localtime())
    minutes = roundToNearestHalfHour(givenTime[:2])
    givenTime = str(givenTime[:2]) + str(minutes)

    return givenTime

  ####################################################

  def convertTimeToUniversal():
    for show in shows:
      hour = calculateHours(show['time'][0])
      minutes = roundToNearestHalfHour(show['time'][0][-5:-2])

      #Replace time with UTC time
      show['time'] = []
      show['time'].append(str(hour) + str(minutes))

  ####################################################

  def calculateHours(hour):
    if ("pm" in hour) and ("12" not in hour):
      hour = int(hour[:2]) + 12
    elif ("am" in hour) and ("120" in hour):
      hour = int(hour[:2]) + 12
    elif ("am" in hour):
      hour = "00"
    else:
      hour = hour[:2]
    return hour


  #####################################################

  def roundToNearestHalfHour(minutes):
    if int(minutes) > 30:
      minutes = "30"
    else:
      minutes = "00"
    return minutes

  ####################################################

  def paginate():
    usrInput = raw_input('Forward or backward?[f/b] Quit?[q]: ')
    if usrInput == "f":
      sortShows(100)
    elif usrInput == "b":
      sortShows(-100)
    elif usrInput == "q":
      global programRunning
      programRunning = False
      sys.exit()
    

  #Start Program
  clearCache()


  ############VARIABLES#####################

  ##Basic text variables
  html_doc = open("tvRage.html", "r")
  givenTime = getTime()
  global showListingTime
  showListingTime = givenTime
  text = html_doc.read()
  content = ''

  ##Soup Variables
  soup = BeautifulSoup(text)
  shows = soup.find_all('show')
  times = soup.find_all('time')
  allTags = soup.find_all()

  for show in shows:
    defineChannelAttribute(show)
    defineUrlAttribute(show)
    defineShowTagContent(show)

  compareChannels()
  assignShowtimes()
  convertTimeToUniversal()
  #sortShows(0)
  paginate()

########################################################################


connectToTvRage()
parseChannelsAndNumbers()

while programRunning:
  runProgram()
