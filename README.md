piChannelGuide
==============

_Class project for silshack in which a raspberry pi will be used to customize the channel browsing experience._

# piChannelGuide

## Project Purpose and Vision

The Raspberry Pi Channel Guide aims to be an easily navigable dynamic schedule generator that runs on the pi. Schedule navigation is made easier with a mechanism that allows users to browse through channel listings to find shows on their own time, rather than having to wait for a non-interactive channel guide to slowly scroll through 100+ channels. Overall, this project will probably extend beyond this course. I do have goals that I would like to finish by the end of the course, but all of the things that I want for the project will require more time than I have within the limits of this course.

While there are numerous channel guide programs and options out there, this channel guide aims to be easier to operate than those I have come in contact with. There is no installation necessary. Customization is relatively straightforward and less complicated than some of the other channel guide options out there. The interface is customizable HTML, and the program's design is modular enough for the user to add their own API if they are comfortable and determined enough with programming to do so.

## Milestones

* Program connects to TVRage Schedule API. At this point, API selection is not intended to be configurable by the user, but this could be a future addition to the project. This connection can be verified with the text from the API being printed onto the console.

* Program selects channels and time zones that apply to the Chapel Hill Area. More broadly, this milestone would enable the user to configure the program to fit their own personal locality. A later edition of this milestone would thus include the program’s acceptance of user input to select the channels that are meaningful to them.

* Program prints the schedule for a user-specified range of time and number of channels. First, the program should prompt, digest, and print the user specifications. Then, the program should print the shows and showtimes for all of the channels specified in the previous step.

* The software runs on the Raspberry Pi. The Raspberry Pi must be configured to display on the television screen. The software display needs to be formatted in a way that is useful for the user on a television screen.

* The software can be controlled by a remote control. Though the pi is a computer and could probably be navigated using a keyboard and/or a mouse, it would make more sense to be able to use a remote that also works with the television so that the user “work flow” when watching television is not interrupted. More research needs to be done to understand how this will work as well.

* The software operates similarly to a DVR. This is a more advanced goal than the scope of this project, but it is definitely a feature that I would like to integrate into the Pi Channel Guide in the long run. This can help smooth out the “work flow” even more.

* The software is well-documented. Once the software is functioning at a level that is useful for the intended user group, Getting Started documentation and an example website will be set up. This will likely be completed after the end of the course, but I envision this as an ongoing project that will be updated as the project is developed.

## Collaboration

I invite any and everyone to make suggestions on ways to improve this program. I have hit numerous unexpected roadblocks that have affected the quality of the program. It is definitely an interesting experience to realize how much I didn't know about how a project like this would work. I'm open to suggestions to making this an awesome open-source project and if you have any questions about how to get involved, please just create an issue and I'll get back to you as soon as I can. *For those of you who aren't familiar with creating issues and such*, you will need to [make a github account](https://github.com/join) before you can create an issue.

## Technologies Used 

A Raspberry Pi will be used to connect the guide to the television, and a remote control will eventually be used to control the Pi. At the moment, I'm using a wireless keyboard and trackpad combination instead of a remote control. Python will be used to accept and apply the user specifications as filters. BeautifulSoup will be used to parse the data into chunks so that the data can be more easily manipulated as individual pieces rather than one huge collection of data with huge manipulation limitations.


## Re-use

Anyone who does not have an easily navigable TV guide should be able to customize and use this project. Also, anyone who wants to use Python to parse data from an API could also find this project useful, as it can serve either as an example or a platform upon which they can build their own project. Overall, I hope for this project to be useful as more than just its main intended functionality. I want it to be a learning tool and maybe even a foundation for other work, which is a major characteristic of Open Source work as a concept. Therefore, a Github repository will definitely be used and hopefully well-documented. An example site is another goal, just in case someone who is less familiar with github wants to learn more about the project, or to use it for their own television watching needs.
