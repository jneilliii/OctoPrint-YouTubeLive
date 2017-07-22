# OctoPrint-YouTubeLive

**Overview:** A simple youtube live viewer tab for OctoPrint. Currently a work in progress and simple skeleton. 

**Details:** This plugin in combination with the instructions found [here](https://blog.alexellis.io/live-stream-with-docker/) creates a pretty good streaming solution for OctoPrint. Currently tested with Octoprint running on Raspberry Pi Zero W and Google Chrome. Would probably run better on a Pi 3 as the live stream does start to buffer running both OctoPrint and the stream from the same Pi Zero W. You could run your stream from any device, this plugin just creates the tab to allow you to look at the given channels live stream.
<img src="https://raw.githubusercontent.com/jneilliii/Octoprint-YouTubeLive/master/screenshot.jpg">
## Setup

Once installed enter your YouTube's channel id which can be found on your [Advanced Account Settings](https://www.youtube.com/account_advanced). Enter your YouTube Channel ID into the YouTube Live settings within OctoPrint's settings dialog.

manually:

    sudo pip install https://github.com/jneilliii/OctoPrint-YouTubeLive/archive/master.zip

## Configuration

## TODO:
* [ ] Additional testing.
