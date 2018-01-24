**Install docker**

    curl -sSL https://get.docker.com | sh
    sudo usermod pi -aG docker
    reboot



sudo apt-get update
sudo apt-get install build-essential git libomxil-bellagio-dev

**Clone git repository**

cd ~
git clone https://github.com/ffmpeg/FFMpeg --depth 1

**Configure build for mmjpeg**

cd ~/FFMpeg
./configure --arch=armel --target-os=linux --enable-gpl --enable-omx --enable-omx-rpi --enable-nonfree

**Make using 4 processors (pi2/3)**

make -j4 

**Test**

cd ~/FFMpeg
./ffmpeg -re -f mjpeg -framerate 5 -i "http://localhost:8080/?action=stream" -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -acodec aac -ab 128k -strict experimental -s 640x480 -vcodec h264 -pix_fmt yuv420p -g 10 -vb 700k -framerate 5 -f flv rtmp://a.rtmp.youtube.com/live2/<STREAM_ID>