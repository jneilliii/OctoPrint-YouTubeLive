**Install docker**

    curl -sSL https://get.docker.com | sh
    sudo usermod pi -aG docker
    sudo reboot

**Pull Docker Image**

    docker pull alexellis2/streaming:17-5-2017
	
**Clone Repository and Rebuild**

    cd ~
    git clone https://github.com/jneilliii/youtubelive --depth 1
	cd youtubelive
	docker build -t octoprint/youtubelive .	
	
**Test**

Set up your stream on the [YouTube Live Dashboard](https://www.youtube.com/live_dashboard) and enter your stream id in the command below in place of xxxx-xxxx-xxxx-xxxx.

    docker run --privileged --name YouTubeLive -ti octoprint/youtubelive:latest http://localhost:8080/?action=stream xxxx-xxxx-xxxx-xxxx

Stream should go live and re-encode the OctoPrint stream to YouTube.  Once verified close ffmpeg and remove docker container.
	
	ctrl+c
	docker rm YouTubeLive
	
**OctoPrint Settings**

Enter your stream id used above in the OctoPrint-YouTubeLive plugin settings.
	
