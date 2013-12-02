from bs4 import BeautifulSoup
import re, string, sys, time, urllib 

##Declare global variables
showListingTime = 0
i = 0
programRunning = True
channelList = []
channelNum = []
customList = []
channel = []

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

def runProgram():

  #############FUNCTIONS#####################

  def clearCache():
    file = open('tvRage2.html','w')
    file.write('')
    file.close()

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
    showListingTime = int(showListingTime) + (interval)

    #Set boundaries for span of time to print entries for
    upperBoundary = "10:00 am" #int(showListingTime) + 100
    midBoundary = "09:30 am" #int(showListingTime) + 30
    lowerBoundary = "0900" #showListingTime

    #Initialize lists for each boundary
    upperBoundaryList = []
    midBoundaryList = []
    lowerBoundaryList = []

    #If show is at a given time, print the show
    for show in shows:
      if show['time'] == lowerBoundary:
        lowerBoundaryList.append(show)
      elif show['time'] == midBoundary:
        midBoundaryList.append(show)
      elif show['time'] == upperBoundary:
        upperBoundaryList.append(show)

    printShows(lowerBoundary, lowerBoundaryList)
#    printShows(midBoundary, midBoundaryList)
#    printShows(upperBoundary, upperBoundaryList)

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

#    if hour == "09":
#      print hour
#    if ("am" in hour):
#      print hour
#      hour = "00"
#      print ""
#    else:
#      hour = hour[:2]
#       print ""
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
  html_doc = open("tvRage.xml", "r")
  givenTime = getTime()
  global i
  global showListingTime
  showListingTime = givenTime
  text = html_doc.read()
  content = ''
  networks = []
  urls = []
  
  ##Soup Variables
  soup = BeautifulSoup(text)
  shows = soup.find_all('show')
  times = soup.find_all('time')
  allTags = soup.find_all()
  allNetworks = soup.find_all('network')
  allUrls = soup.find_all('link')
  #print soup

#  for show in shows:
#    defineChannelAttribute(show)
    #defineUrlAttribute(show)
    #defineShowTagContent(show)
  listNetworks()
  listUrls()
  for show in shows:
    defineChannelAttribute(show)
    defineUrlAttribute(show)
    assignShowtimes(show)
#    calculateHours(show['time'])
    convertTimeToUniversal(show)
    i += 1
  compareChannels()
#  assignShowtimes()
#  convertTimeToUniversal()
  #sortShows(0)
  paginate()

########################################################################


#connectToTvRage()
parseChannelsAndNumbers()

#while programRunning:
runProgram()
