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
* line 31 change the fps (12). This will affect the image generation, and thus the video generation too.
* run the script by using "python main.py"

### Frames to Video (Quick and dirty usage)

* Edit "main.py"
* line 17 change the variable "mode" to "img2vid" to generate a video from the frames
* line 24 change the name ("WIP") to set the project folder.
* run the script by using "python main.py"


## Tip and Tricks

### Exported frames scaling

By default, the program export frames in 160x120.
For now, the only way to change the video exported size is to edit the "project.json" file.
You can change in the section "frame" the "width" and "height".

### Project frames per second

The script forces the fps to 12. Feel free to either change the code (main.py, line 31, project.set_fps( 12 ) ), or edit the "project.json" file.
You can change in the section "video" the "fps" value.
Remember that doing so change both the frame generation and video reconstruction.
If, for exemple, you set it to 12 to export frames, and then 24 to make the video, the generated video will be twice as short, and the sound not in sync.

### Exported video scaling

By default, the program export video in 640x480.
For now, the only way to change the video exported size is to edit the "project.json" file.
You can change in the section "video" the "width" and "height".

By default, the program export video using "clostest neighbor" as a scaling method.
For now, the only way to change it is to edit the code.

Please, read the [ffmpeg documentation](https://ffmpeg.org/ffmpeg-filters.html#scale-1) to know what to use here. 

* Edit "IVAM\\__init__.py"
* Line 230, videoOptions = f'-vf "scale={w}:{h},setsar=1:1" -sws_flags neighbor'

### Exported video codecs

By default, the program export video in VP8
For now, the only way to change the video codec is to edit the code.
The "project.json" file is not yet used.

* Edit "IVAM\\__init__.py"
* Line 118 and 119, you will find two variables, "codec" and "encoding", change it accordingly:

| codec | "webm" | "mp4" |
| --- | --- | --- |
| encoding = "fast" | VP8 | x264 |
| encoding != "fast" | VP9 | x265 |

You can, obviously, force it to whatever you want by modyfing the code further; that needs, however, to know ffmpeg codecs designation and options.
