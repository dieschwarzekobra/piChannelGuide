#Import libraries
from bs4 import BeautifulSoup
import re, string, sys, time, urllib, webbrowser

#############################################################

#Declare global variables
showListingTime = 0
i = 0
programRunning = True
file = ''
day = ''

channelList = []
channelNum = []
customList = []
channel = []

#############################################################

#Define global functions
def connectToTvRage():
  page = urllib.urlopen("http://services.tvrage.com/feeds/fullschedule.php?country=US")
  page = page.read()

  file = open("xml/fullSchedule.xml", "w")
  file.write(page)
  file.close()
  print "Connection complete."


#############################################################

def getImportantChannels():

#Uncomment to allow user to input channels via the command line.
#  input = raw_input("What channels are important to you?[i.e.: 59_Animal Planet  83_Logo]: ")

#Comment everything up to "usrList = ..." to allow user to input channels via the command line.
  file = open("channels.txt", "r")
  input = file.read()
  file.close()

  usrList = input.split("  ")
  return usrList
  
#############################################################

def parseChannelsAndNumbers():
  usrList = getImportantChannels()
  if usrList > 1:
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

def printCustomList():
  usrList = getImportantChannels()
  if usrList > 1:
    for chann in usrList:
      dash = chann.find("_")
      chann = "<channel>" + chann[:dash] + " " + chann[dash+1:] + "</channel>"
      if "&" in chann:
        ampersand = chann.find("&")
        chann = chann[:ampersand] + chann[ampersand+1:]
      writeToCache(chann)

#############################################################

def writeToCache(text):
  global file
  testing = str(text)
  file.write(testing)

#############################################################


#Define program-level functions

def runProgram():

  #############FUNCTIONS#####################

  def clearCache():
    global file
    file = open('xml/cache.xml','w')
    file.write('<?xml version="1.0" encoding="ISO-8859-1" ?><?xml-stylesheet type="text/xsl" href="cache.xsl"?><guide>')
    file.close()
    file = open('xml/cache.xml', 'a')

  #################PARSE#####################

  def listNetworks():

    #Grab network
    for chann in allNetworks:
      networks.append(chann.contents[0])
    print "Done grabbing networks"

  ############################################

  def defineChannelAttribute(show):
    global i
    show['channel'] = networks[i].lower()
    channel.append(networks[i].lower())

  ############################################

  def assignShowtimes(show):
    show['time'] = show.parent['attr']
    show['day'] = show.parent.parent['attr']


  ###################DISPLAY######################

  def getTime():

    #Get local time
    givenTime = time.strftime("%H%M", time.localtime())
    minutes = roundToNearestHalfHour(givenTime[2:])
    givenTime = str(givenTime[:2]) + str(minutes)

    return givenTime

  #############################################

  def calculateHours(hour):
    if ("pm" in hour) and ("12" not in hour):
      hour = int(hour[:2]) + 12
    elif ("am" in hour) and ("12:0" in hour):
      hour = "00"
    else:
      hour = hour[:2]
    return hour

  #############################################

  def roundToNearestHalfHour(minutes):
    if int(minutes) >= 30:
      minutes = "30"
    else:
      minutes = "00"
    return minutes

  #############################################

  def convertTimeToUniversal(show):
    hour = calculateHours(show['time'])
    minutes = roundToNearestHalfHour(show['time'][-5:-2])

    #Replace time with UTC time
    show['time'] = str(hour) + str(minutes)


  #############################################

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
    print Boundary
    Boundary = "<time><header>" + str(Boundary)[-4:-2] + ":" + str(Boundary)[-2:] + "</header>"
    writeToCache(Boundary)
    if len(customList) <= 0:
      for item in List:
        if item['day'] == day:
          print item
          writeToCache(item)
    elif len(customList) >= 1:
      for item in List:
        if (item['channel'] in customList) and (item['day'] == day):
          print item
          writeToCache(item)
    endTag = "</time>"
    writeToCache(endTag)



  #Clear the cache
  #Connect to TVRage Full Schedule. Download the schedule for parsing.
  #Define channels that are important to the user.
  #Print this list of channels to the display and save it to the cache.
  #Parse the data provided by the user to separate the channels from the channel numbers.
  #Create a list of the channels present in the TV schedule.
  #Compare the user-provided list of channels to the list of channels present in the TV schedule. Compose a list of the channels each list has in common.
  #Get local time.
  #Convert all times to Universal Time, rounded to the nearest hour.
  #Parse TVRage schedule and restructure 'show' element to include a channel and time attribute.
  #Select upcoming shows that are showing within an hour and a half of the current local time.
  #Print those listings and save them to the cache.
  #Display the cached data in the webbrowser
  #Repeat every thirty minutes.