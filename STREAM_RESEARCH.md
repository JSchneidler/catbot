ffserver: /etc/ffserver.conf, ffserver -d
Stream to ffserver: ffmpeg -r 25 -s 1280x720 -i /dev/video0 -maxrate 2M http://localhost:8090/feed1.ffm
https://stackoverflow.com/questions/37403282/is-there-anyone-who-can-success-real-time-streaming-with-ffserver

Stream to Twitch: ffmpeg -r 25 -s 1280x720 -i /dev/video0 -maxrate 2M  -f flv rtmp://twitchIngest
