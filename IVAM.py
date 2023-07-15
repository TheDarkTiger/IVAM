#!/usr/bin/env python
#! coding: utf-8
#! python3
# ~= Inept's Video Awesome Madness =~
# Dirty as hay, learn python with this file at your own risks.
# TheDarkTiger 2023
#
# Takes a video, and decompose it to sequences of images.
# Or take a sequence of images, and reconstruct the video.

import os
import json

print( "Hi Nepter!" )

input = "aCAT47.webm"
output = "WIP"
mode = "vid2img"
# mode = "img2vid"

if mode == "vid2img" :
	print( "Vid 2 Images" )
	input = "aCAT47.webm"
	
	output = "WIP\\config.json"
	commandLine = f'ffprobe -v quiet -print_format json -show_format -show_streams "{input}">"{output}"'
	print( commandLine )
	os.system( commandLine )
	
	output = "WIP\\frame%04d.png"
	commandLine = f'ffmpeg -i "{input}" -r 30 -f image2 -vf "scale=-2:120" "{output}"'
	commandLine = f'ffmpeg -i "{input}" -f image2 -vf "scale=160:120:force_original_aspect_ratio=decrease,pad=160:120:-1:-1:color=black" "{output}"'
	print( commandLine )
	os.system( commandLine )
	
	output = "WIP\\audio.ogg"
	commandLine = f'ffmpeg -y -i "{input}" -vn -c:a libopus "{output}"'
	print( commandLine )
	os.system( commandLine )
	
	
elif mode == "img2vid" :
	print( "Images 2 Vid" )
	images = "WIP\\frame%04d.png"
	audio = "WIP\\audio.ogg"
	
	framerate = 24
	data = None
	with open( "WIP\\config.json", "r" ) as readFile :
		data = json.load(readFile)
		
	framerate = data["streams"][0]["r_frame_rate"]
	
	output = "WIP\\generated.webm"
	videoCodec = '-c:v libvpx-vp9'
	videoCodec = '-c:v libvpx'
	videoOptions = '-vf "scale=-2:480" -sws_flags neighbor'
	audioCodec = '-c:a libopus'
	commandLine = f'ffmpeg -framerate {framerate} -i "{images}" -i "{audio}" {videoCodec} {videoOptions} {audioCodec} "{output}"'
	print( commandLine )
	os.system( commandLine )
	
else :
	print( "Mode unknown" )
	


