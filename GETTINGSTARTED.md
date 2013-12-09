# Getting Started - Using the program

Before you get started, make sure you have:

* [Git](http://git-scm.com/downloads)
* [Python](http://www.python.org/getit/)
* [Firefox](http://www.mozilla.org/en-US/firefox/)
* A basic text editor
* A command-line interface

If you're not familiar with using the command-line, you may want to take a look at tutorials for using the command-line (also known as terminal or prompt) for your operating system.


## Step One: Clone the repository.

You can't really start using the program if you don't have the files :). Open up a terminal, and make sure you're in your directory of choice. Then, enter the following command:

```
git clone http://github.com/dieschwarzekobra/piChannelGuide.git
```

## Step Two: Edit channels.txt

To customize your list of channels, you must open up channels.txt in your text editor of choice and replace the default channels with your channels of choice. Be sure to maintain the format presented as the default: channelNumber_channelName  channelNumber_channelName  etc. There are two spaces between each channel. *i.e.: 2_fox  3_abc  4_pbs  5_cbs*. **It is also important for the channel names to be lowercase.**

## Step Three: Run the program.

In your terminal window, make sure you're in the piChannelGuide\programFiles directory. Then, run the following command:

```
python piChannelGuide.py
```

If you're using Windows, you can either create an alias for your python command, or use 
```
PATH:\TO\PYTHON\python.exe
```
 in place of just
```
python
```
. Of course you have to use whatever your path is to python, and not the placeholder text I have above.

The program should be running. Your firefox browser should open once the schedule for the next few hours is compiled.

## Things to note

This program is a work in progress. There are a lot of things that still need to be done. Right now, the program has to be re-run each time you want to recompile the schedule. My goal is to automate that. Any contributions to getting this project to function better are welcome!