from bs4 import BeautifulSoup
import re, string, sys, time, urllib 

##Declare global variables

showListingTime = 0
i = 0
programRunning = True
file = ''

channelList = []
channelNum = []
customList = []
channel = []
textForCache = []

def connectToTvRage():
  page = urllib.urlopen("http://services.tvrage.com/feeds/fullschedule.php?country=US")
  page = page.read()

  file = open("tvRage.xml", "w")
  file.write(page)
  file.close()
  print "Connection complete."

#############################################################

def getImportantChannels():

#Uncomment to allow user to input channels via the command line
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
  print customList

#############################################################

def writeToCache(text):
  global file
  testing = str(text)
  file.write(testing)
  print testing

#############################################################

def runProgram():

  #############FUNCTIONS#####################

  def clearCache():
    global file
    file = open('tvRage2.html','w')
    file.write('')
    file.close()
    file = open('tvRage2.html', 'a')

  ############################################

  def listNetworks():

    #Grab network
    for chann in allNetworks:
      networks.append(chann.contents[0])
    print "Done grabbing networks"

  ############################################

  def listUrls():
    #Grab url
    for url in allUrls:
      urls.append(url.contents[0])
    print "Done grabbing urls"

  ############################################

  def defineChannelAttribute(show):
    global i
    show['channel'] = networks[i].lower()
    channel.append(networks[i].lower())

  ##############################################

  def defineUrlAttribute(show):
    global i
    show['link'] = urls[i]

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

  def assignShowtimes(show):
    show['time'] = show.parent['attr']
       
  #################################################

  def sortShows(interval):

    global showListingTime
    showListingTime = showListingTime + interval

    #Set boundaries for span of time to print entries for
    lowerBoundary = showListingTime
    upperBoundary = lowerBoundary + 100
    if str(lowerBoundary)[-2:] == "30":
      midBoundary = lowerBoundary + 70
    else:
       midBoundary = lowerBoundary + 30

    #Initialize lists for each boundary
    upperBoundaryList = []
    midBoundaryList = []
    lowerBoundaryList = []

    #If show is at a given time, print the show
    for show in shows:
      if int(show['time']) == int(lowerBoundary):
        lowerBoundaryList.append(show)
      elif int(show['time']) == midBoundary:
        midBoundaryList.append(show)
      elif int(show['time']) == upperBoundary:
        upperBoundaryList.append(show)

    printShows(lowerBoundary, lowerBoundaryList)
    printShows(midBoundary, midBoundaryList)
    printShows(upperBoundary, upperBoundaryList)

  ###################################################

  def printShows(Boundary, List):
    global textForCache
    print Boundary
    writeToCache(Boundary)

    if len(customList) <= 0:
      print "Sorry, there are no shows for this time period :("
    #  writeToCache("Sorry, there are no shows for this time period :(")
    elif len(customList) >= 1:
      for item in List:
        if item['channel'] in customList:
          print item
          writeToCache(item)

  ###################################################

  def getTime():

    #Get local time
    givenTime = time.strftime("%H%M", time.localtime())
    minutes = roundToNearestHalfHour(givenTime[2:])
    givenTime = str(givenTime[:2]) + str(minutes)

    return givenTime

  ####################################################

  def convertTimeToUniversal(show):
    hour = calculateHours(show['time'])
    minutes = roundToNearestHalfHour(show['time'][-5:-2])

    #Replace time with UTC time
    show['time'] = str(hour) + str(minutes)

  ####################################################

  def calculateHours(hour):
    if ("pm" in hour) and ("12" not in hour):
      hour = int(hour[:2]) + 12
    elif ("am" in hour) and ("12:0" in hour):
      hour = "00"
    else:
      hour = hour[:2]
    return hour


  #####################################################

  def roundToNearestHalfHour(minutes):
    if int(minutes) >= 30:
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

  ##Basic variables and global variables
  ###Basic variables
  html_doc = open("tvRage.xml", "r")
  givenTime = getTime()
  networks = []
  urls = []

  ###Global variables
  global i
  global showListingTime

  ###Derivative variables
  showListingTime = int(givenTime) - 100
  text = html_doc.read()
  
  ##Soup Variables
  soup = BeautifulSoup(text)
  shows = soup.find_all('show')
  times = soup.find_all('time')
  allTags = soup.find_all()
  allNetworks = soup.find_all('network')
  allUrls = soup.find_all('link')

  listNetworks()
  listUrls()
  for show in shows:
    defineChannelAttribute(show)
    defineUrlAttribute(show)
    assignShowtimes(show)
    convertTimeToUniversal(show)
    i += 1
  compareChannels()
  paginate()
#  writeToCache(textForCache)

########################################################################


#connectToTvRage()
parseChannelsAndNumbers()

#while programRunning:
runProgram()
