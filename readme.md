# Inept's Video Awesome Madness
Dirty as hay, learn python with this file at your own risks.
TheDarkTiger 2023


## The scrip
Takes a video, and decompose it to sequences of images.
Or take a sequence of images, and reconstruct the video.

## How to use install?

### Classic python install
Install Python >=3.7
Install ffmpeg, and make sure it is available in the PATH.
You should be able to run the scrip by using "python main.py"

### Windows executable
Not yet available


## How to use?

By now, it's not really user friendly.
You need to change the script to make it work.
Even if the script will check as much as I could think of, it's always best save your hard work somewhere else before runing it.

### Video to Frames (Quick and dirty usage)

* Edit "main.py".
* line 17 change the variable "mode" to "vid2img" to deconstruct the video to frames
* line 24 change the name ("WIP") to set the project folder.
* line 27 change the file ("video.webm") to set the input video file.
* run the script by using "python main.py"

### Frames to Video (Quick and dirty usage)

* Edit "main.py"
* line 17 change the variable "mode" to "img2vid" to generate a video from the frames
* line 24 change the name ("WIP") to set the project folder.
* run the script by using "python main.py"


## Tip and Tricks

### Exported video scaling

By default, the program export video in -2x480 (meaning, keeping the aspect ration almost the same as the original images, as long as it fits the codec size specification and have a height of 480).
For now, the only way to change the video exported size is to edit the code.

By default, the program export video using "clostest neighbor" as a scaling method.
For now, the only way to change it is to edit the code.

Please, read the [ffmpeg documentation](https://ffmpeg.org/ffmpeg-filters.html#scale-1) to know what to use here. 

* Edit "IVAM\\__init__.py"
* Line 115, videoOptions = '-vf "scale=-2:480" -sws_flags neighbor'

### Exported video codecs

By default, the program export video in VP8
For now, the only way to change the video codec is to edit the code.

* Edit "IVAM\\__init__.py"
* Line 118 and 119, you will find two variables, "codec" and "encoding", change it accordingly:

| codec | "webm" | "mp4" |
| --- | --- | --- |
| encoding = "fast" | VP8 | x264 |
| encoding != "fast" | VP9 | x265 |
