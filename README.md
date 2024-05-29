# OctoPrint-YouTubeLive
**Alert - Breaking Change by YouTube:** Due to the addition of Live Control Room by YouTube there are extra steps necessary to go live now. You can no longer just simply use a generic live stream key unless you utilize the `Stream Now Classic` interface. There is no indication of when that option will no longer be available. 

In the new `Control Room` interface you will have to manually create your live broadcast and Enable the options `Enable Auto-start` otherwise you'll have to press the `Go Live` button after starting the stream from the plugin's tab. The stream key used in the plugin's settings will need to be updated for the auto-generated stream key provided in the new interface or you will need to create a re-useable one from the drop-down and save that into the plugin's settings.

If the option `Enable Auto-stop` option is enabled the stream will automatically end and the broadcast will be closed and cannot be re-used. It may be possible to leave that option disabled and re-use the broadcast later, but that is currently not fully tested and more than likely the broadcast will be ended after some currently unknown timeout value by YouTube.

The drawback of re-using the same broadcast, if it is possible, is that recordings will not be generated for inidivudual sessions and you'll have an extremely long single recording once the stream is eventually ended.

As I personally don't use this plugin, future development will be dependant on votes from my higher Tier Patrons/Github Sponsors, so if you want this situation to be improved, consider becoming a Patron/Sponsor.

**Overview:** Plugin that adds a tab to OctoPrint for viewing, starting, and stopping a YouTube Live stream. 

**Details:** Based on the work found [here](https://blog.alexellis.io/live-stream-with-docker/). Currently tested with OctoPrint running on a Raspberry Pi Zero W and on a Pi3. 

<img src="https://raw.githubusercontent.com/jneilliii/Octoprint-YouTubeLive/master/tab_screenshot.jpg">

## Requirements for Streaming
Follow the instructions found [here](docker_instructions.md) to install and configure docker/mmjpeg for use with this plugin for Live streaming. This is not necessary if you just want to view a YouTube channel in a tab.

## Setup
Once installed enter your YouTube's channel id ([Advanced Account Settings](https://www.youtube.com/account_advanced)) and your YouTube stream id ([YouTube Live Dashboard](https://www.youtube.com/live_dashboard)) into the YouTube Live plugin settings.

<img src="https://raw.githubusercontent.com/jneilliii/Octoprint-YouTubeLive/master/settings_screenshot.jpg">

## Get Help

If you experience issues with this plugin or need assistance please use the issue tracker by clicking issues above.

### Additional Plugins

Check out my other plugins [here](https://plugins.octoprint.org/by_author/#jneilliii)

### Sponsors
- Andreas Lindermayr
- [@TheTuxKeeper](https://github.com/thetuxkeeper)
- [@tideline3d](https://github.com/tideline3d/)
- [SimplyPrint](https://simplyprint.io/)
- [Andrew Beeman](https://github.com/Kiendeleo)
- [Calanish](https://github.com/calanish)
- [Lachlan Bell](https://lachy.io/)
- [Jonny Bergdahl](https://github.com/bergdahl)
## Support My Efforts
I, jneilliii, programmed this plugin for fun and do my best effort to support those that have issues with it, please return the favor and leave me a tip or become a Patron if you find this plugin helpful and want me to continue future development.

[![Patreon](patreon-with-text-new.png)](https://www.patreon.com/jneilliii) [![paypal](paypal-with-text.png)](https://paypal.me/jneilliii)

<small>No paypal.me? Send funds via PayPal to jneilliii&#64;gmail&#46;com</small>
