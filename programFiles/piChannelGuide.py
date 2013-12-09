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
  for chann in getImportantChannels():
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

  ############################################

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

  ################################################

  def assignShowtimes(show):
    show['time'] = show.parent['attr']
    show['day'] = show.parent.parent['attr']

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